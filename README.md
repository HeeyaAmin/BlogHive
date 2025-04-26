
# BlogHive 🐝

An AI-powered blog template generator where users can select interests (keywords) and receive blog templates — complete with title, description, image, and multilingual audio files!

Built using **Flask**, **MySQL**, **LangChain**, and **OpenAI APIs**.

---

## 📋 Features

- User Signup/Login
- Select Interests from Keyword Buttons
- Generate Blog Templates (Title, Description, Image)
- View Blog Templates in a Carousel
- Star Favorite Blogs (Save for Audio Download)
- Multilingual Audio Generation (English, French, German)
- Download Audio Files (MP3)

---

## 🛠️ Tech Stack

- **Backend:** Flask, LangChain, OpenAI API
- **Database:** MySQL (Local Instance, port 8889)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **APIs:** 
  - ChatOpenAI (for titles, descriptions)
  - DALL·E 2 (for image generation)
  - OpenAI TTS (for multilingual blog audio)

---

## 📁 Project Structure

BlogHive/ │ ├── app.py ├── create.py ├── langchain_arch.py ├── match_keywords_langchain.py ├── tts.py ├── requirements.txt ├── .env (store your secret keys here, not public) │ ├── templates/ │ ├── login.html │ ├── signup.html │ └── indexo.html │ ├── static/ │ ├── script.js │ ├── styles/ │ │ ├── login_styles.css │ │ ├── signup_styles.css │ │ └── styles_index.css │ ├── blog_image/ (generated blog images) │ └── audio/ (generated audio files) │ └── README.md

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/BlogHive.git
cd BlogHive
```

2. Set up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Create a .env file

In your project root:
```bash

dotenv
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
SECRET_KEY=your_flask_secret_key_here
(Never share your .env file publicly.)
```

5. Set Up MySQL Database
Run the provided SQL script to create:
blogs database

user, keywords, new_blogs_table, audio_table tables

Configure root/root user on port 8889 (adjust if needed).

6. Run the Flask App
```bash
python app.py
```
App will be available at:

```
http://localhost:5000/
```
🚀 Usage
Sign up or log in.

Select interests (keywords) from the displayed buttons.

Submit your selection to view matching blog templates.

Star your favorite blogs to save them.

Click on the blog title to open a modal and download multilingual audio versions.

📸 Screenshots

(Add your screenshots after project is running.)

🧠 Future Improvements
Allow users to enter custom prompts along with keywords

Personalize blog generation based on user history

Save user downloads in database for history tracking

Deployment to Vercel / Render / Fly.io

🧑‍💻 Author:

Heeya Amin

Data Scientist & Software Developer







