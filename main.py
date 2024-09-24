from fastapi import FastAPI
from db.init_db import init_db
from routes.vocab_route import vocab_router
from routes.questions_route import question_router

app = FastAPI()

# Initialize the database connection
init_db()

# Register routes
app.include_router(vocab_router)
app.include_router(question_router)
