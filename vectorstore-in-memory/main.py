import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

if __name__ == '__main__':
    print("Hello World")
    pdf_path='/Users/agsen/Desktop/vectorstore-in-memory/file-sample_150kB.pdf'
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10, separator='\n')
    text = text_splitter.split_documents(documents=documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(text, embeddings)
    vectorstore.save_local("faiss_index_react")

    new_vectorstore = FAISS.load_local("faiss_index_react", embeddings, allow_dangerous_deserialization=True)

    retrieval_qa_chat_prompt = hub.pull('langchain-ai/retrieval-qa-chat')
    combine_docs_chain = create_stuff_documents_chain(OpenAI(), retrieval_qa_chat_prompt)
    retrieval_chain = create_retrieval_chain(new_vectorstore.as_retriever(), combine_docs_chain)

    res = retrieval_chain.invoke(input = {"input": "lorem emsum"})

    print(res["answer"])