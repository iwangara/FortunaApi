from flask import Flask,request, jsonify, make_response
from flaskext.mysql import MySQL
import pymysql
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
        cursor.execute("SELECT * FROM livesessions WHERE  language=%s",language)
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
        cursor.execute("SELECT * FROM livesessions WHERE  id=%s",id)
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
@app.route('/bot_messages/')
def bot_messages():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM bot_texts")
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
        cursor.execute("SELECT * FROM bot_texts WHERE id=%s",id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


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
    app.run()
