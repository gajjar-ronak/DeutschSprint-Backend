from fastapi import HTTPException
from datetime import datetime
from db.init_db import get_collection

# Save test results to MongoDB
def save_test_result(user_progress, test_level):
    test_result = {
        "test_start_time": user_progress["test_start_time"],
        "test_end_time": datetime.now(),
        "correct_answers": user_progress["correct_answers"],
        "wrong_answers": user_progress["wrong_answers"],
        "questions_answered": user_progress["questions_answered"],
        "final_level": test_level,
        "question_history": user_progress["question_history"]
    }
    get_collection("test_results").insert_one(test_result)

# Calculate final level based on user's performance
def calculate_final_level(user_progress, num_of_questions):
    if user_progress["questions_answered"] < num_of_questions:
        raise HTTPException(status_code=400, detail="Test not completed yet.")

    level_scores = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
    total_score = sum(level_scores[q["level"]] for q in user_progress["question_history"])
    average_score = total_score / len(user_progress["question_history"])

    if average_score >= 5:
        return "C2"
    elif average_score >= 4:
        return "C1"
    elif average_score >= 3:
        return "B2"
    elif average_score >= 2:
        return "B1"
    elif average_score >= 1:
        return "A2"
    else:
        return "A1"
    
# Reset test progress
def reset_progress():
    return {
        "level": "A1",
        "questions_answered": 0,
        "correct_answers": 0,
        "wrong_answers": 0,
        "question_history": [],
        "asked_questions": set(),
        "test_start_time": datetime.now()
    }