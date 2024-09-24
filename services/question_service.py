import random
from fastapi import HTTPException
from db.init_db import get_vocab_collection  # Ensure this returns your main vocabulary collection

def get_question(user_progress):
    """
    Fetch a random question from the database based on the user's current level.
    """
    current_level = user_progress["current_level"]

    # Fetch the collection for the vocabulary
    collection = get_vocab_collection()  # Get the main vocabulary collection

    # Get a random question from the collection (excluding already asked questions)
    asked_questions = list(user_progress["asked_questions"])

    # Use MongoDB aggregation to pick a random document based on level
    query = {
        "level": current_level,         # Match the current level
        "German": {"$nin": asked_questions}  # Exclude already asked questions
    }
    pipeline = [
        {"$match": query},           # Match questions that haven't been asked
        {"$sample": {"size": 1}}     # Pick one random question
    ]

    question_docs = list(collection.aggregate(pipeline))

    if not question_docs:
        raise HTTPException(status_code=400, detail="No more questions available at this level.")

    # Extract the question
    question_doc = question_docs[0]
    german_word = question_doc['word']
    correct_answer = question_doc['meaning']

    # Generate three incorrect options from the same collection
    incorrect_options = list(collection.aggregate([
        {"$match": {"level": current_level, "English": {"$ne": correct_answer}}},  # Exclude correct answer
        {"$sample": {"size": 3}}  # Randomly select 3 incorrect answers
    ]))

    if len(incorrect_options) < 3:
        raise HTTPException(status_code=400, detail="Not enough incorrect options available.")

    incorrect_answers = [doc['meaning'] for doc in incorrect_options]

    # Randomize the options
    options = incorrect_answers + [correct_answer]
    random.shuffle(options)

    # Return the question along with the number of questions answered
    return {
        "german_word": german_word,
        "options": options,
        "correct_answer": correct_answer,
        "questions_answered": user_progress["questions_answered"]  # Add the count of questions answered
    }