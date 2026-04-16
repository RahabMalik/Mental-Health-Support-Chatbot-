import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# For LlamaIndex
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# -------------------------------
# Load environment variables
# -------------------------------
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# -------------------------------
# Setup LangChain LLM for conversation
# -------------------------------
langchain_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=OPENAI_API_KEY
)

# Store conversation memory for each session
session_memory_map = {}

def get_response(session_id: str, user_query: str) -> str:
    """Get chatbot response with session memory."""
    if session_id not in session_memory_map:
        memory = ConversationBufferMemory()
        session_memory_map[session_id] = ConversationChain(
            llm=langchain_llm, memory=memory
        )
    conversation = session_memory_map[session_id]
    return conversation.predict(input=user_query)

# -------------------------------
# Setup Llama-Index for document querying
# -------------------------------
# Configure LlamaIndex settings
Settings.llm = LlamaOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=OPENAI_API_KEY
)

Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key=OPENAI_API_KEY
)

# Initialize document index and query engine
doc_index = None
query_engine = None

def initialize_documents():
    """Initialize document index if data folder exists."""
    global doc_index, query_engine
    
    data_dir = "data"
    if os.path.exists(data_dir) and os.path.isdir(data_dir):
        try:
            # Check if there are any files in the data directory
            files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
            if not files:
                print(f"Warning: No files found in '{data_dir}' directory")
                return
            
            print(f"Loading documents from '{data_dir}' directory...")
            documents = SimpleDirectoryReader(data_dir).load_data()
            
            if documents:
                doc_index = VectorStoreIndex.from_documents(documents)
                query_engine = doc_index.as_query_engine()
                print(f"Successfully loaded {len(documents)} documents")
            else:
                print("No documents were loaded")
                
        except Exception as e:
            print(f"Error loading documents: {e}")
    else:
        print(f"'{data_dir}' directory not found. Document querying will be disabled.")

def query_documents(query: str) -> str:
    """Query documents using Llama-Index."""
    if query_engine is None:
        return ("Document querying is not available. Please ensure:\n"
                "1. A 'data' folder exists in the project directory\n"
                "2. The folder contains readable documents (txt, pdf, docx, etc.)")
    
    try:
        response = query_engine.query(query)
        return str(response)
    except Exception as e:
        return f"Error querying documents: {str(e)}"

# Initialize documents when the module is imported
initialize_documents()