from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_together import Together
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
import os

# Set API key for Together AI
os.environ['TOGETHER_API_KEY'] = 'a0ea6b08429661d592dab6beca8f9f95437f7efdbe794e254f4710d04b75e89d'

# Define prompt template
prompt_template = """This is a chat template and as a Law School Assistant Chatbot, your primary objective is to help 8th–12th grade and law students understand legal and constitutional topics in simple, clear terms.

Your role:
- Use the provided knowledge base for accurate answers.
- Explain rights, duties, IPC sections, and procedures with relatable examples.
- Stick to the context; avoid adding your own questions or assumptions.
- Be brief, clear, and informative.
CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]
"""

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1",
    model_kwargs={"trust_remote_code": True, "revision": "289f532e14dbbbd5a04753fa58739e9ba766f3c7"}
)

# Load FAISS vector store
db = FAISS.load_local("ipc_vector_db", embeddings, allow_dangerous_deserialization=True)
db_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Define the prompt template
prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question', 'chat_history'])

# Initialize the LLM (Together API)
llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    temperature=0.5,
    max_tokens=1024,
    together_api_key=os.environ['TOGETHER_API_KEY']
)

# Memory for conversational retrieval
memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# Create the Conversational Retrieval Chain
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=db_retriever,
    combine_docs_chain_kwargs={'prompt': prompt}
)


def reset_conversation():
    memory.clear()


def chatbot(query):
    user_input = query

    if user_input.lower() == 'reset':
        reset_conversation()
        return("Conversation reset.")

    result = qa.invoke(input=user_input)
    
    return (result['answer'])

