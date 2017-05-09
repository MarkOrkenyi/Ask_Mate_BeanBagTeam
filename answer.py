@app.route("/question/<question_id>/new-answer", methods=['POST'])
def new_answer(question_id):
    return render_template("answer.html")


@app.route("/question/<question_id>/new-answer-submit", methods=['POST'])
def add_new_answer(question_id):
    answer = str(request.form('newanswer'))
    return redirect("./")
