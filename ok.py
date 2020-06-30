# -*- coding: utf-8 -*-
from flask import Flask,request, jsonify, json
from flaskext.mysql import MySQL
import pymysql
import decimal
from datetime import datetime
mysql = MySQL()
class MyJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)
app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.config.from_object('config.DevelopmentConfig')
mysql.init_app(app)

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
        return sesions
        # if stype == "Wala":
        #     cursor.execute(f"""SELECT * FROM wala WHERE language=%s AND  session1 IN {sesions} """,
        #                    langauge)
        #     exercise = cursor.fetchall()
        #     resp = jsonify(exercise)
        #     resp.status_code = 200
        #     return resp

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)