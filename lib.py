import os
from secret import OLLAMA_EXTERNAL_BASEURL
from typing import DefaultDict

os.environ["OLLAMA_HOST"] = OLLAMA_EXTERNAL_BASEURL
os.environ["OPENAI_API_KEY"] = "dummykey"
import embedchain

# docs: https://docs.embedchain.ai/
def print_calling_params(args, kwargs):
    print("[*] Args:", args)
    print("[*] Kwargs:", kwargs)


# load llm configuration from config.yaml file
class EmbedApp:
    def __init__(self, config_path="secret.embedchain_config.yaml"):
        self.app = embedchain.App.from_config(config_path=config_path)

    def add(self, *args, **kwargs):
        print("[*] Adding to index:")
        print_calling_params(args, kwargs)
        return self.app.add(*args, **kwargs)

    def query(self, *args, **kwargs) -> str:
        print("[*] Performing query:")
        print_calling_params(args, kwargs)
        return self.app.query(*args, **kwargs)

    def get_all_data_from_chromadb(self) -> dict:
        ret = self.app.db.get()
        return ret

    def check_url_is_added(self, url: str) -> bool:
        embed_data = self.get_all_data_from_chromadb()
        for metadata in embed_data["metadatas"]:
            added_url = metadata["url"]
            if url == added_url:
                return True
        return False

    def get_all_document_chunks(self) -> list[dict[str, str]]:
        ret = []
        embed_data = self.get_all_data_from_chromadb()
        for metadata, document in zip(embed_data["metadatas"], embed_data["documents"]):
            url = metadata["url"]
            ret.append(dict(url=url, document=document))
        return ret

    def get_all_documents_by_url(self) -> dict[str, list[str]]:
        ret = DefaultDict(list)
        document_chunks = self.get_all_document_chunks()
        for it in document_chunks:
            ret[it["url"]].append(it["document"])
        return dict(ret)
