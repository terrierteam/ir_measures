from typing import Optional
from urllib.parse import quote
import os
import json
import requests
import bibtexparser
import gzip
from pylatexenc.latex2text import LatexNodes2Text
from docutils import nodes
from docutils.parsers.rst import Directive
from pyparsing import ParseException
from sphinx.util import logging

latex_converter = LatexNodes2Text()
logger = logging.getLogger(__name__)

# Cache file to store BibTeX entries
CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "dblp_cache.json.gz")


def load_dblp_cache():
    """Load the cache from the file, or create a new one if it doesn't exist."""
    if os.path.exists(CACHE_FILE):
        with gzip.open(CACHE_FILE, "rt") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

dblp_cache = load_dblp_cache()

def save_dblp_cache():
    """Save the cache to the file."""
    with gzip.open(CACHE_FILE, "wt") as f:
        json.dump(dblp_cache, f, indent=4)


class CiteNode(nodes.General, nodes.Element):
    """Custom node to render DBLP citation."""
    def __init__(self, citation_id, citation, link, bibtex):
        super().__init__()
        self['id'] = citation_id
        self['citation'] = citation
        self['link'] = link
        self['bibtex'] = bibtex


class CiteDirective(Directive):
    required_arguments = 1
    has_content = True
    option_spec = {'citation': str, 'link': str, 'blbtex': str}

    def run(self):
        # Create a custom node to hold the BibTeX content and display data
        node = CiteNode(
            self.get_citation_id(),
            self.get_citation(),
            self.get_link(),
            self.get_bibtex()
        )

        # in the future, could store citation information in self.state.document.settings.env
        # to generate a bibliography page.

        return [node]

    def get_citation_id(self) -> str:
        return self.arguments[0]

    def get_citation(self) -> Optional[str]:
        return self.options.get('citation')

    def get_link(self) -> Optional[str]:
        return self.options.get('link')

    def get_bibtex(self) -> Optional[str]:
        if self.content:
            return '\n'.join(self.content)
        return None


class CiteDblpDirective(CiteDirective):
    """Directive to fetch and display a citation from DBLP using a DBLP ID."""
    has_content = False
    required_arguments = 1  # The DBLP ID must be provided as an argument.

    def run(self):
        dblp_id = self.arguments[0]
        record_url = f"https://dblp.org/rec/{quote(dblp_id)}"
        cached = dblp_cache.get(dblp_id)
        try:
            bibtex = cached
            if bibtex is None:
                bibtex = []
                for variant in (0, 1):
                    response = requests.get(f"{record_url}.bib?param={variant}", timeout=10)
                    response.raise_for_status()
                    bibtex.append(response.text)
            short_entries, full_entries = [bibtexparser.loads(entry).entries for entry in bibtex]
            if not short_entries or not full_entries:
                raise ValueError("DBLP response contains no BibTeX entries")
        except (requests.RequestException, ParseException, KeyError, ValueError) as exc:
            logger.info("Using a DBLP record link for %s because BibTeX is unavailable: %s", dblp_id, exc)
            return [CiteNode(
                self.get_citation_id(),
                super().get_citation() or f"DBLP: {quote(dblp_id)}",
                super().get_link() or record_url,
                None,
            )]

        if cached is None:
            dblp_cache[dblp_id] = bibtex
            save_dblp_cache()
        self.short_entry = short_entries[0]
        self.full_entry = full_entries[0]
        self.bibtex_entry_full = bibtex[1]
        return super().run()

    def get_citation_id(self) -> str:
        return 'dblp:' + self.arguments[0]

    def get_citation(self) -> Optional[str]:
        citation = super().get_citation()
        if citation is not None:
            return citation
        res = self.short_entry
        authors = latex_converter.latex_to_text(res.get('author', ''))
        if authors:
            authors = authors.split(' and\n')
            if len(authors) > 2:
                authors = authors[0].split()[-1] + ' et al'
            elif len(authors) == 2:
                authors = authors[0].split()[-1] + ' and ' + authors[1].split()[-1]
            else:
                authors = authors[0].split()[-1]
        title = latex_converter.latex_to_text(res.get('title', ''))
        year = latex_converter.latex_to_text(res.get('year', ''))
        if 'journal' in res and res['journal'] == 'CoRR':
            citation = f'{authors}. {title}. arXiv {year}.'
        elif 'journal' in res:
            journal = latex_converter.latex_to_text(res['journal'])
            citation = f'{authors}. {title}. {journal} {year}.'
        elif 'booktitle' in res:
            conf = latex_converter.latex_to_text(res['booktitle'])
            citation = f'{authors}. {title}. {conf} {year}.'
        else:
            citation = f'{authors}. {title}. {year}.'
        return citation

    def get_link(self) -> Optional[str]:
        link = super().get_link()
        if link is not None:
            return link
        res = self.full_entry
        return latex_converter.latex_to_text(res.get('url', ''))

    def get_bibtex(self) -> Optional[str]:
        bibtex = super().get_bibtex()
        if bibtex is not None:
            return bibtex
        return self.bibtex_entry_full


def visit_cite_node_html(self, node):
    """HTML visitor to render the DblpNode."""
    citation = node['citation']
    link = node['link']
    bibtex = node['bibtex']

    if link:
        link_html = f' <a href="{link}" target="_blank">[link]</a>'
    else:
        link_html = ''

    if bibtex:
        body_html = f'''
<details class="dblp-citation">
  <summary><b>{citation}</b>{link_html}</summary>
  <pre class="bibtex">{bibtex.strip()}</pre>
</details>
'''
    else:
        body_html = f'<p><b>{citation}</b>{link_html}</p>'

    self.body.append(f'''
<div class="admonition">
  <p class="admonition-title">Citation</p>
  {body_html}
</div>
    ''')


def depart_cite_node_html(self, node):
    """HTML departure for DblpNode."""
    pass


def setup(app):
    app.add_node(CiteNode, html=(visit_cite_node_html, depart_cite_node_html))
    app.add_directive('cite', CiteDirective)
    app.add_directive('cite.dblp', CiteDblpDirective)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
