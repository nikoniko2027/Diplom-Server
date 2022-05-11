from flask import Flask, request, send_file
from flask_restful import Api, Resource, reqparse

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

        if DB.GetStatus():
            DBpass = DB.UserAuth(login)
            ###
            if DBpass != None:
                ###
                if DBpass == password:
                    UUID = uuid.uuid4().hex
                    DB.UserUUID(login, UUID)
                    return "Successful authorization.", 201 # Успешная авторизация
                else:
                    return "The specified username or password is incorrect", 401 # Неправильный пароль
                ###
            else:
                return "The user's data is specified incorrectly", 402 # Неправильный логин
            ###
        else:
            print("Failed to connect to the database. Try again later.")
            return "Failed to connect to the database. Try again later.", 503




        ### Получение данных об аккаунте
    @app.route('/GetAccountInfo', methods=['POST'])
    def GetAccountInfo():
        login = request.form['login']
        return DB.GetAccountInfo(login), 210




        ### Получение данных об аккаунте по UUID
    @app.route('/GetLoadAuth', methods=['POST'])
    def GetLoadAuth():
        myuuid = request.form['uuid']
        return DB.GetUserInfoWithUUID(myuuid), 210




        ### Получение данных об аккаунте по UUID
    @app.route('/GetInfoAuthUUID', methods=['POST'])
    def GetInfoAuthUUID():
        myuuid = request.form['uuid']
        return DB.GetUserInfoWithUUID(myuuid), 211




        ### Отправка сообщения в чат
    @app.route('/SendChatMessage', methods=['POST'])
    def SendChatMessage():
        myuuid = request.form['uuid']
        message = request.form['message'] # WebCommunication плохо работает с русскими символами.
        DB.SendMessage(myuuid, message)
        return "Successfull send", 222



        ### Получение 10 последних сообщений чата
    @app.route('/GetChatMessage', methods=['POST'])
    def GetChatMessage():
        return DB.GetLast10Message(), 223



        ### Генерация лобби
    @app.route('/GenerateLobby', methods=['POST'])
    def GenerateLobby():
        login = request.form['firstplayer']
        correctanswer = request.form['correctanswer']
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        gametype = request.form['gametype']
        DB.GenerateLobby(login, correctanswer, gametype, q1, q2, q3, q4, q5)
        return "Successfull Generate Lobby", 224




        ### Получение всех лобби
    @app.route('/GetLobbies', methods=['POST'])
    def GetLobbies():
        login = request.form['login']
        return DB.GetLobbies(login), 225




        ### Получение всех лобби
    @app.route('/EndLobby', methods=['POST'])
    def EndLobby():
        login = request.form['secondplayer']
        id = request.form['id']
        correctanswer = request.form['correctanswer']
        DB.EndLobby(login, correctanswer, id)
        return "Successfull End Lobby", 226




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