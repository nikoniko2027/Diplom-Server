import pymysql


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
        sql = "INSERT INTO `u12254_diplom`.`Users` (`ID`, `Login`, `Password`, `Email`, `MMR`) VALUES (NULL, %s, %s, %s, '1000')"
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
        print(res["Password"])
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




    ### SELECT получения Login + MMR пользователя по UUID
    def GetUserInfoWithUUID(self, myuuid):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        sql = "SELECT `ID`, `MMR`, `Login`, `UUID`, `Email` FROM `Users` WHERE `UUID` = %s"
        cur.execute(sql, myuuid)
        res = cur.fetchone()
        con.commit()
        con.close()
        return res

        
        

    ### INSERT uuid пользователя при авторизации
    def UserUUID(self, login, uuid):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        sql = "UPDATE `Users` SET `UUID`=%s WHERE `Login` = %s"
        cur.execute(sql, (uuid, login)) 
        res = cur.fetchone()
        con.commit()
        con.close()




    ### Для выполнения сторонних команд SQL
    def SQLexecute(command):
        con = pymysql.connect(host=Host, user=User, password=Pass, database=DB, cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        try:
            cur.execute(command)
            con.commit()
            con.close()
            return "Successful execution", 200 # Успешное выполнение
        except:
            con.close()
            return "Unsuccessful execution", 403 # Неуспешное выполнение