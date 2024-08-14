url = "https://baai-agents.github.io/Cradle/"

# ref: https://docs.llamaindex.ai/en/stable/examples/data_connectors/WebPageDemo/
# TODO: download and use spider.rs library to comprehend web pages
# https://docs.rs/spider/latest/spider/

from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
from llama_index.llms.ollama import Ollama

from secret import OLLAMA_EXTERNAL_BASEURL

documents = SimpleWebPageReader(html_to_text=True).load_data(
    [url]
)
index = SummaryIndex.from_documents(documents)
# set Logging to DEBUG for more detailed outputs
llm = Ollama(model="mistral:v0.3", request_timeout=120.0, base_url = OLLAMA_EXTERNAL_BASEURL)
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("What is special about Cradle?")
print("[*] Response:")
print(response)