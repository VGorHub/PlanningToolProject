from flask import Flask, request, json
from flask import render_template
from flask_restful import Api , Resource , reqparse
from flask_api import status
from psycopg2.extras import RealDictCursor

import json

import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user = "postgres",
                                    password = "123qwe",
                                    host = "92.63.178.148",
                                    port = "5432",
                                    database= "hackaton")

    # Курсор для выполнения операций с базой данных
    with connection.cursor() as cursor:
        # #создание новой таблицы
        # cursor.execute("""CREATE TABLE users (
        #                     id serial PRIMARY KEY,
        #                     email varchar(50) NOT NULL,
        #                     password varchar(50) NOT NULL,
        #                     role varchar(30)
        #                     )""")
        # cursor.execute("""CREATE TABLE auditory(
        #                     id serial PRIMARY KEY,
        #                     name varhar(30),
        #                     type varchar(30)
        #                     """)
        # cursor.execute("""INSERT INTO users(email,password)
        #                     VALUES ('vova@mail.ru','qwer123')""")
        cursor.execute("""SELECT column_name, data_type
                            FROM information_schema.columns
                            WHERE table_name = 'auditories';
                            """)

        print(cursor.fetchall())

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        connection.close()
        print("Соединение с PostgreSQL закрыто")

app = Flask(__name__)
api = Api()

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