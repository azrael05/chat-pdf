import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".envs")
from chunker import chunk_text
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
# pdf_reader = PDFReader()
import google.generativeai as genai
from my_embedding import get_vectorstore
from pdf_reader import PDFReader
from chunker import chunk_text
from langchain_google_genai import ChatGoogleGenerativeAI
def get_conversation_chain(vectorstore):    
    llm = ChatGoogleGenerativeAI(model=os.environ["MODEL_NAME"])
    # llm = ChatVertexAI(model="gemini-1.5-flash")
    # llm = ChatOpenAI(model="gpt-4o-mini")
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def chat(vectorstore, question):
    results = vectorstore.similarity_search(
    question,
    k=4,
    # filter={"source": "tweet"},
    )

    text = ""
    for res in results:
        print(res)
        text += res.page_content + ".\n"
    prompt = f"{text} \nUse the information above and answer the question {question}"
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print(response.text)
    st.write(response.text)
    # return response.text


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)
        # chat(vectorstore, user_question)
    pdf_reader = PDFReader()
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = pdf_reader.read(pdf_docs)
                # get the text chunks
                text_chunks = chunk_text(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)
                # if user_question:
                #         chat(vectorstore, user_question)
                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()