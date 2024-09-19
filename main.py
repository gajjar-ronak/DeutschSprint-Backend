from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import random
from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB setup
MONGO_URL= os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.deutsch_sprint
performance_collection = db.performance_logs

# Initialize FastAPI
app = FastAPI()


# total number of questions 
total_questions = 20

# Load questions from Excel
def load_questions():
    file_path = './data/verbs.xlsx'
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    questions = []
    
    # Iterate over each sheet in the Excel file
    for sheet_name, sheet_data in all_sheets.items():
        for index, row in sheet_data.iterrows():
            german_word = row['German']
            english_meaning = row['English']
            
            questions.append({
                "german": german_word,
                "english": english_meaning
            })
    
    return questions

# This function will return a shuffled list of wrong answers for a given word
def generate_mcq_options(correct_answer, all_questions):
    wrong_answers = random.sample([q['english'] for q in all_questions if q['english'] != correct_answer], 3)
    options = wrong_answers + [correct_answer]
    random.shuffle(options)
    
    return options

# Load all questions from the Excel file (this loads when the app starts)
all_questions = load_questions()

# Endpoint 1: Get total_questions random MCQs
@app.get("/questions")
def get_mcqs():
    if len(all_questions) < total_questions:
        raise HTTPException(status_code=400, detail="Not enough questions available.")
    
    selected_questions = random.sample(all_questions, total_questions)
    
    mcqs = []
    for idx, question in enumerate(selected_questions):
        options = generate_mcq_options(question["english"], all_questions)
        mcqs.append({
            "question_number": idx + 1,
            "german_word": question["german"],
            "options": options
        })
    
    return {"questions": mcqs}

# Model to capture the submitted answers
class AnswerSubmission(BaseModel):
    answers: dict  # Question number as key, selected answer as value

# Endpoint 2: Submit answers and log the performance
@app.post("/answers")
def submit_answers(submission: AnswerSubmission):
    correct_answers = 0
    wrong_answers = 0

    for question_num, selected_answer in submission.answers.items():
        # Convert the question_num to index
        question_idx = int(question_num) - 1
        if question_idx < len(all_questions):
            correct_answer = all_questions[question_idx]["english"]
            
            if selected_answer == correct_answer:
                correct_answers += 1
            else:
                wrong_answers += 1

    # Log performance to MongoDB
    test_log = {
        "date": datetime.utcnow(),
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "total_questions": total_questions,
        "performance_percentage": (correct_answers / total_questions) * 100
    }
    
    performance_collection.insert_one(test_log)

    return {
        "message": "Test results saved.",
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "performance_percentage": (correct_answers / total_questions) * 100
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)