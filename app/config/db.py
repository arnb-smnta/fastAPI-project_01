from pymongo import MongoClient
from rich.console import Console
from rich.text import Text
from dotenv import load_dotenv  
import os

# Initialize variables
load_dotenv()
console = Console()
conn = None  # Define conn in global scope

try:
    # Create MongoDB connection
    conn = MongoClient(os.getenv("MONGODB_URL"))
    conn.list_database_names()
    console.print(Text("MongoDB connection established successfully.", style="green"))
    
except Exception as e:
    console.print(Text(f"Failed to connect to MongoDB: {e}", style="red"))

# Explicitly export conn
__all__ = ['conn']