import os
from secret import OLLAMA_EXTERNAL_BASEURL

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
