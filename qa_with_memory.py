from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=db.as_retriever(),
    memory=memory
)

# Test it
query = "What is gradient descent?"
result = qa({"question": query})
print(result["answer"])

query2 = "Explain it like I'm 5."  # Follow-up question
result2 = qa({"question": query2})  # Remembers previous chat
print(result2["answer"])
