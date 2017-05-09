from flask import Flask, render_template, request, redirect
import function


app = Flask(__name__)


@app.route("/question/<question_id>")
def question_details(question_id):
    questions_list = function.read_csv("./data/question.csv", True)
    for row in questions_list:
        if question_id == row[0]:
            question = row
            break
    question_message = question[5]
    question_title = question[4]
    answers = []
    answers_list = function.read_csv("./data/answer.csv", False)
    for row in answers_list:
        if question_id == row[3]:
            answers.append(row)
    return render_template("question_details.html",
                           question_title=question_title,
                           question_message=question_message,
                           question=question,
                           answers=answers,
                           question_id=question_id)


if __name__ == '__main__':
    app.run(debug=True)
