from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

data_path = r"data_file"
chroma_path = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=chroma_path)
collection = chroma_client.get_or_create_collection(name="nike_pdf")
user_query = input("Hello! What would you like help with?\n\n")
loader = PyPDFDirectoryLoader(data_path)
docs = loader.load()
print(f"Loaded {len(docs)} documents from PDF directory.")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=50, length_function=len,
)
chunks = text_splitter.split_documents(docs)

documents = []
metadata = []
ids = []
i = 0

for chunk in chunks:
    documents.append(chunk.page_content)
    ids.append("ID"+str(i))
    metadata.append(chunk.metadata)
    i += 1

collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
)


