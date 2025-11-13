from typing import Tuple

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.twitter import scrape_twitter_acc
from output_parsers import summary_parser, Summary

def ice_break_with (name : str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name = name)
    linkedin_data = scrape_linkedin_profile(linkedin_username)
    twitter_username = twitter_lookup_agent(name = name)
    tweets =  scrape_twitter_acc(username = twitter_username, mock=True)
    summary_template = """
       given the information about a person from LinkedIn {information},
       and twitter posts {twitter_posts} I want you to create:
       1. A short summary
       2. 2 interesting facts about them
       
       Use both information from twitter and linkedin
       \n{format_instructions}
       """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"], template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )
    llm = ChatOllama(model="llama3")
    #chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser
    res : Summary = chain.invoke(input = {"information" : linkedin_data, "twitter_posts" : tweets})
    return res, linkedin_data.get("photoUrl")

if __name__ == "__main__":
   load_dotenv()
   print("Ice breaker enter")
   ice_break_with(name = "Eden Marco")
