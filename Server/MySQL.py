#!/usr/bin/python3

import pymysql
import json
import random

Host = 'db3.myarena.ru'
User = 'u12254_diplom'
Pass = 'nikoniko2027'
DB = 'u12254_diplom'


class ConnectDB:

    ### Получение статуса подключения к БД
    def GetStatus(self):
        try:
            con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
            con.close()
            return True
        except:
            return False
    



    ### INSERT пользователя в БД
    def UserRegister(self, login, password, email):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        sql = "INSERT INTO `u12254_diplom`.`Users` (`ID`, `Login`, `Password`, `Email`, `MMR`) VALUES (NULL, %s, %s, %s, '159')"
        try:
            cur.execute(sql, (login, password, email))
            con.commit()
            con.close()
            return "Successful registration", 202 # Успешная регистрация
        except:
            con.close()
            return "An account with this username already exists.", 403 # Пользователь с указанным логином уже существует




    ### SELECT получения пароля пользователя
    def UserAuth(self, login):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        sql = "SELECT `Password` FROM `Users` WHERE `Login` = %s"
        cur.execute(sql, login)
        res = cur.fetchone()
        con.commit()
        con.close()
        try:
            return res["Password"]
        except:
            return None




    ### SELECT для получения данных аккаунта без пароля
    def GetAccountInfo(self, login):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        sql = "SELECT `ID`, `Login`, `Email`, `MMR`, `UUID` FROM `Users` WHERE `Login` LIKE %s"
        cur.execute(sql, login)
        res = cur.fetchone()
        con.commit()
        con.close()
        return res




    ### SELECT получения MMR пользователя
    def GetUserMMR(self, login):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        sql = "SELECT `MMR` FROM `Users` WHERE `Login` = %s"
        cur.execute(sql, login)
        res = cur.fetchone()
        con.commit()
        con.close()
        try:
            return res["MMR"]
        except:
            return None




    ### SELECT получения профиля пользователя по UUID
    def GetUserInfoWithUUID(self, myuuid):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        sql = "SELECT `ID`, `MMR`, `Login`, `UUID`, `Email` FROM `Users` WHERE `UUID` = %s"
        cur.execute(sql, myuuid)
        res = cur.fetchone()
        con.commit()
        con.close()

        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "SELECT * FROM `Lobby` WHERE `FirstPlayer` LIKE %s OR `SecondPlayer` LIKE %s"
        cur.execute(sql, (res["Login"], res["Login"]))
        arr = list()
        for i in cur:
            arr.append(i)
        res["Lobbies"] = json.dumps(arr)
        con.commit()
        con.close()

        return res

        
        

    ### UPDATE uuid пользователя при авторизации
    def UserUUID(self, login, uuid):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        sql = "UPDATE `Users` SET `UUID`=%s WHERE `Login` = %s"
        cur.execute(sql, (uuid, login)) 
        res = cur.fetchone()
        con.commit()
        con.close()




    ### INSERT сообщения в чате пользователя
    def SendMessage(self, myuuid, message):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "SELECT `ID`, `Login` FROM `Users` WHERE `UUID` = %s"
        cur.execute(sql, myuuid)
        res = cur.fetchone()
        con.commit()
        con.close()

        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "INSERT INTO `u12254_diplom`.`Chat` (`ID`, `UserID`, `Login`, `Message`) VALUES (NULL, %s, %s, %s);"
        cur.execute(sql, (res['ID'], res['Login'], message)) 
        con.commit()
        con.close()




    ### SELECT получения последних 10 сообщений
    def GetLast10Message(self):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        sql = "SELECT * FROM Chat ORDER BY `ID` DESC LIMIT 10"
        cur.execute(sql)
        arr = list()
        for i in cur:
            arr.append(i)
        res = json.dumps(arr)
        con.commit()
        con.close()
        return res




    ### INSERT генерация лобби
    def GenerateLobby(self, login, correctanswer, gametype, q1, q2, q3, q4, q5):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "INSERT INTO `u12254_diplom`.`Lobby` (`ID`, `FirstPlayer`, `SecondPlayer`, `CorrectAnswerFirstPlayer`, `CorrectAnswerSecondPlayer`, `LobbyOpen`, `GameType`, `Q1`, `Q2`, `Q3`, `Q4`, `Q5`) VALUES (NULL, %s, '', %s, '', '1', %s, %s, %s, %s, %s, %s);"
        cur.execute(sql, (login, correctanswer, gametype, q1, q2, q3, q4, q5))
        res = cur.fetchone()
        con.commit()
        con.close()










    def GenerateLobbyNewWithoutIMG(self, login, mmr, gametype):
            ### Получение вопросов
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        if login == "Random":
            sql = "SELECT `ID` FROM `Task`"
            cur.execute(sql)
        else:
            sql = "SELECT `ID` FROM `Task` WHERE `Type` LIKE %s"
            cur.execute(sql, gametype)

        con.commit()
        con.close()

            ### Выбор 5 вопросов
        tasks = list()
        for i in cur:
            tasks.append(i['ID'])

        res = list()
        for _ in range(5):
            X = random.choice(tasks)
            res.append(X)
            tasks.remove(X)
        

            ### Создание лобби
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "INSERT INTO `u12254_diplom`.`Lobby` (`FirstPlayer`, `FirstMMR`,  `LobbyOpen`, `GameType`, `Q1`, `Q2`, `Q3`, `Q4`, `Q5`) VALUES ( %s, %s,'1', %s, %s, %s, %s, %s, %s);"
        cur.execute(sql, (login, mmr, gametype, res[0], res[1], res[2], res[3], res[4]))
        lastid = con.insert_id()
        con.commit()
        con.close()
        print("!!!!!!!!", mmr)
        return lastid # возврат ID лобби




    def StartLobby(self, lobbyid):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "SELECT `Q1`, `Q2`, `Q3`, `Q4`, `Q5`  FROM `Lobby` WHERE `ID` = %s"
        cur.execute(sql, lobbyid)
        res = cur.fetchone()
        con.commit()
        con.close()
        return res




    def GetLobbyQuestions(self, Questions):
        arr = list()
        for i in range(5):
            con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
            cur = con.cursor()
            sql = "SELECT * FROM `Task` WHERE `ID` = %s"
            cur.execute(sql, Questions[i])
            arr.append(cur.fetchone())
            con.commit()
            con.close()
        return json.dumps(arr)




    def FirstSendLobby(self, lobbyid, answers):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "UPDATE `Lobby` SET `FirstPlayerAns`= %s WHERE `ID` = %s;"
        cur.execute(sql, (answers, lobbyid))
        con.commit()
        con.close()





    def SupGetLobbiesMMR(self, login):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "SELECT `MMR` FROM `Users` WHERE `Login` = %s"
        cur.execute(sql, login)
        mmr = cur.fetchone()
        con.commit()
        con.close()
        return mmr['MMR']

    ### SELECT получения открытых лобби
    def GetLobbies(self, login):

        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "SELECT * FROM `Lobby` WHERE `FirstPlayer` != %s AND `LobbyOpen` = 1"
        cur.execute(sql, login)
        arr = list()
        for i in cur:
            i['MMR'] = self.SupGetLobbiesMMR(i['FirstPlayer'])
            arr.append(i)
        res = json.dumps(arr)
        con.commit()
        con.close()
        return res




    ### INSERT закрытия лобби (ДОБАВИТЬ ИЗМЕНЕНИЯ В ММР!!!)
    def EndLobby(self, login, correctanswer, id):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "UPDATE `Lobby` SET `SecondPlayer`=%s,`CorrectAnswerSecondPlayer`=%s,`LobbyOpen`=0, `MMR`=10 WHERE `ID` = %s"
        cur.execute(sql, (login, correctanswer, id))
        res = cur.fetchone()
        con.commit()
        con.close()






    def Test(self):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        sql = "SELECT * FROM `Task`"
        cur.execute(sql)
        res = cur.fetchone()
        #print(res)
        con.commit()
        con.close()
        return res
