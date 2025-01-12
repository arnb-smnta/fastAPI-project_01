from pymongo import MongoClient
from rich.console import Console  # Import Console from rich for colored output
from rich.text import Text  # Import Text for colored text formatting
from dotenv import load_dotenv  
import os


load_dotenv()
console = Console()
try:
    conn = MongoClient(f"{os.getenv("MONGODB_URL")}/{os.getenv("DB_NAME")}")
    conn.list_database_names()
    console.print(Text("MongoDB connection established successfully.", style="green"))  # Green for success
    
except Exception as e:
    console.print(Text(f"Failed to connect to MongoDB: {e}", style="red"))