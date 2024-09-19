# DeutschSprint-Backend

**DeutschSprint** is a FastAPI-powered web application designed to help users learn German vocabulary quickly through interactive multiple-choice quizzes (MCQs). The app dynamically generates 20 random questions from an Excel sheet containing German words and their English meanings, with progress tracked over time. Performance data, including correct and incorrect answers, is logged into MongoDB for later analysis, making DeutschSprint ideal for anyone seeking to rapidly boost their German language skills.

## Features

- **Randomized MCQs**: Generates 20 questions with 4 options (1 correct and 3 incorrect answers) each time.
- **Excel Integration**: Reads German-English vocabulary pairs from an Excel file (multiple sheets supported).
- **Performance Tracking**: Logs test results (correct/incorrect answers) in MongoDB for analysis.
- **Data-Driven**: Stores performance metrics like total tests, correct answers, incorrect answers, and daily results.
- **FastAPI**: Powered by FastAPI, ensuring high performance and ease of use.
- **MongoDB Storage**: Efficient and scalable logging of test data and user performance.

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **File Handling**: Excel file reading with Pandas
- **Environment Variables**: Managed securely with `dotenv`

## Installation

### Prerequisites

- Python 3.7+
- MongoDB installed and running locally or accessible remotely
- `pip` for Python package management

### Step-by-Step Setup

**Clone the Repository**:
   `git clone url`
   `cd DeutschSprint`

Install the Required Python Packages:
Run the following command to install FastAPI, MongoDB driver, Pandas, and other dependencies:

`pip install -r requirements.txt`


### Set up MongoDB:
Ensure MongoDB is running locally, or update the MongoDB connection string in your `.env` file to point to your remote database.

### Configure Environment Variables:

Create a .env file in the project root:
`touch .env`
Add the following environment variables to the `.env` file:

MONGO_URL=mongodb://localhost:27017/

### Prepare Your Excel File:
Ensure that you have a file named questions.xlsx in the project root, with multiple sheets (e.g., A1, A2, etc.), each containing two columns:

Column 1: German
Column 2: English

### Run the Application:

Start the FastAPI server using Uvicorn:
`uvicorn main:app --reload`
The API will be accessible at `http://127.0.0.1:8000`.

