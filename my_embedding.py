import google.generativeai as genai
import os
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
from uuid import uuid4
from langchain_core.documents import Document


genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_embeddings_gemini(text):
    result = genai.embed_content(
    model="models/text-embedding-004",
    content=text,
    task_type="retrieval_document")
    return result['embedding']

index = faiss.IndexFlatL2(len(generate_embeddings_gemini("hello world")))



def get_vectorstore(text_chunks):
    vector_store = FAISS(
    embedding_function=generate_embeddings_gemini,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
    )

    documents = []
    for text_chunk in text_chunks:
        document = Document(page_content=text_chunk)
        documents.append(document)
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    return vector_store