from flask import Flask, request, send_file
from flask_restful import Api, Resource, reqparse


import os
import base64
import pickle
import json

app = Flask(__name__)
api = Api(app)

from MySQL import ConnectDB
import uuid

DB = ConnectDB()




class Diplom(Resource):

  
    def ReconnectDB():
        DB = ConnectDB()


        ### Регистрация клиента
    @app.route('/Register', methods=['POST'])
    def Register():
        login = request.form['login']
        password = request.form['pass']
        email = request.form['email']
        print(DB.GetStatus())
        if DB.GetStatus():
            return DB.UserRegister(login, password, email)
        else:
            print("Failed to connect to the database. Try again later.")
            return "Failed to connect to the database. Try again later.", 503



        ### Авторизация клиента
    @app.route('/Auth', methods=['POST'])
    def Auth():
        login = request.form['login']
        password = request.form['pass']
        email = request.form['email']

        if DB.GetStatus():
            DBpass = DB.UserAuth(login)
            ###
            if DBpass != None:
                ###
                if DBpass == password:
                    UUID = uuid.uuid4().hex
                    DB.UserUUID(login, UUID)
                    return "Successful authorization.", 201 # Успешная авторизация (НУЖЕН ТОКЕН ПОТОМ)
                else:
                    return "The specified username or password is incorrect", 401 # Неправильный пароль
                ###
            else:
                return "The user's data is specified incorrectly", 402 # Неправильный логин
            ###
        else:
            print("Failed to connect to the database. Try again later.")
            return "Failed to connect to the database. Try again later.", 503




        ### Загрузка фото на сервер
    @app.route('/UploadFile', methods=['POST'])
    def UploadFile():
        print(request.form)
        if 'file' not in request.files:
            return "No file part", 200
        else:
            file = request.files['file']
            if file.filename != '':
                file.save(os.path.join(os.getcwd() + "/Images/", file.filename))
            return "Good file", 200




        ### Возврат фото с сервера
    @app.route('/ReturnFile', methods=['GET'])
    def ReturnFile():
        print(request.args['ID']) # ID Фото для возврата
        file = os.getcwd() + "/Images/Niko.png"
        return send_file(file, mimetype='image/png'), 202




api.add_resource(Diplom)
if __name__ == '__main__':
    app.run(debug=False)