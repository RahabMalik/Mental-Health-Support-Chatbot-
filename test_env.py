from dotenv import load_dotenv
import os

print("Current directory:", os.getcwd())
print("Looking for .env at:", os.path.abspath(".env"))

load_dotenv(".env")

print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
