import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI as LlamaOpenAI

# Initialize LLM
llama_llm = LlamaOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Set global LLM
Settings.llm = llama_llm

# Load documents
try:
    documents = SimpleDirectoryReader("data").load_data()
    
    # Build vector store index
    index = VectorStoreIndex.from_documents(documents)
    
    # Create query engine
    query_engine = index.as_query_engine()
    
except Exception as e:
    print(f"Warning: Could not load documents: {e}")
    query_engine = None

def query_documents(query: str) -> str:
    """Query documents using the vector store index."""
    if query_engine is None:
        return "Document querying is not available. Please ensure the 'data' folder exists with documents."
    
    try:
        response = query_engine.query(query)
        return str(response)
    except Exception as e:
        return f"Error querying documents: {str(e)}"