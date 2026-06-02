from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper


def get_arxiv_tool():

    arxiv = ArxivAPIWrapper(
        top_k_results = 1,
        doc_content_chars_max = 300
    )

    tool = ArxivQueryRun(api_wrapper = arxiv)

    tool.name = "arxiv_search"
    tool.description = "Search research papers from Arxiv"

    return tool