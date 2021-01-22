from flask import Flask,redirect,render_template,request,url_for,session,Response,make_response
import data_manager, utility
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def list_first_5_questions():
    all_questions_stories = data_manager.get_first_5_questions_stories()
    return render_template("list.html", all_questions_stories=all_questions_stories)

@app.route("/")
def index():
    if session.get('username') :
        return list_first_5_questions()
    else:
        return redirect('/login')

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        password = request.form.get('password')
        user = request.form.get('user')
        users = data_manager.list_users()
        list_users = []
        for things in users:
            list_users.append(things['email'])

        if user in list_users:
            hash_pass = data_manager.user_password(user)
            if utility.verify_password(password,hash_pass[0]['password']):
                session['username']= user
                userid = data_manager.select_userid(session['username'])
                session['user_id']= userid[0]['id']
                return list_first_5_questions()

            else:
                return render_template("login.html",error = "incorrect password")
        else:
            return render_template("login.html", error="incorrect user")

    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login')




@app.route("/list")
def list_all_questions():
    if session.get('username'):
        if not request.args.get('order_by') and request.args.get('order_direction'):
            all_questions_stories = data_manager.get_all_questions_stories()
            return render_template("list.html", all_questions_stories=all_questions_stories)
        else:
            order_by = request.args.get('order_by')
            order_direction = request.args.get('order_direction')
            all_questions_stories = data_manager.get_all_questions_stories_sorted(order_by, order_direction)
            return render_template("list.html", all_questions_stories=all_questions_stories)
    else:
        return redirect('/login')

@app.route("/search")
def list_search_result():
    if session.get('username'):
        word = request.args.get('q')
        all_questions_stories = data_manager.get_questions_story_by_search_word(word)
        for question_story in all_questions_stories:
            if word in question_story['title']:
                question_story['title'] = question_story['title'].replace(word,'<span style="background-color: yellow;">'+word+'</span>')
            if word in question_story['message']:
                question_story['message'] = question_story['message'].replace(word,'<span style="background-color: yellow;">'+word+'</span>')

        return render_template("list.html", all_questions_stories=all_questions_stories, word=word)
    else:
        return redirect('/login')

@app.route('/display-question/<question_id>', methods=['POST', 'GET'])
def list_question(question_id):
    if session.get('username'):
        if request.method == "GET":
            question_story = data_manager.get_questions_story(question_id)
            answer_story = data_manager.get_answer_story(question_id)
            question_comment_stories = data_manager.get_question_comments_stories(question_id)
            all_answers_comments_stories = data_manager.get_all_comment_stories()
            all_tags_for_a_question = data_manager.get_all_tags_for_a_question(question_id)
            return render_template('display-question.html',
                                   question_story=question_story,
                                   answer_story=answer_story,
                                   question_comment_stories=question_comment_stories,
                                   all_answers_comments_stories=all_answers_comments_stories,
                                   all_tags_for_a_question=all_tags_for_a_question)
    else:
        return redirect('/login')


@app.route('/add-question', methods=['POST', 'GET'])
def add_question():
    if session.get('username'):
        if request.method == "POST":
            partial_question_story = request.form.to_dict()
            if request.files:
                image = request.files["image"]
                image.save(
                    os.path.join(utility.QUESTION_IMG_PATH, image.filename))
                partial_question_story.update({'image': image.filename})
            else:
                partial_question_story.update({'image': ''})
            question_story = utility.question_story_constructor(partial_question_story)
            data_manager.write_question_story(question_story,session['user_id'])
            question_id = data_manager.get_bigest_id('question')
            return redirect(url_for('list_question', question_id=question_id['max']))

        if request.method == "GET":
            return render_template('add-question.html')
    else:
        return redirect('/login')

@app.route('/display-question/<question_id>/add-answer', methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == "GET":
        return render_template('add-answer.html', question_id=question_id)
    if request.method == "POST":
        partial_answer_story = request.form.to_dict()
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(utility.ANSWER_IMG_PATH, image.filename))
            partial_answer_story.update({'image': image.filename})
        else:
            partial_answer_story.update({'image': ''})

        answer_story = utility.answer_story_constructor(question_id, partial_answer_story)
        data_manager.write_answer_story(answer_story)
        return redirect(url_for('list_question', question_id=answer_story['question_id']))


@app.route('/display-question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_all_question_tag(question_id)
    data_manager.delete_all_question_comments(question_id)
    list_with_answers_ids_to_be_deleted = utility.get_list_with_all_answers_ids_of_a_question(question_id)
    for answer_id in list_with_answers_ids_to_be_deleted:
        data_manager.delete_all_answer_comments(answer_id)
    utility.remuve_all_answers_images_of_a_question(question_id)
    try:
        utility.remuve_all_answers_images_of_a_question(question_id)
    except:
        print('nu sunt imagini ')
    data_manager.delete_answer_story(question_id)
    try:
        utility.remuve_all_answers_images_of_a_question(question_id)
    except:
        print('nu sunt imagini cccc')

    data_manager.delete_question_story(question_id)

    return redirect(url_for('list_all_questions'))


@app.route('/display-question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    if request.method == "GET":
        question_story = data_manager.get_questions_story(question_id)
        return render_template("edit-question.html", question_story=question_story)
    if request.method == "POST":
        data_to_be_updated = request.form.to_dict()
        data_manager.update_question_story(question_id, data_to_be_updated)
        return redirect(url_for('list_question', question_id=question_id))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answer_story = data_manager.get_answer_story_by_answer_id(answer_id)
    answer_image_name = answer_story['image']
    utility.remuve_answer_image(answer_image_name)
    data_manager.delete_all_answer_comments(answer_id)
    question_id = answer_story['question_id']
    data_manager.delete_answer_story_by_answer_id(answer_id)
    return redirect(url_for('list_question', question_id=question_id))


@app.route('/question/<question_id>/vote_up')
def vote_question_up(question_id):
    data_manager.increment_question_vote(question_id)
    return redirect(url_for('list_question', question_id=question_id))


@app.route('/question/<question_id>/vote_down')
def vote_question_down(question_id):
    data_manager.decrease_question_vote(question_id)
    return redirect(url_for('list_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote_up')
def vote_answer_up(answer_id):
    data_manager.increment_answer_vote(answer_id)
    answer_story = data_manager.get_answer_story_by_answer_id(answer_id)
    question_id = answer_story['question_id']
    return redirect(url_for('list_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote_down')
def vote_answer_down(answer_id):
    data_manager.decrease_answer_vote(answer_id)
    answer_story = data_manager.get_answer_story_by_answer_id(answer_id)
    question_id = answer_story['question_id']
    return redirect(url_for('list_question', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def add_comment_to_question_story(question_id):
    if request.method == "POST":
        partial_question_comment_story = request.form.to_dict()
        question_comment_story = utility.construct_question_comment_story(question_id, partial_question_comment_story)
        data_manager.write_question_comment(question_comment_story)
        return redirect(url_for('list_question', question_id=question_id))
    if request.method == "GET":
        return render_template("add-question-comment.html", question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=["POST", "GET"])
def add_comment_to_answer_story(answer_id):
    if request.method == "POST":
        partial_answer_comment_story = request.form.to_dict()
        answer_comment_story = utility.construct_answer_comment_story(partial_answer_comment_story, answer_id)
        data_manager.write_answer_comment(answer_comment_story)
        question_id = utility.get_question_id(answer_id)
        return redirect(url_for('list_question', question_id=question_id))

    if request.method == "GET":
        return render_template("add-answer-comment.html", answer_id=answer_id)


@app.route('/answer/<answer_id>/edit', methods=['POST', 'GET'])
def edit_answer(answer_id):
    if request.method == "GET":
        answer_story = data_manager.get_answer_story_by_answer_id(answer_id)
        return render_template("edit-answer.html", answer_story=answer_story)
    if request.method == "POST":
        data_to_be_updated = request.form.to_dict()
        data_manager.update_answer_story(answer_id, data_to_be_updated)
        question_id = utility.get_question_id(answer_id)
        return redirect(url_for('list_question', question_id=question_id))


@app.route('/comment/<comment_id>/edit', methods=['POST', 'GET'])
def edit_comment(comment_id):
    if request.method == "GET":
        answer_comment_story = data_manager.get_answer_comment_story(comment_id)
        return render_template("edit-comment.html", answer_comment_story=answer_comment_story)
    if request.method == "POST":
        data_to_be_updated = request.form.to_dict()
        data_manager.update_answer_comment_story(comment_id, data_to_be_updated)
        answer_id = utility.get_answer_id(comment_id)
        question_id = utility.get_question_id(answer_id)
        return redirect(url_for('list_question', question_id=question_id))


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    if request.args.get('question_id') is None:
        answer_id = utility.get_answer_id(int(comment_id))
        question_id = utility.get_question_id(answer_id)
        data_manager.delete_comment_story(comment_id)
        return redirect(url_for('list_question', question_id=question_id))
    else:
        question_id = int(request.args.get('question_id'))
        data_manager.delete_comment_story(comment_id)
        return redirect(url_for('list_question', question_id=question_id))


@app.route('/question/<question_id>/new-tag', methods=['POST', 'GET'])
def add_question_tag(question_id):
    if request.method == "POST":
        question_tag_dict = request.form.to_dict()
        question_tag = question_tag_dict['tag']
        data_manager.write_question_tag(question_tag,question_id)
        return redirect(url_for('list_question', question_id=question_id))
    if request.method == "GET":
        return render_template("add-question-tag.html", question_id=question_id)

@app.route('/registration', methods=['POST', 'GET'])
def register_user():
    if request.method == "GET":
        return render_template("registration.html")
    if request.method == "POST":
        user_story = request.form.to_dict()
        user_story['password'] = utility.hash_password(user_story['password'])
        data_manager.write_user_story(user_story)
        return redirect('/')

@app.route('/users')
def list_all_users():
    if session.get('username'):
        users_stories = data_manager.get_all_users_stories()
        return render_template("users.html", users_stories=users_stories)
    else:
        return redirect('/login')

@app.route('/user/<string:user_id>')
def profile(user_id):
    print (session.get('username'))
    if session.get('username'):
        data_manager.set_reputation_user(session["user_id"])
        profile_data = data_manager.list_user_profile(user_id)
        return render_template('user.html',profile_data = profile_data)
    else:
        return redirect('/login')


@app.route('/link_q/<string:question>')
def user_question_link(question):
    id =data_manager.redirect_question(question)
    return list_question(str(id[0]["id"]))

@app.route('/link_a/<string:answer>')
def user_answer_link(answer):
    id =data_manager.redirect_answer(answer)
    return list_question(str(id[0]["question_id"]))

@app.route('/link_c/<string:comment>')
def user_comment_link(comment):
    id =data_manager.redirect_comment(comment)
    return list_question(str(id[0]["question_id"]))


@app.route('/mark-accepted/<answer_id>/<question_id>')
def route_mark_accepted(answer_id, question_id):
    data_manager.mark_answer_as_accepted(answer_id)
    return redirect(url_for('list_question', question_id=question_id))


@app.route('/unmark/<answer_id>/<question_id>')
def route_unmark_answer(answer_id, question_id):
    data_manager.unmark_accepted_answer(answer_id)
    return redirect(url_for('list_question', question_id=question_id))




if __name__ == "__main__":
    app.run(
        debug=True
    )
