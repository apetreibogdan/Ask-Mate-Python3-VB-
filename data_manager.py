from psycopg2.extras import RealDictCursor
import database_common, utility
from flask import session
import datetime


@database_common.connection_handler
def get_all_questions_stories(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC
       """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_questions_stories_sorted(cursor: RealDictCursor, order_by, order_direction) -> list:
    if order_by and order_direction is not None:
        query = f"""
            SELECT *
            FROM question
            ORDER BY {order_by} {order_direction}
           """
        cursor.execute(query)
        return cursor.fetchall()
    else:
        query = """
                SELECT *
                FROM question
                ORDER BY submission_time DESC
               """
        cursor.execute(query)
        return cursor.fetchall()


@database_common.connection_handler
def get_first_5_questions_stories(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5
       """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_answers_stories(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM answer
        ORDER BY submission_time DESC
       """
    cursor.execute(query)
    return cursor.fetchall()




@database_common.connection_handler
def get_questions_story(cursor: RealDictCursor, question_id) -> list:
    query = f"""
        SELECT q.* , u.username
        FROM question q
        LEFT JOIN users u ON q.user_id = u.id
        WHERE q.id = {question_id}
        """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_questions_story_by_search_word(cursor: RealDictCursor, word) -> list:
    query = f"""
        SELECT *
        FROM question
        WHERE CONCAT(title,message)
        LIKE '%{word}%'
       """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_story(cursor: RealDictCursor, question_id) -> list:
    query = f"""
        SELECT *
        FROM answer
        WHERE question_id = {question_id}
       """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_story_by_answer_id(cursor: RealDictCursor, answer_id) -> list:
    query = f"""
        SELECT *
        FROM answer
        WHERE id = {answer_id}
       """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def write_question_story(cursor: RealDictCursor, question_story, userid) -> list:
    query = f"""
                INSERT INTO question ( submission_time,
                                        view_number,
                                        vote_number,
                                        title,
                                        message,
                                        image,
                                        user_id)
                VALUES ('{question_story['submission_time']}',
                        '{question_story['view_number']}',
                        '{question_story['vote_number']}',
                        '{question_story['title']}',
                        '{question_story['message']}',
                        '{question_story['image']}',
                        '{userid}')
                """
    cursor.execute(query)


@database_common.connection_handler
def write_answer_story(cursor: RealDictCursor, answer_story) -> list:
    query = f"""
                INSERT INTO answer( submission_time,
                                    vote_number,
                                    question_id,
                                    message,
                                    image,
                                    user_id)
                VALUES ('{answer_story['submission_time']}',
                        '{answer_story['vote_number']}',
                        '{answer_story['question_id']}',
                        '{answer_story['message']}',
                        '{answer_story['image']}',
                        '{session['user_id']}')
                """
    cursor.execute(query)


@database_common.connection_handler
def delete_question_story(cursor: RealDictCursor, question_id) -> list:
    query = f"""
                DELETE FROM question
                WHERE id = {question_id};
                """
    cursor.execute(query)


@database_common.connection_handler
def delete_answer_story(cursor: RealDictCursor, question_id) -> list:
    query = f"""
                DELETE FROM answer
                WHERE question_id = {question_id};
                """
    cursor.execute(query)


@database_common.connection_handler
def delete_comment_story(cursor: RealDictCursor, comment_id) -> list:
    query = f"""
                DELETE FROM comment
                WHERE id = {comment_id};
                """
    cursor.execute(query)


@database_common.connection_handler
def delete_all_answer_comments(cursor: RealDictCursor, answer_id) -> list:
    query = f"""
                DELETE FROM comment
                WHERE answer_id = {answer_id};
                """
    cursor.execute(query)


@database_common.connection_handler
def delete_all_question_comments(cursor: RealDictCursor, question_id) -> list:
    query = f"""
                DELETE FROM comment
                WHERE question_id = {question_id};
                """
    cursor.execute(query)


@database_common.connection_handler
def update_question_story(cursor: RealDictCursor, question_id, data_to_be_updated):
    for key, value in data_to_be_updated.items():
        query = f"""
            UPDATE question
            SET {key} = '{value}'
            WHERE id = '{question_id}';
           """
        cursor.execute(query)


@database_common.connection_handler
def update_answer_story(cursor: RealDictCursor, answer_id, data_to_be_updated):
    query = f""" UPDATE answer
                SET message = '{data_to_be_updated['message']}'
                WHERE id = '{answer_id}';
               """
    cursor.execute(query)


@database_common.connection_handler
def update_answer_comment_story(cursor: RealDictCursor, comment_id, data_to_be_updated):
    query = f""" UPDATE comment
                SET message = '{data_to_be_updated['message']}',
                    submission_time = '{utility.get_current_datetime()}',
                    edited_count = edited_count + 1
                WHERE id = '{comment_id}';
               """
    cursor.execute(query)


@database_common.connection_handler
def delete_answer_story_by_answer_id(cursor: RealDictCursor, answer_id) -> list:
    query = f"""
                DELETE FROM answer
                WHERE id = {answer_id}; 
                """
    cursor.execute(query)


@database_common.connection_handler
def increment_question_vote(cursor: RealDictCursor, question_id) -> list:
    query = f"""
                UPDATE question
                SET vote_number = vote_number + 1
                WHERE id = {question_id}
                """
    cursor.execute(query)


@database_common.connection_handler
def decrease_question_vote(cursor: RealDictCursor, question_id) -> list:
    query = f"""
                UPDATE question
                SET vote_number = vote_number - 1
                WHERE id = {question_id}
                """
    cursor.execute(query)


@database_common.connection_handler
def increment_answer_vote(cursor: RealDictCursor, answer_id) -> list:
    query = f"""
                UPDATE answer
                SET vote_number = vote_number + 1
                WHERE id = {answer_id}
                """
    cursor.execute(query)


@database_common.connection_handler
def decrease_answer_vote(cursor: RealDictCursor, answer_id) -> list:
    query = f"""
            UPDATE answer
            SET vote_number = vote_number - 1
            WHERE id = {answer_id}
            """
    cursor.execute(query)


@database_common.connection_handler
def increment_question_views(cursor: RealDictCursor, question_id) -> list:
    query = f"""
                UPDATE question
                SET view_number = view_number + 1
                WHERE id = {question_id}
                """
    cursor.execute(query)


@database_common.connection_handler
def get_all_comment_stories(cursor: RealDictCursor) -> list:
    query = """
            SELECT *
            FROM comment
           """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def write_question_comment(cursor: RealDictCursor, question_comment_story):
    query = """
                INSERT INTO comment (question_id,
                                    submission_time,
                                    message,
                                    edited_count,
                                    user_id)
                VALUES ( %s, %s, %s, %s, %s)
                """
    cursor.execute(query, (question_comment_story['question_id'],
                           question_comment_story['submission_time'],
                           question_comment_story['message'],
                           question_comment_story['edited_count'],
                           session['user_id'])
                   )


@database_common.connection_handler
def get_question_comments_stories(cursor: RealDictCursor, question_id) -> list:
    query = f"""
            SELECT *
            FROM comment
            WHERE question_id = {question_id}
           """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_comment_story(cursor: RealDictCursor, comment_id) -> list:
    query = f"""
            SELECT *
            FROM comment
            WHERE id = {comment_id}
           """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def write_answer_comment(cursor: RealDictCursor, answer_comment_story):
    query = """
                INSERT INTO comment (answer_id,
                                    submission_time,
                                    message,
                                    edited_count,
                                    user_id)
                VALUES ( %s, %s, %s, %s, %s)
                """
    cursor.execute(query, (answer_comment_story['answer_id'],
                           answer_comment_story['submission_time'],
                           answer_comment_story['message'],
                           answer_comment_story['edited_count'],
                           session['user_id']))


@database_common.connection_handler
def write_question_tag(cursor: RealDictCursor, question_tag, question_id) -> list:
    query = f"""
            SELECT id
            FROM tag
            WHERE name = '{question_tag}'
           """
    cursor.execute(query)
    tag_id = cursor.fetchone()

    query = """INSERT INTO question_tag ( question_id,tag_id)
                VALUES (%s, %s)
            """
    cursor.execute(query, (question_id, tag_id['id']))


@database_common.connection_handler
def get_all_tags_for_a_question(cursor: RealDictCursor, question_id) -> list:
    query = f"""SELECT *
                FROM question_tag
                JOIN tag ON question_tag.tag_id=tag.id
                WHERE question_tag.question_id = {question_id}
                """
    cursor.execute(query)
    return cursor.fetchall()



@database_common.connection_handler
def delete_all_question_tag(cursor: RealDictCursor, question_id) -> list:
    query = f"""
            DELETE FROM question_tag
            WHERE question_id = {question_id}
           """
    cursor.execute(query)



@database_common.connection_handler
def get_bigest_id(cursor: RealDictCursor, table) -> list:
    query = f"""
            SELECT MAX(id)
            FROM {table}
           """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def list_users(cursor: RealDictCursor) -> list:
    query = """
        SELECT email
        FROM users
       """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def user_password(cursor: RealDictCursor, user: str) -> list:
    query = """
        SELECT password
        FROM users
        WHERE email = '%s' """
    cursor.execute(query%(user))
    return cursor.fetchall()


@database_common.connection_handler
def select_userid(cursor: RealDictCursor, user) -> list:
    query = """
        SELECT id
        FROM users
        WHERE email = '%s' """
    cursor.execute(query%(user))
    return cursor.fetchall()

@database_common.connection_handler
def write_user_story(cursor: RealDictCursor, user_story) -> list:
    query = """
               INSERT INTO users (  reputation,
                                    username,
                                    registration_date,
                                    email,
                                    password )
               VALUES ( %s, %s, %s, %s, %s)
                   """
    cursor.execute(query, (0,
                           user_story['username'],
                           utility.get_current_datetime(),
                           user_story['email'],
                           user_story['password']))

@database_common.connection_handler
def get_all_users_stories(cursor: RealDictCursor ) -> list:
    query = """
       select  u.id, u.username, u.registration_date, u.reputation, count (distinct q.id) as count_questions, count (distinct a.id) as count_answers, count (distinct c.id) as count_comments
from users u
left join question q on u.id = q.user_id
left join answer a on u.id = a.user_id
left join comment c on u.id = c.user_id
group by  u.id 
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def list_user_profile(cursor: RealDictCursor ,userid) -> list:
    query = """
select  u.id, u.username, u.registration_date, u.reputation, count (distinct q.id) as count_questions, count (distinct a.id) as count_answers,
       count (distinct c.id) as count_comments,
       string_agg (distinct  a.message::character varying,'--' order by a.message::character varying desc) as "user_answers",
       string_agg (distinct  q.message::character varying,'--' order by q.message::character varying desc) as "user_questions",
       string_agg (distinct  c.message::character varying,'--' order by c.message::character varying desc) as "user_comments"

from users u
left join question q on u.id = q.user_id
left join answer a on u.id = a.user_id
left join comment c on u.id = c.user_id
where u.id= '%s'
group by  u.id
        """
    cursor.execute(query%(userid))
    return cursor.fetchall()



@database_common.connection_handler
def redirect_question(cursor: RealDictCursor, question) -> list:
    query = """
        SELECT id
        FROM question
        WHERE message  like '%s'"""
    cursor.execute(query%(question))
    return cursor.fetchall()

@database_common.connection_handler
def redirect_answer(cursor: RealDictCursor, answer) -> list:
    query = """
        SELECT question_id
        FROM answer
        WHERE message  like '%s'"""
    cursor.execute(query%(answer))
    return cursor.fetchall()

@database_common.connection_handler
def redirect_comment(cursor: RealDictCursor, comment) -> list:
    query = """
        SELECT question_id
        FROM comment
        WHERE message  like '%s'"""
    cursor.execute(query%(comment))
    return cursor.fetchall()


@database_common.connection_handler
def set_reputation_user(cursor: RealDictCursor,id) -> list:
    query = """
update users u
set reputation = ((select sum(vote_number) from question q where q.user_id = u.id)+
                 (select sum(vote_number) from answer a where a.user_id = u.id)+
                  (select sum(accepted)from answer a where a.user_id = u.id))
where  u.id = '%s'"""
    cursor.execute(query%(id))



@database_common.connection_handler
def mark_answer_as_accepted(cursor: RealDictCursor, answer_id) -> list:
    query = f"""
            UPDATE answer
            SET accepted = 10
            WHERE id = {answer_id}
            """
    cursor.execute(query)

@database_common.connection_handler
def unmark_accepted_answer(cursor: RealDictCursor, answer_id) -> list:
    query = f"""
            UPDATE answer
            SET accepted = 5
            WHERE id = {answer_id}
            """
    cursor.execute(query)
