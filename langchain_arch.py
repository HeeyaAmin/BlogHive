# langchain_arch.py
# This file initializes the LangChain architecture: LLM, SQL Database utilities

from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase
import mysql.connector
from dotenv import load_dotenv
import os

# ✅ Load environment variables (optional, if using .env for API Key)
load_dotenv()

# ✅ MySQL Configuration for Local Instance 8889
MYSQL_HOST = "localhost"
MYSQL_PORT = 8889
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DATABASE = "blogs"

# ✅ Connect to MySQL
connection = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
    consume_results=True  # important for LangChain database utilities
)

# ✅ Initialize SQLDatabase object for LangChain
db = SQLDatabase.from_uri(
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# ✅ Setup LangChain LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo-1106",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")  # load from .env (or you can hardcode if needed temporarily)
)

# ✅ Setup LangChain chains
# Basic prompt to generate titles and keywords
template = """Create a valid JSON array structure of three blog titles each having three keywords based on: {input_sentence}."""

prompt = PromptTemplate(
    template=template,
    input_variables=["input_sentence"]
)

# Text generation chain
llm_chain = create_sql_query_chain(llm=llm, db=db)

# Contextual prompt loading for LLM
context = db.get_context()
llm_chain.get_prompts(context)

# Connection closed at the end of file execution (optional, since app stays running)
# connection.close()  (commenting this out for now so that connection stays alive during Flask runtime)
