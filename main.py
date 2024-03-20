from flask import Flask, request

from flask_api import status
from psycopg2.extras import RealDictCursor


import psycopg2

app = Flask(__name__)

@app.route("/getAuditories",methods = ['GET'])
def getAuditories():
    connection = psycopg2.connect(user="postgres",
                                  password="123qwe",
                                  host="92.63.178.148",
                                  port="5432",
                                  database="hackaton")
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM auditories")
        resultAuditories = cursor.fetchall()

    connection.close()
    return resultAuditories
@app.route("/getAuditoryEvents/<auditory_id>",methods = ['GET'])
def getAuditoryEvents(auditory_id):
    connection = psycopg2.connect(user="postgres",
                                  password="123qwe",
                                  host="92.63.178.148",
                                  port="5432",
                                  database="hackaton")
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM events WHERE auditoryId = %s",(auditory_id))
        events = cursor.fetchall()

    connection.close()
    return events
@app.route("/signUp",methods = ['POST'])
def signUp():
    email = request.form.get('email')
    role = request.form.get('role')
    password = request.form.get('password')

    content = {'result': 'status'}

    connection = psycopg2.connect(user="postgres",
                                  password="123qwe",
                                  host="92.63.178.148",
                                  port="5432",
                                  database="hackaton")
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (email,password,role) VALUES (%s,%s,%s)", (email, password, role))
        else:
            connection.close()
            return content,  status.HTTP_400_BAD_REQUEST

    connection.commit()
    connection.close()
    return content, status.HTTP_200_OK

@app.route("/login",methods = ['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    content = {'result': 'status'}

    connection = psycopg2.connect(user="postgres",
                                  password="123qwe",
                                  host="92.63.178.148",
                                  port="5432",
                                  database="hackaton")
    #Добавить проверку на существование пользователя и правильность пароля
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s",(email,password,))
        user = cursor.fetchone()
        if (not user):
            connection.close()
            return content, status.HTTP_400_BAD_REQUEST
        else:
            connection.close()
            return user, status.HTTP_200_OK

@app.route("/joinEvent",methods = ['POST'])
def joinEvent():
    id = request.form.get('id')
    password = request.form.get('password')
    eventId = request.form.get('eventId')

    content = {'result': 'status'}

    connection = psycopg2.connect(user="postgres",
                                  password="123qwe",
                                  host="92.63.178.148",
                                  port="5432",
                                  database="hackaton")
    # Добавить проверку на то что ивент существует вообще
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s AND password = %s", (id, password,))
        user = cursor.fetchone()
        if (not user):
            connection.close()
            return content, status.HTTP_404_NOT_FOUND
        else:
            cursor.execute("SELECT * FROM members WHERE userId = %s AND eventId = %s", (id, eventId,))
            if (cursor.fetchone()):
                connection.close()
                return content, status.HTTP_400_BAD_REQUEST
            else:
                cursor.execute("INSERT INTO members (userId, eventId) VALUES (%s,%s)",(id, eventId))
                connection.commit()
                connection.close()
                return content, status.HTTP_200_OK


if __name__ == '__main__':
    app.run(debug=True)