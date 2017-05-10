@app.route("/question/<question_id>/new-answer", methods=['POST'])
def new_answer(question_id):
    return render_template("answer.html")


@app.route("/question/<question_id>/new-answer-submit", methods=['POST'])
def add_new_answer(question_id):
    to_add = []
    time = datetime.datetime.now()
    answer = str(request.form('newanswer'))
    to_add.append(function.get_new_id("./data/answer.csv"))
    to_add.append(time)
    to_add.append(0)
    to_add.append(question_id)
    to_add.append(answer)
    function.write_csv("./data/answer.csv", to_add, False)
    return redirect("/question/{}".format(question_id))
