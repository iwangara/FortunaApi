from flask import Flask,request, jsonify, make_response
from flaskext.mysql import MySQL
import pymysql
from datetime import datetime
mysql = MySQL()

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
mysql.init_app(app)


#get live sessions
@app.route('/sessions/<string:language>')
def sessions(language):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM livesessions WHERE  language=%s ORDER BY id ASC",language)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# get questions
@app.route('/questions/<int:id>')
def questions(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM livesessions WHERE  id=%s ORDER BY id ASC",id)
        livesession = cursor.fetchall()
        langauge = livesession[0]['language']
        stype = livesession[0]['type']
        session =livesession[0]['session']
        tmp = session.split(",")
        sess =[]
        for x in tmp:
            sess.append(f"{str(x)}")
        sesions =tuple(sess)#','.join(sess)



        print(sesions)
        if stype=='Apollo':
            cursor.execute(f"""SELECT * FROM apollos WHERE language=%s AND  session1 IN {sesions} """,langauge)
            exercise =cursor.fetchall()
            resp = jsonify(exercise)

            resp.status_code = 200
            return resp



    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



# get bot messages
@app.route('/bot_messages')
def bot_messages():

    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM bot_texts ORDER BY id ASC")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# get bot a single message
@app.route('/bot_messages/<int:id>')
def bot_messagesid(id):

    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM bot_texts WHERE id=%s ORDER BY id ASC",id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


"""Student resource"""
#get all students
@app.route('/students')
def students():

    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM students ORDER BY id ASC")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# get single student per language per exercise
@app.route('/student')
def student():
    try:
        if not request.is_json:
            return jsonify(message=['Invalid data type'])
        _json = request.json
        _userid = _json['userid']
        _language = _json['language']
        _exercise = _json['exercise']
        # print(_json)
        if _userid and _language and _exercise:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM students WHERE userid=%s AND language=%s AND exercise=%s ORDER BY id ASC",(_userid,_language,_exercise))
            rows = cursor.fetchone()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# get student per language
@app.route('/student/language')
def student_language():
    if not request.is_json:
        return jsonify(message=['Invalid data type'])
    try:
        _json = request.json
        _userid = _json['userid']
        _language = _json['language']

        # print(_json)
        if _userid and _language :
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM students WHERE userid=%s AND language=%s ORDER BY id ASC",(_userid,_language))
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

"""create new student language exercise"""
@app.route('/student/new',methods=['POST'])
def add_student():
    try:
        if not request.is_json:
            return jsonify(message=['Invalid or empty data'])
        _json = request.json
        _userid = _json.get('userid', None)
        _language = _json.get('language', None)
        _exercise = _json.get('exercise', None)
        _name = _json.get('name', None)
        _fortunas = 0
        if not _language:
            return jsonify(message=['Missing language'])
        if not _userid:
            return jsonify(message=['Missing userid'])
        if not _exercise:
            return jsonify(message=['Missing exercise'])
        if not _name:
            return jsonify(message=['Missing name'])

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM students WHERE userid=%s AND language=%s AND exercise=%s ORDER BY id ASC",
                       (_userid, _language, _exercise))
        stud = cursor.fetchall()
        # if the student is already saved return false
        if len(stud) > 0:
            return jsonify(success=False)
        # else create a new student and give them 0 fortunas
        else:
            cu_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO students(name,userid,language,exercise,fortunas,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (_name, _userid, _language, _exercise, _fortunas, cu_at, cu_at))
            conn.commit()
            resp = jsonify(message=['Student added successfully!'])
            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


"""updated user's fortunas"""
@app.route('/student/point',methods=['POST'])
def add_points():
    try:
        if not request.is_json:
            return jsonify(message=['Invalid or empty data'])
        _json = request.json
        _userid = _json.get('userid', None)
        _language = _json.get('language', None)
        _exercise = _json.get('exercise', None)
        if not _language:
            return jsonify(message=['Missing language'])
        if not _userid:
            return jsonify(message=['Missing userid'])
        if not _exercise:
            return jsonify(message=['Missing exercise'])
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM students WHERE userid=%s AND language=%s AND exercise=%s ORDER BY id ASC",
                       (_userid, _language, _exercise))
        stud = cursor.fetchall()
        if len(stud) > 0:
            cu_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fortunas = stud[0]['fortunas']
            fortunas += 1
            sql = "UPDATE students SET fortunas=%s,updated_at=%s WHERE userid=%s AND language=%s AND exercise=%s"
            data = (fortunas, cu_at, _userid, _language, _exercise)
            cursor.execute(sql, data)
            conn.commit()
            return jsonify(message=[f'{_exercise} fortuna updated'])
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

"""Get student messages"""
@app.route('/student/messages')
def student_messages():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM messages ORDER BY id ASC")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

"""Create or update messages"""
@app.route('/student/messages',methods=['POST'])
def CuMessages():
    if not request.is_json:
        return jsonify(message=['Invalid or empty data'])
    _json = request.json
    _userid = _json.get('userid', None)
    _language = _json.get('language', None)
    _messages = _json.get('count', None)
    if not _language:
        return jsonify(message=['Missing language'])
    if not _userid:
        return jsonify(message=['Missing userid'])
    if not _messages:
        return jsonify(message=['Missing messages'])


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp



if __name__ == '__main__':
    app.run(debug=True)
