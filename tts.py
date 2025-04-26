# tts.py
# Handles generating blog audio in English, French, and German using OpenAI TTS

import warnings
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import mysql.connector
from langchain_community.utilities import SQLDatabase
from openai import OpenAI
from langchain_arch import llm_chain

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

db = SQLDatabase.from_uri(
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# ✅ OpenAI Client
client = OpenAI()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=1)

# ----------------------------
# 🎧 Generate Audio for Blog Description
# ----------------------------
def get_audios(description, blog_id):
    """Generate audios for English, French, and German"""

    # English
    prompt_en = PromptTemplate(
        template=f"generate audio content for this blog description: {description}",
        input_variables=["description"]
    )
    llm_chain_en = LLMChain(prompt=prompt_en, llm=llm)
    response_en = llm_chain_en.invoke({"description": description})['text']

    # French
    prompt_fr = PromptTemplate(
        template=f"translate the following blog description to French: {description}",
        input_variables=["description"]
    )
    llm_chain_fr = LLMChain(prompt=prompt_fr, llm=llm)
    response_fr = llm_chain_fr.invoke({"description": description})['text']

    # German
    prompt_ge = PromptTemplate(
        template=f"translate the following blog description to German: {description}",
        input_variables=["description"]
    )
    llm_chain_ge = LLMChain(prompt=prompt_ge, llm=llm)
    response_ge = llm_chain_ge.invoke({"description": description})['text']

    # ✅ Use OpenAI TTS (text-to-speech)
    audio_en = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=response_en
    )
    audio_fr = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=response_fr
    )
    audio_ge = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=response_ge
    )

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Save files locally
    path_en = f"static/audio/audio_english_{blog_id}.mp3"
    path_fr = f"static/audio/audio_french_{blog_id}.mp3"
    path_ge = f"static/audio/audio_german_{blog_id}.mp3"

    audio_en.stream_to_file(path_en)
    audio_fr.stream_to_file(path_fr)
    audio_ge.stream_to_file(path_ge)

    # ✅ Update audio_table in MySQL
    response_update = llm_chain.invoke({
        "question": f"UPDATE audio_table SET english_audio='{path_en}', french_audio='{path_fr}', german_audio='{path_ge}' WHERE blog_id={blog_id}"
    })
    cursor = connection.cursor()
    cursor.execute(response_update)
    connection.commit()

    return path_en, path_fr, path_ge

# ----------------------------
# 📋 Get Blog Description and Blog ID
# ----------------------------
def get_desc_and_id(title):
    """Fetch blog_id and description for a given blog title"""

    response = llm_chain.invoke({
        "question": f"SELECT blog_id, description FROM new_blogs_table WHERE title='{title}'"
    })

    cursor = connection.cursor()
    cursor.execute(response)
    result = cursor.fetchone()
    connection.commit()

    if result:
        blog_id, description = result
        return blog_id, description
    else:
        return None, None

# ----------------------------
# 🎯 Main function: Get or Generate Audios
# ----------------------------
def audios(title):
    """Main function called from app.py to either fetch or generate blog audios"""

    # Check if audio already exists
    response_check = llm_chain.invoke({
        "question": f"SELECT english_audio, french_audio, german_audio FROM audio_table WHERE title='{title}'"
    })

    cursor = connection.cursor()
    cursor.execute(response_check)
    match = cursor.fetchone()
    connection.commit()

    if match:
        # Audio already exists
        return match[0], match[1], match[2]
    else:
        # Need to generate audio
        blog_id, description = get_desc_and_id(title)

        if blog_id is not None and description is not None:
            # Insert initial row into audio_table with blog_id and title
            insert_query = f"INSERT INTO audio_table (blog_id, title) VALUES ({blog_id}, '{title}')"
            cursor.execute(insert_query)
            connection.commit()

            return get_audios(description, blog_id)
        else:
            return "", "", ""

