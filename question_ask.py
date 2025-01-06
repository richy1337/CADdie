import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

data_path = r"data_file"
chroma_path = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=chroma_path)
collection = chroma_client.get_or_create_collection(name="nike_pdf")
user_query = input("Hello! What would you like help with?\n\n")

results = collection.query(
    query_texts=[user_query],
    n_results = 1
)

if not results['documents'] or len(results['documents'][0]) == 0:
    print("No relevant documents found. Please check the data")
    exit()                                

client = OpenAI()
system_prompt = """
You are a helpful assistant. You answer questions about the nike annual report. But you only answer
based on the knowledge I'm providing you. Don't use your internal knowledge and don't make anything up. If you don't
know the answer, just reply with: I don't have the answer to this question, please ask a member of MDL

---------------------

The data:

"""+str(results['documents'])+"""
"""

response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_query}
    ]
)

print("\n--------------------\n")
print(response.choices[0].message.content)