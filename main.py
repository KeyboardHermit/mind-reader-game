from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import FileResponse

# Mount static folder
# app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

# Temporary word database (later we connect real DB)
word_db = {
    "apple": {
        "questions": {
            "Is it a living thing?": "no",
            "Is it a fruit?": "yes",
            "Is it red?": "yes",
            "Is it used in technology?": "no"
        }
    },
    "cat": {
        "questions": {
            "Is it a living thing?": "yes",
            "Is it a mammal?": "yes",
            "Can it fly?": "no",
            "Is it kept as a pet?": "yes"
        }
    },
    "nothing": {
        "questions": {
            "Is it a physical object?": "no",
            "Can you touch it?": "no",
            "Is it a feeling?": "no",
            "Is it a concept?": "yes"
        }
    }
}

# Request Models
class Answer(BaseModel):
    question: str
    answer: str

class Session(BaseModel):
    answers: List[Answer]

# Routes
@app.get("/start_game")
def start_game():
    questions = [
        "Is it a living thing?",
        "Is it an object?",
        "Is it an emotion?",
        "Can it be eaten?",
        "Is it found in nature?",
        "Is it related to technology?"
    ]
    random.shuffle(questions)
    return {"questions": questions[:5]}  # Return 5 random questions

@app.post("/guess_word")
def guess_word(session: Session):
    user_answers = {ans.question.lower(): ans.answer.lower() for ans in session.answers}

    possible_words = []

    for word, data in word_db.items():
        match = True
        for q, a in user_answers.items():
            if q in (question.lower() for question in data["questions"]):
                expected_answer = data["questions"][q]
                if expected_answer != a:
                    match = False
                    break
        if match:
            possible_words.append(word)

    if not possible_words:
        raise HTTPException(status_code=404, detail="I couldn't guess it 😔. Teach me!")

    guess = random.choice(possible_words)
    return {"guess": guess}

@app.post("/learn_new_word")
def learn_new_word(word: str, questions: dict):
    word_db[word.lower()] = {"questions": questions}
    return {"message": f"Thanks! I learned the word '{word}'."}
