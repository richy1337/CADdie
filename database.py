from openai import OpenAI
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

data_path = r"data_file"
pc = Pinecone(api_key="pcsk_6bVnaX_vymrJ3iq9vDywksrgmXsiD3pr4aDSRYxaLe7cKGoCUn7HWQhywrD2zDiWz2sVY")

chroma_client = chromadb.PersistentClient(path=chroma_path)
collection = chroma_client.get_or_create_collection(name="nike_pdf")
loader = PyPDFDirectoryLoader(file_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

