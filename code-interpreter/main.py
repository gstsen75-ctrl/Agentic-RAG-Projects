from dotenv import load_dotenv
from langchain import hub
from langchain_core.tools import Tool
from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool

load_dotenv()


def main():
    print("Start...")
    instructions = """You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute Python code.
    If you encounter an error, debug your code and try again.
    Only use the output of your code to answer questions.
    You might know the answer without running any code, but you should still run the code to get the final answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions = instructions)
    tools = [PythonREPLTool()]

    agent = create_react_agent(
        prompt = prompt,
        tools = tools,
        llm = ChatOpenAI(temperature=0, model="gpt-4-turbo"),
    )

    python_agent_executor = AgentExecutor(agent = agent, tools = tools, verbose = True)


    csv_agent_executor : AgentExecutor = create_csv_agent(
        llm = ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        path = "episode_info.csv",
        verbose = True,
        allow_dangerous_code=True,
    )

    tools = [
        Tool(
            name = "Python Agent",
            func = python_agent_executor.invoke,
            description = """Useful when you need to transform natural language to python and execute python code,
            returning the results of the code execution.
            DOES NOT ACCEPT CODE AS INPUT""",
        ),

        Tool(
            name = "CSV Agent",
            func = csv_agent_executor.invoke,
            description = """Useful when you need to answer questions regarding the episode_info.csv file.
            Takes an entire question as input and returns the answer after running some pandas calculations."""

        ),
    ]
    prompt = base_prompt.partial(instructions = "")
    grand_agent = create_react_agent(
        prompt = prompt,
        tools = tools,
        llm = ChatOpenAI(temperature=0, model="gpt-4-turbo"),
    )
    grand_agent_executor = AgentExecutor(agent = grand_agent, tools = tools, verbose = True)

    print(grand_agent_executor.invoke({"input": "which season has the most episodes?"}))


if __name__ == "__main__":
    main()
