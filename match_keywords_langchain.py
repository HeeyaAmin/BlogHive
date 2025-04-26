# match_keywords_langchain.py
# Handles matching user-selected keywords to blog titles from the database using LangChain

from langchain_arch import llm_chain
import mysql.connector
from langchain_community.utilities import SQLDatabase

# ✅ MySQL Configuration (Local Instance 8889)
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

# ✅ Initialize SQLDatabase object (optional if needed for direct queries)
db = SQLDatabase.from_uri(
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# ----------------------------
# 🔍 Function to match selected keywords to blog titles
# ----------------------------
def match_keywords_userside(selected_keywords):
    matched_titles = []
    description_title = []
    image_urls = []

    # ✅ Create the LangChain query prompt
    response = llm_chain.invoke({
        "question": f"show all the titles from new_blogs_table that have these keywords in it {selected_keywords}"
    })

    # ✅ Execute the generated SQL query
    cursor = connection.cursor()
    cursor.execute(response)
    results = cursor.fetchall()
    connection.commit()

    # ✅ Process results
    for row in results:
        title = row[0]
        matched_titles.append(title)

        # Fetch description for each title
        desc = get_description_for_title(title)
        description_title.append(desc)

        # Fetch image URL for each title
        img_url = get_image_for_title(title)
        image_urls.append(img_url)

    return matched_titles, description_title, image_urls

# ----------------------------
# 📋 Helper function: Get description for a blog title
# ----------------------------
def get_description_for_title(title):
    response = llm_chain.invoke({
        "question": f"for the title '{title}' show the corresponding description from new_blogs_table"
    })

    cursor = connection.cursor()
    cursor.execute(response)
    result = cursor.fetchone()
    connection.commit()

    return result[0] if result else ""

# ----------------------------
# 📋 Helper function: Get image path for a blog title
# ----------------------------
def get_image_for_title(title):
    response = llm_chain.invoke({
        "question": f"get the image_url of the title '{title}' from new_blogs_table"
    })

    cursor = connection.cursor()
    cursor.execute(response)
    result = cursor.fetchone()
    connection.commit()

    return result[0] if result else ""

