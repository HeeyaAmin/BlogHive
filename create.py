# create.py
# This script generates blog titles, keywords, descriptions, and images
# and saves them into the MySQL database.

from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.utilities import SQLDatabase
import mysql.connector
from openai import OpenAI
import json
import urllib.request
from dotenv import load_dotenv
import os

# ✅ Load environment variables (if needed for OpenAI key)
load_dotenv()

# ✅ MySQL Configuration
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
    consume_results=True
)

# ✅ Initialize SQLDatabase
db = SQLDatabase.from_uri(
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# ✅ OpenAI Client
client = OpenAI()

# ✅ Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=1,
    openai_api_key=os.getenv("OPENAI_API_KEY")  # or hardcode temporarily
)

# ✅ Create LangChain SQL query chain
llm_chain = create_sql_query_chain(llm=llm, db=db)

# ✅ Context loading (optional)
context = db.get_context()
llm_chain.get_prompts(context)


# ----------------------------
# 🎯 Function: Generate Titles and Keywords
# ----------------------------
def generate_titles_and_keywords(category_name):
    """Generates two blog titles and related keywords for a given category."""

    prompt_template = f"""
    In the category {category_name}, generate two creative blog titles along with 3-4 related keywords each.
    Provide output in the following JSON format:
    {{
        "blogs": [
            {{
                "title": "Title 1",
                "keywords": ["keyword1", "keyword2", "keyword3"]
            }},
            {{
                "title": "Title 2",
                "keywords": ["keyword1", "keyword2", "keyword3"]
            }}
        ]
    }}
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["category_name"])
    chain = LLMChain(prompt=prompt, llm=llm)
    response = chain.invoke({"category_name": category_name})

    json_data = json.loads(response['text'])
    return json_data['blogs']


# ----------------------------
# 📝 Insert Keywords into keywords table
# ----------------------------
def insert_keywords_into_db(keywords):
    """Insert each keyword into the keywords table."""
    cursor = connection.cursor()
    for keyword in keywords:
        try:
            cursor.execute("INSERT IGNORE INTO keywords (keyword_name) VALUES (%s)", (keyword,))
        except Exception as e:
            print("Error inserting keyword:", e)
    connection.commit()
    cursor.close()


# ----------------------------
# ✍️ Generate Blog Content and Image
# ----------------------------
def generate_blog_content_and_image(title, keywords):
    """Generates blog description and image for a given title and keywords."""

    # Generate Blog Description
    prompt_desc = f"Write a detailed, engaging blog article based on the title '{title}' and keywords {keywords}."
    desc_prompt = PromptTemplate(template=prompt_desc, input_variables=["title", "keywords"])
    desc_chain = LLMChain(prompt=desc_prompt, llm=llm)
    description_response = desc_chain.invoke({"title": title, "keywords": keywords})
    description = description_response['text']

    # Generate Blog Image
    prompt_image = f"Create an image that visually represents the concept of '{title}' and {keywords}."
    response_img = client.images.generate(
        model="dall-e-2",
        prompt=prompt_image,
        size="512x512",
        quality="standard",
        n=1
    )
    image_url = response_img.data[0].url

    # Save the image locally
    image_filename = f"static/blog_image/{title.replace(' ', '_')}.png"
    urllib.request.urlretrieve(image_url, image_filename)

    return description, image_filename


# ----------------------------
# 📥 Insert Blog into new_blogs_table
# ----------------------------
def insert_blog_into_db(title, keywords, description, image_path):
    """Insert a new blog entry into new_blogs_table."""
    cursor = connection.cursor()
    keywords_combined = ', '.join(keywords)

    try:
        cursor.execute(
            "INSERT INTO new_blogs_table (title, keywords, description, image_url) VALUES (%s, %s, %s, %s)",
            (title, keywords_combined, description, image_path)
        )
        connection.commit()
    except Exception as e:
        print("Error inserting blog:", e)
    finally:
        cursor.close()


# ----------------------------
# 🏁 Main Function: Run All
# ----------------------------
def run_blog_generation_flow(category_name):
    """Complete flow: generate blogs, keywords, description, image and insert into database."""

    blogs = generate_titles_and_keywords(category_name)

    all_keywords = []

    for blog in blogs:
        title = blog['title']
        keywords = blog['keywords']

        all_keywords.extend(keywords)

        description, image_path = generate_blog_content_and_image(title, keywords)
        insert_blog_into_db(title, keywords, description, image_path)

    insert_keywords_into_db(all_keywords)


# ----------------------------
# 🏃‍♂️ If running directly
# ----------------------------
if __name__ == "__main__":
    category = "travel"  # Example starting category
    run_blog_generation_flow(category)

    print("Blog generation completed successfully!")

