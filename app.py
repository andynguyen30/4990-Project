from flask import Flask, request, render_template
import os
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Define the HTML template for the frontend
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Quiz Generator</title>
</head>
<body>
    <h1>Quiz Generator</h1>
    <form action="/generate_completion" method="post">
        <label for="prompt">Prompt:</label>
        <input type="text" id="prompt" name="prompt"><br><br>
        <input type="submit" value="Generate Completion">
    </form>
    <div id="completion"></div>
</body>
</html>
"""

# Route for the home page
@app.route('/')
def home():
    return html_template

# Route for generating the completion
@app.route('/generate_completion', methods=['POST'])
def generate_completion():
    prompt = request.form.get('prompt')

    # Generate completion using OpenAI's API with GPT-3.5 Turbo model
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": 'Create a multiple choice quiz with the subject = ' + prompt + ' include the correct answers in a seperate place at the end'}],
        model="gpt-3.5-turbo",
    )

    # Extract and format the generated completion
    completion_text = completion.choices[0].message.content
    questions_and_answers = completion_text.split('\n\n')  # Split completion into questions and answers

    # Extract questions and correct answers separately
    questions = questions_and_answers[:-1]  # Exclude the last element (correct answers)
    correct_answers = questions_and_answers[-1].split('\n')[1:]  # Get correct answers and remove the "Correct Answers:" line

    return render_template('quiz.html', questions=questions, correct_answers=correct_answers)

if __name__ == '__main__':
    app.run(debug=True)
