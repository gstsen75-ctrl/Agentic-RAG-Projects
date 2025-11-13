from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature = 0)

raw_prompt = hub.pull("rlm/rag-prompt")

# Rebuild it as a v2-compatible ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(raw_prompt.messages)



generation_chain = prompt | llm | StrOutputParser()

