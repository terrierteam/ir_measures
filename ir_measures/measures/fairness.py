from abc import abstractmethod, ABC
from collections import Counter
from enum import Enum
from functools import cached_property
from itertools import permutations
from math import log, nextafter
from random import choice
from typing import (
    Iterable, Union, Iterator, Hashable, Optional, Sequence, TYPE_CHECKING
)

from ir_measures.measures import (
    Measure, ParamInfo, register
)
from ir_measures.util import Metric, rel_entr

if TYPE_CHECKING:
    from pandas import DataFrame

ColumnType = Hashable
GroupNameType = Hashable


class ProtectedGroupStrategy(Enum):
    """
    Strategy for selecting the protected group per query,
    in case no fixed protected group was given.
    """

    MINORITY = "minority"
    """
    Select the group that occurs least often in the query's qrels.
    """

    MAJORITY = "majority"
    """
    Select the group that occurs most often in the query's qrels.
    """


class TieBreakingStrategy(Enum):
    """
    Strategy for breaking ties when selecting the protected group
    using the minority or majority strategies.
    E.g., if groups A and B occur equally often, then the tie breaking strategy
    determines whether A or B would be used as protected group.
    """

    RANDOM = "random"
    """
    For ties in the protected group selection, choose the protected group 
    randomly. Note that this introduces randomness and multiple measurements 
    on the same run can lead to different result metrics.
    """

    GROUP_ASCENDING = "group-ascending"
    """
    For ties in the protected group selection, choose the protected group 
    by ascending order of the group names.
    """

    GROUP_DESCENDING = "group-descending"
    """
    For ties in the protected group selection, choose the protected group 
    by descending order of the group names.
    """


class FairnessMeasure(Measure, ABC):
    SUPPORTED_PARAMS = {
        "cutoff": ParamInfo(
            dtype=int,
            required=False,
            desc="Ranking cutoff threshold."
        ),
        "group_col": ParamInfo(
            dtype=Hashable,
            required=False,
            default="group",
            desc="Group column in the run."
        ),
        "groups": ParamInfo(
            dtype=str,
            required=False,
            desc="Comma-separated list of group names (optional)."
        ),
        "protected_group": ParamInfo(
            dtype=Hashable,
            required=False,
            default=ProtectedGroupStrategy.MINORITY.value,
            desc="Protected group name or selection strategy."
        ),
        "tie_breaking": ParamInfo(
            dtype=Hashable,
            required=False,
            desc="Tie breaking strategy when selecting the protected group "
                 "using the minority or majority strategies. Can also be a "
                 "comma-separated preference list. (If not specified, "
                 "ties will raise an exception.)"
        ),
    }

    @cached_property
    def _cutoff_param(self) -> Optional[int]:
        if "cutoff" not in self.params:
            return None
        return self.params["cutoff"]

    @cached_property
    def _group_col_param(self) -> ColumnType:
        if "group_col" not in self.params:
            return "group"
        return self.params["group_col"]

    @cached_property
    def _groups_param(self) -> Optional[set[str]]:
        if "groups" not in self.params:
            return None
        groups = self.params["groups"]
        return {
            group.strip()
            for group in str(groups).split(",")
        }

    @cached_property
    def _protected_group_param(self) -> Union[
        ProtectedGroupStrategy, GroupNameType
    ]:
        if "protected_group" not in self.params:
            return ProtectedGroupStrategy.MINORITY
        protected_group = self.params["protected_group"]
        if protected_group in {s.value for s in ProtectedGroupStrategy}:
            return ProtectedGroupStrategy(protected_group)
        if not isinstance(protected_group, GroupNameType):
            raise ValueError(
                f"Illegal protected_group param: {protected_group}"
            )
        return protected_group

    @cached_property
    def _tie_breaking_param(self) -> Union[
        TieBreakingStrategy, Sequence[GroupNameType], None
    ]:
        if "tie_breaking" not in self.params:
            return None
        tie_breaking = self.params["tie_breaking"]
        if tie_breaking is None:
            return None
        if tie_breaking in {s.value for s in TieBreakingStrategy}:
            return TieBreakingStrategy(tie_breaking)
        if not isinstance(tie_breaking, (str, bytes)):
            raise ValueError(
                f"Illegal tie_breaking param: {tie_breaking}"
            )
        return [
            group.strip()
            for group in str(tie_breaking).split(",")
        ]

    @abstractmethod
    def unfairness(
            self,
            ranking: tuple[GroupNameType],
            groups: set[GroupNameType],
            group_counts: dict[GroupNameType, int],
            protected_group: GroupNameType,
    ) -> float:
        """
        Compute a ranking's unfairness of representing a given protected group.
        Pre-computed group counts are provided for efficient computation.

        :param ranking: Ranking, given as an ordered sequence of the ranked
        items groups.
        :param groups: Set of groups to be considered for measuring fairness.
        :param group_counts: Lookup table of how often each group occurs in the
        query's qrels.
        :param protected_group: Name of the protected group.
        :return: Group fairness score for the protected group.
        """
        pass

    @staticmethod
    def group_counts(
            qrels_or_ranking: Iterable[GroupNameType],
            groups: set[GroupNameType],
    ) -> dict[GroupNameType, int]:
        """
        Compute the number of occurrences of each group in the qrels or
        ranking.
        :param qrels_or_ranking: Qrels or ranked list, given as iterable of
        group names.
        :param groups: Set of groups to be considered for counting occurrences.
        :return: Lookup table of how often each group occurs in the qrels or
        ranking.
        """
        counts = Counter(qrels_or_ranking)
        return {group: counts.get(group, 0) for group in groups}

    def _protected_group(
            self,
            group_counts: dict[GroupNameType, int],
    ) -> GroupNameType:
        """
        Determine the protected group based on the group counts for a query.
        :param group_counts: Lookup table of how often each group occurs in the
        qrels or ranking.
        :return: Name of the protected group.
        """
        protected_group = self._protected_group_param
        if isinstance(protected_group, ProtectedGroupStrategy):
            strategy: ProtectedGroupStrategy = protected_group
            groups: list[tuple[GroupNameType, int]] = [
                item for item in group_counts.items()
            ]
            if strategy == ProtectedGroupStrategy.MINORITY:
                groups = sorted(groups, key=lambda item: item[1])
            elif strategy == ProtectedGroupStrategy.MAJORITY:
                groups = sorted(groups, key=lambda item: item[1], reverse=True)
            else:
                raise ValueError(
                    f"Unknown protected group strategy: {strategy}"
                )
            if len(groups) > 1 and groups[0][1] == groups[1][1]:
                # Tie in group selection.
                count = groups[0][1]
                tie_groups = [
                    group[0]
                    for group in groups
                    if group[1] == count
                ]
                tie_breaking = self._tie_breaking_param
                if tie_breaking is None:
                    raise ValueError(
                        f"Could not select protected group "
                        f"by {strategy.value} because of a tie. "
                        f"Groups {tie_groups} all occur {count} time(s)."
                    )
                elif isinstance(tie_breaking, TieBreakingStrategy):
                    if not all(hasattr(g, "__lt__") for g in tie_groups):
                        raise ValueError(
                            f"Tie breaking {tie_breaking.value} requires "
                            f"sorting but groups are not "
                            f"sortable: {tie_groups}"
                        )
                    if tie_breaking == TieBreakingStrategy.RANDOM:
                        return choice(tie_groups)
                    elif tie_breaking == TieBreakingStrategy.GROUP_ASCENDING:
                        # noinspection PyTypeChecker
                        return sorted(tie_groups)[0]
                    elif tie_breaking == TieBreakingStrategy.GROUP_DESCENDING:
                        # noinspection PyTypeChecker
                        return sorted(tie_groups, reverse=True)[0]
                else:
                    tie_breaking_groups = [
                        group
                        for group in tie_breaking
                        if group in tie_groups
                    ]
                    if len(tie_breaking_groups) == 0:
                        raise ValueError(
                            f"Tie breaking preference {tie_breaking} not "
                            f"applicable to resolve tie: {tie_groups}"
                        )
                    return tie_breaking_groups[0]
            return groups[0][0]
        else:
            return protected_group

    @staticmethod
    def _permuted_rankings(
            ranking: tuple[GroupNameType],
    ) -> set[tuple[GroupNameType]]:
        """
        Generate all possible, unique permutations of the ranking.
        :param ranking:
        :return: Set of rankings, each given as an ordered sequence of the
        ranked items groups.
        """
        # noinspection PyTypeChecker
        return set(permutations(ranking))

    def max_unfairness(
            self,
            ranking: tuple[GroupNameType],
            groups: set[GroupNameType],
            group_counts: dict[GroupNameType, int],
            protected_group: GroupNameType,
    ) -> float:
        """
        Compute a ranking's maximum possible unfairness of representing a given
        protected group. Pre-computed group counts are provided for efficient
        computation.

        A naive implementation can just generate all possible permutations of
        the ranking and iteratively find the maximum across the permuted
        rankings. Subclasses should instead override this method with an
        analytical solution, if possible.

        :param ranking: Ranking, given as an ordered sequence of the ranked
        items groups.
        :param groups: Set of groups to be considered for measuring fairness.
        :param group_counts: Lookup table of how often each group occurs in the
        query's qrels.
        :param protected_group: Name of the protected group.
        :return: Group fairness score for the protected group.
        """
        return max(
            self.unfairness(
                permuted_ranking,
                groups,
                group_counts,
                protected_group,
            )
            for permuted_ranking in self._permuted_rankings(ranking)
        )

    def _measure_query(
            self,
            qrels: tuple[GroupNameType],
            ranking: tuple[GroupNameType],
            groups: set[GroupNameType],
    ) -> float:
        """
        Measure fairness of a ranking for a single query, based on the query's
        qrels and groups to be considered.
        :param qrels: Collection of group names in the query's qrels.
        :param ranking: Ranking, given as an ordered sequence of the ranked
        items groups.
        :param groups: Set of groups to be considered for measuring fairness.
        :return:
        """
        group_counts = self.group_counts(qrels, groups)
        protected_group = self._protected_group(group_counts)
        if protected_group not in group_counts.keys():
            raise ValueError(
                f"Protected group {protected_group} "
                f"not found in groups {set(group_counts.keys())}."
            )

        max_unfairness = self.max_unfairness(
            ranking,
            groups,
            group_counts,
            protected_group
        )
        if max_unfairness == 0:
            return 0
        unfairness = self.unfairness(
            ranking,
            groups,
            group_counts,
            protected_group
        )
        normalized_unfairness = unfairness / max_unfairness
        return normalized_unfairness

    def _groups(
            self,
            qrels: tuple[GroupNameType],
    ) -> set[GroupNameType]:
        """
        Determine the set of groups to be considered for measuring fairness.
        :param qrels: Collection of group names in the qrels.
        :return: Set of groups to be considered for measuring fairness.
        """
        if self._groups_param is not None:
            return self._groups_param
        return set(qrels)

    def measure(self, qrels: "DataFrame", run: "DataFrame") -> Iterator[Metric]:
        """
        Measure fairness of a run based on qrels.
        :param qrels: Data frame with qrels for each query. The query should be
        given in the ``query_id`` column and the group in the specified column
        as per the measure's parameters.
        :param run: Data frame with ranking for each query. The query should be
        given in the ``query_id`` column and the group in the specified column
        as per the measure's parameters.
        :return:
        """
        group_col = self._group_col_param
        qrels = qrels[["query_id", group_col]]
        run = run[["query_id", group_col]]

        groups = self._groups(qrels[group_col])
        if len(groups) == 0:
            raise ValueError("No groups given.")

        if self._cutoff_param is not None:
            run = run.groupby("query_id").head(self._cutoff_param)

        for qid, ranking in run.groupby("query_id"):
            yield Metric(
                str(qid),
                self,
                self._measure_query(
                    tuple(qrels[qrels["query_id"] == qid][group_col]),
                    tuple(ranking[group_col]),
                    groups,
                )
            )

    def __str__(self):
        name = self.NAME
        cutoff = ""
        if self._cutoff_param is not None:
            cutoff = f"@{self._cutoff_param}"
        group_col = None
        if self._group_col_param != "group":
            group_col = repr(self._group_col_param)
        groups = None
        if self._groups_param is not None:
            groups = repr(",".join(self._groups_param))
        protected_group_param = self._protected_group_param
        protected_group = None
        if isinstance(protected_group_param, ProtectedGroupStrategy):
            if protected_group_param != ProtectedGroupStrategy.MINORITY:
                protected_group = repr(protected_group_param.value)
        elif isinstance(protected_group_param, Hashable):
            protected_group = repr(protected_group_param)
        tie_breaking_param = self._tie_breaking_param
        tie_breaking = None
        if isinstance(tie_breaking_param, TieBreakingStrategy):
            tie_breaking = repr(tie_breaking_param.value)
        elif isinstance(tie_breaking_param, Sequence):
            tie_breaking = repr(",".join(tie_breaking_param))
        params = [
            f"{name}={param}"
            for name, param in {
                "group_col": group_col,
                "groups": groups,
                "protected_group": protected_group,
                "tie_breaking": tie_breaking,
            }.items()
            if param is not None
        ]
        return f"{name}{cutoff}({','.join(params)})"


class _NormalizedDiscountedDifference(FairnessMeasure):
    """
    Normalized discounted difference (rND) computes the difference in the
    proportion of members of the protected group at top-i and in the over-all
    population, accumulated for all cutoff points in the ranking with a
    logarithmic discount, and finally normalized wrt. the ideal rND.

    ::

        @inproceedings{YangS2017,
            author = {Yang, Ke and Stoyanovich, Julia},
            title = {Measuring Fairness in Ranked Outputs},
            year = {2017},
            isbn = {9781450352826},
            publisher = {Association for Computing Machinery},
            address = {New York, NY, USA},
            url = {https://doi.org/10.1145/3085504.3085526},
            doi = {10.1145/3085504.3085526},
            booktitle = {Proceedings of the 29th International Conference on
                Scientific and Statistical Database Management},
            articleno = {22},
            numpages = {6},
            location = {Chicago, IL, USA},
            series = {SSDBM '17}
        }
    """

    NAME = "rND"
    __name__ = "rND"

    def unfairness(
            self,
            ranking: tuple[GroupNameType],
            groups: set[GroupNameType],
            group_counts: dict[GroupNameType, int],
            protected_group: GroupNameType,
    ) -> float:
        n = sum(group_counts.values())
        s_plus = group_counts[protected_group]

        metric = 0
        for i in range(1, len(ranking)):
            ranking_i = ranking[:i]
            group_counts_i = self.group_counts(ranking_i, groups)

            s_plus_i = group_counts_i[protected_group]

            metric += (
                    (1 / log(i + 1, 2)) *
                    abs(
                        abs(s_plus_i / (i + 1)) -
                        abs(s_plus / n)
                    )
            )

        return metric


NormalizedDiscountedDifference = _NormalizedDiscountedDifference()
rND = NormalizedDiscountedDifference
register(rND, ["NormalizedDiscountedDifference"])


class _NormalizedDiscountedKlDivergence(FairnessMeasure):
    """
    Normalized discounted KL-divergence (rKL) computes the expectation of the
    difference between protected group membership at top-i versus in the
    overall population, accumulated for all cutoff points in the ranking with a
    logarithmic discount, and finally normalized wrt. the ideal rKL.
    ::

        @inproceedings{YangS2017,
            author = {Yang, Ke and Stoyanovich, Julia},
            title = {Measuring Fairness in Ranked Outputs},
            year = {2017},
            isbn = {9781450352826},
            publisher = {Association for Computing Machinery},
            address = {New York, NY, USA},
            url = {https://doi.org/10.1145/3085504.3085526},
            doi = {10.1145/3085504.3085526},
            booktitle = {Proceedings of the 29th International Conference on
                Scientific and Statistical Database Management},
            articleno = {22},
            numpages = {6},
            location = {Chicago, IL, USA},
            series = {SSDBM '17}
        }
    """

    SUPPORTED_PARAMS = {
        **FairnessMeasure.SUPPORTED_PARAMS,
        "correct_extreme": ParamInfo(
            dtype=bool,
            required=False,
            default=True,
            desc="correct extreme probability distributions such "
                 "that 0 > P(x) > 1 and 0 > Q(x) > 1"
        ),
    }
    NAME = "rKL"
    __name__ = "rKL"

    @cached_property
    def _correct_extreme(self) -> bool:
        if "correct_extreme" not in self.params:
            return True
        return self.params["correct_extreme"]

    def _distribution(
            self,
            plus: int,
            minus: int,
            n: int,
    ) -> tuple[float, float]:
        distribution = (plus / n, minus / n)
        if self._correct_extreme:
            if plus == n:
                q_plus = nextafter(distribution[0], 0)
                distribution = (q_plus, 1 - q_plus)
            elif minus == n:
                q_minus = nextafter(distribution[1], 0)
                distribution = (1 - q_minus, q_minus)
        return distribution

    @staticmethod
    def _kl_divergence(x1: Sequence[float], x2: Sequence[float]) -> float:
        return sum(rel_entr(x1, x2))

    def unfairness(
            self,
            ranking: tuple[GroupNameType],
            groups: set[GroupNameType],
            group_counts: dict[GroupNameType, int],
            protected_group: GroupNameType,
    ) -> float:
        n = sum(group_counts.values())
        s_plus = group_counts[protected_group]
        s_minus = n - s_plus
        q = self._distribution(s_plus, s_minus, n)

        metric = 0
        for i in range(1, len(ranking)):
            ranking_i = ranking[:i]
            group_counts_i = self.group_counts(ranking_i, groups)

            s_plus_i = group_counts_i[protected_group]
            s_minus_i = i - s_plus_i
            p = self._distribution(s_plus_i, s_minus_i, i)

            metric += self._kl_divergence(p, q) / log(i + 1, 2)

        return metric


NormalizedDiscountedKlDivergence = _NormalizedDiscountedKlDivergence()
rKL = NormalizedDiscountedKlDivergence
register(rKL, ["NormalizedDiscountedKlDivergence"])


class _NormalizedDiscountedRatio(FairnessMeasure):
    """
    Normalized discounted ratio (rRD) computes the difference in the
    proportion of members of the protected group versus the unprotected group
    at top-i and in the over-all population, accumulated for all cutoff points
    in the ranking with a logarithmic discount, and finally normalized wrt. the
    ideal rRD.

    ::

        @inproceedings{YangS2017,
            author = {Yang, Ke and Stoyanovich, Julia},
            title = {Measuring Fairness in Ranked Outputs},
            year = {2017},
            isbn = {9781450352826},
            publisher = {Association for Computing Machinery},
            address = {New York, NY, USA},
            url = {https://doi.org/10.1145/3085504.3085526},
            doi = {10.1145/3085504.3085526},
            booktitle = {Proceedings of the 29th International Conference on
                Scientific and Statistical Database Management},
            articleno = {22},
            numpages = {6},
            location = {Chicago, IL, USA},
            series = {SSDBM '17}
        }
    """

    NAME = "rRD"
    __name__ = "rRD"

    @staticmethod
    def _fraction(numerator: int, denominator: int) -> float:
        if numerator == 0 or denominator == 0:
            return 0
        else:
            return abs(numerator / denominator)

    def unfairness(
            self,
            ranking: tuple[GroupNameType],
            groups: set[GroupNameType],
            group_counts: dict[GroupNameType, int],
            protected_group: GroupNameType,
    ) -> float:
        n = sum(group_counts.values())
        s_plus = group_counts[protected_group]
        s_minus = n - s_plus
        s_frac = self._fraction(s_plus, s_minus)

        metric = 0
        for i in range(1, len(ranking)):
            ranking_i = ranking[:i]
            group_counts_i = self.group_counts(ranking_i, groups)

            s_plus_i = group_counts_i[protected_group]
            s_minus_i = i - s_plus_i
            s_frac_i = self._fraction(s_plus_i, s_minus_i)

            metric += (
                    (1 / log(i + 1, 2)) *
                    abs(s_frac_i - s_frac)
            )

        return metric


NormalizedDiscountedRatio = _NormalizedDiscountedRatio()
rRD = NormalizedDiscountedRatio
register(rRD, ["NormalizedDiscountedRatio"])
