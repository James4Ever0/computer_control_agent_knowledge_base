import os
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
from embedchain import App

# docs: https://docs.embedchain.ai/

# load llm configuration from config.yaml file
app = App.from_config(config_path="embedchain_config.yaml")

# Create a bot instance
os.environ["OPENAI_API_KEY"] = "dummykey"

# Embed online resources
app.add("https://baai-agents.github.io/Cradle/")

# app.add("https://en.wikipedia.org/wiki/Elon_Musk")
# app.add("https://www.forbes.com/profile/elon-musk")

# Query the app
answer:str = app.query("How is Cradle different from other projects?")
# answer = app.query("How many companies does Elon Musk run and name those?")
# Answer: Elon Musk currently runs several companies. As of my knowledge, he is the CEO and lead designer of SpaceX, the CEO and product architect of Tesla, Inc., the CEO and founder of Neuralink, and the CEO and founder of The Boring Company. However, please note that this information may change over time, so it's always good to verify the latest updates.

# print("[*] Answer:")
# print(answer)