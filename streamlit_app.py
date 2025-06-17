import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS

import os
from dotenv import load_dotenv
load_dotenv()

# Load FAISS vector DB
embeddings = OpenAIEmbeddings()
db = FAISS.load_local("faiss_index", embeddings)

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=db.as_retriever(),
    memory=memory
)

# Streamlit UI
st.title("Virtual TA (with Memory)")
user_input = st.text_input("Ask a question:")
if user_input:
    result = qa({"question": user_input})
    st.write(result["answer"])
