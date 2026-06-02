from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def get_wikipedia_tool():

    wiki_api = WikipediaAPIWrapper(
        top_k_results = 2,
        doc_content_chars_max = 1200
    )

    wiki_tool = WikipediaQueryRun(api_wrapper = wiki_api)

    return wiki_tool
