from fastapi import APIRouter
from services.question_service import get_question
from fastapi import APIRouter, HTTPException
from db.init_db import get_vocab_collection  # Ensure this imports correctly
from datetime import datetime
from services.test_service import save_test_result, calculate_final_level, reset_progress

question_router = APIRouter()

# Define a constant for the number of questions
NUM_OF_QUESTIONS = 5  # Adjust this as needed

# Define level order
levels = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Initialize session
current_user_progress =  {
        "current_level": "A1",
        "questions_answered": 0,
        "correct_answers": 0,
        "wrong_answers": 0,
        "question_history": [],
        "asked_questions": set(),
        "test_start_time": datetime.now()
    }

@question_router.get("/question")
def next_question():
    """
    Get the next question based on user's current level from MongoDB.
    """
    question = get_question(current_user_progress)

    # Append the question to the history and mark it as asked
    current_user_progress["question_history"].append({
        "german_word": question["german_word"],
        "correct_answer": question["correct_answer"],
        "options": question["options"],
        "level": current_user_progress["current_level"],
    })
    current_user_progress["asked_questions"].add(question["german_word"])

    return {
        "question": question["german_word"],
        "options": question["options"],
        "question_level": current_user_progress["current_level"],
        "question_number": len(current_user_progress["question_history"])
    }

@question_router.post("/answer")
def submit_answer(german_word: str, user_answer: str):

    # Find the question in history
    last_question = next((q for q in current_user_progress["question_history"] if q["german_word"] == german_word), None)

    if not last_question:
        raise HTTPException(status_code=400, detail="Invalid question")

    # Check if the answer is correct
    correct_answer = last_question["correct_answer"]
    current_level = last_question["level"]

    # Adjust difficulty factor based on answer correctness
    difficulty_factor = last_question.get("difficulty_factor", 3)

    if user_answer == correct_answer:
        current_user_progress["correct_answers"] += 1
        
        # Decrease difficulty factor (correct answer, less likely to repeat)
        if difficulty_factor > 1:
            last_question["difficulty_factor"] = difficulty_factor - 1
        
        # Optionally increase the user's level
        current_level_index = levels.index(current_level)
        if current_level_index < len(levels) - 1:
            current_user_progress["current_level"] = levels[current_level_index + 1]
    else:
        current_user_progress["wrong_answers"] += 1
        
        # Increase difficulty factor (wrong answer, more likely to repeat)
        if difficulty_factor < 5:
            last_question["difficulty_factor"] = difficulty_factor + 1
        
        # Optionally decrease the user's level
        current_level_index = levels.index(current_level)
        if current_level_index > 0:
            current_user_progress["current_level"] = levels[current_level_index - 1]

    current_user_progress["questions_answered"] += 1

    # Get all options (both correct and incorrect)
    all_options = last_question["options"]

    # Create a mapping of all options (English words) to their German equivalents
    option_to_german_mapping = {}
    for option in all_options:
        # Find the German word for each option
        german_word_for_option = None
        # Assuming `get_vocab_collection` returns a collection to query
        collection = get_vocab_collection()  
        match = collection.find_one({"meaning": option})
        if match:
            german_word_for_option = match['word']

        # Add the option and its corresponding German word to the mapping
        if german_word_for_option:
            option_to_german_mapping[option] = german_word_for_option

    # Ensure the correct answer is included in the mapping
    option_to_german_mapping[correct_answer] = german_word

    # If the number of questions exceeds the limit, return the completion message
    if current_user_progress["questions_answered"] >= NUM_OF_QUESTIONS:
        return {"message": "Test completed. Please check your level.", "test_status": "completed"}

    return {
        "message": "Answer submitted",
        "next_level": current_user_progress["current_level"],
        "correct_answer": correct_answer,
        "all_option_answers": option_to_german_mapping,  # Return all options with their corresponding German words
        "difficulty_factor": last_question["difficulty_factor"],  # Return updated difficulty factor for debugging
        "questions_answered": current_user_progress["questions_answered"]  # Track number of questions answered
    }

@question_router.get("/result")
def get_final_level():
    """
    Get the final level based on user's performance and save the result.
    """
    test_level = calculate_final_level(current_user_progress, NUM_OF_QUESTIONS)
    save_test_result(current_user_progress, test_level)
    
    return {
        "level": test_level,
        "correct_answers": current_user_progress["correct_answers"],
        "wrong_answers": current_user_progress["wrong_answers"],
        "questions_answered": current_user_progress["questions_answered"]
    }

@question_router.post("/reset")
def reset_test():
    """
    Reset the test progress.
    """
    current_user_progress = reset_progress()
    return {"message": "Test progress reset."}