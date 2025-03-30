import pymysql

def connection():
    try:
        db = pymysql.connect( host='127.0.0.1', 
                             port=3306,user='root', 
                             password=open('password','r').read(),
                             db = 'boards')
                                
        return db
    
    except :
        pass


def sign_up_check(cursor,column,check_item):

    db = connection()
    cursor = db.cursor()

    query = f"SELECT * FROM users WHERE {column} = %s;"

    cursor.execute(query,(check_item,))
    user_data = cursor.fetchone()

    cursor.close()
    return user_data


def login_check(cursor, column_1, column_2, id, password):

    db = connection()
    cursor = db.cursor()

    query = f"SELECT * FROM users WHERE {column_1} = %s AND {column_2} = %s;"

    user_data = cursor.execute(query,(id,password,))

    cursor.close()

    if user_data:
        result = "로그인에 성공하셨습니다."

        return result

    else:
        result = "로그인에 실패하셨습니다."

        return result


