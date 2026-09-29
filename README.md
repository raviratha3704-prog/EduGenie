# EduGenie

EduGenie is an AI-powered educational learning assistant.

It provides:

- AI Question Answering
- Concept Explanation
- Quiz Generation
- Text Summarization
- Personalized Learning Paths

The backend is built with FastAPI and the AI features use Google Gemini.

A local Hugging Face model can also be used for concept explanations.

---

# Project Structure

```text
EduGenie/
│
├── main.py
├── config.py
├── models.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── app.js
│
└── tests/
    └── test_api.py