import data_manager
import datetime
import os
import bcrypt

QUESTION_IMG_PATH = "/home/victor/PycharmProjects/ask-mate-3-python-Kinkey232/static/image/question"
ANSWER_IMG_PATH = "//home/victor/PycharmProjects/ask-mate-3-python-Kinkey232/static/image/answer"


def question_story_constructor(partial_question_story):
    partial_question_story.update({'submission_time': get_current_datetime(),
                                   'view_number': 0,
                                   'vote_number': 0})
    question_story = partial_question_story
    return question_story


def answer_story_constructor(question_id, partial_answer_story):
    partial_answer_story.update({'submission_time': get_current_datetime(),
                                 'vote_number': 0,
                                 'question_id': question_id})
    answer_story = partial_answer_story
    return answer_story


def get_current_datetime():
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return current_datetime




def remuve_question_image(file_name):
    os.remove(os.path.join(QUESTION_IMG_PATH, file_name))


def remuve_answer_image(answer_image_name):
    os.remove(os.path.join(ANSWER_IMG_PATH, answer_image_name))


def remuve_all_answers_images_of_a_question(question_id):
    list_with_all_answers_images_of_a_question = []
    answers_story = data_manager.get_answer_story(question_id)
    for answer in answers_story:
        list_with_all_answers_images_of_a_question.append(answer['image'])
    for image in list_with_all_answers_images_of_a_question:
        os.remove(os.path.join(ANSWER_IMG_PATH, image))


def construct_question_comment_story(question_id, partial_question_comment_story):
    partial_question_comment_story.update({'submission_time': get_current_datetime(),
                                           'question_id': question_id,
                                           'answer_id': '',
                                           'edited_count': 0})
    question_comment_story = partial_question_comment_story
    return question_comment_story


def construct_answer_comment_story(partial_answer_comment_story, answer_id):
    partial_answer_comment_story.update({'submission_time': get_current_datetime(),
                                         'question_id': '',
                                         'answer_id': answer_id,
                                         'edited_count': 0})
    answer_comment_story = partial_answer_comment_story
    return answer_comment_story


def get_question_id(answer_id):
    for answer_story in data_manager.get_all_answers_stories():
        if int(answer_id) == answer_story['id']:
            return answer_story['question_id']


def get_answer_id(comment_id):
    for answer_comment_story in data_manager.get_all_comment_stories():
        if int(comment_id) == answer_comment_story['id']:
            return answer_comment_story['answer_id']

def get_list_with_all_answers_ids_of_a_question(question_id):
    list_of_ids = []
    for answer_story in data_manager.get_all_answers_stories():
        if answer_story['question_id'] == int(question_id):
            list_of_ids.append (answer_story['id'])
    return (list_of_ids)

def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)