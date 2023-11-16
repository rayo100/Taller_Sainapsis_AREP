import os

from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI

import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools import tool
from langchain.vectorstores.pinecone import Pinecone
from load_files import load_files

# Conección a la base de datos de PineCone
pinecone.init(api_key="709f5a01-aa44-4eb6-8ad2-e81bcae0afc0", environment="gcp-starter")
##pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENVIRONMENT'))
# Objeto que convierte el texto en un vector de dimensión 1536
embeddings = OpenAIEmbeddings()
texts = load_files()
##
data = Pinecone.from_texts(texts=texts, embedding=embeddings, index_name="arep-ia")


@tool("SayHello", return_direct=True)
def say_hello(name: str) -> str:
    """
    Answer when someone say hello
    :param name:
    :return:
    """
    return "Hello " + name + " My name is Sainapsis"


@tool("Files", return_direct=True)
def files(program: str) -> str:
    """
    Answer a query from ECI programs
    :param name:
    :return:
    """
    file_search = Pinecone.from_existing_index("vectordb", embeddings)
    file = file_search.similarity_search(program)
    return file.pop().page_content


def main():
    llm = ChatOpenAI(temperature=0)
    tools = [
        say_hello,
        files
    ]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    print(agent.run("Hello!, My name is Cesar"))
    print(agent.run("ingeniería  sistemas"))


if __name__ == '__main__':
    main()
