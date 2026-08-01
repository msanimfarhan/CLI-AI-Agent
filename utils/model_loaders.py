import os 
from dotenv import load_dotenv 
from typing import Literal,Optional,Any 
from pydantic import BaseModel,Field 
from utils.config_loader import load_config 
from langchain_groq import ChatGroq 
from langchain_openai import ChatOpenAi 


class ConfigLoader:

    def __init__(self):
        print(f"Loading config....")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader:
    model_provider:Literal["groq","openai"] = "groq"
    config: Optional[ConfigLoader] =Field(default=None,exclude=True)

    def model_post_init(self,__content:Any)->None:
        self.config= ConfigLoader()

    class Config:
        arbitary_types_allowed =True 

    def load_llm(self):
        """load and return model"""

        print("LLM Loading.....")
        print(f"Loading model from provider: {self.model_provider} ")

        if self.model_provider == "groq":
            print("'Loading LLM from Grow........")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(model=model_name,api_key=groq_api_key)
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..........")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAi(model_name="o4-mini",api_key=openai_api_key)

        return llm