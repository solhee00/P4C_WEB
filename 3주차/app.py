from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd="snowsolhee^^",
    db='boards'
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS boards")
cursor.execute("USE boards")

sql = """
CREATE TABLE IF NOT EXISTS boards (
    idx INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT
)
"""
cursor.execute(sql)

db.commit()

cursor.close()
db.close()

@app.route('/index', methods=['GET', 'POST'])
def index() :
    global data

    with pymysql.connect(host = "127.0.0.1", 
                        port=3306,
                        user='root',
                        passwd='snowsolhee^^',
                        db = 'boards') as db:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM boards")
            data = cursor.fetchall()

    return render_template('index.html', data = data)


@app.route('/write', methods=['GET', 'POST'])
def write() :

    if request.method == "POST":
        title = request.form.get('title')
        comment = request.form.get('comment')

        print(title, comment)

        sql_template = "insert into boards (title, content) values(%s, %s);"
        with pymysql.connect(host = "127.0.0.1", 
                        port=3306,
                        user='root',
                        passwd='snowsolhee^^',
                        db = 'boards') as conn:
            
            with conn.cursor() as cursor:
                cnt = cursor.executemany(sql_template, [(title, comment)])
                print("insert 갯수:", cnt)
                conn.commit()

        return redirect(url_for('index'))
    
    return render_template('write.html')
   

@app.route('/view', methods=['GET', 'POST'])
def view() :
    t = None

    with pymysql.connect(host = "127.0.0.1", 
                        port=3306,
                        user='root',
                        passwd='snowsolhee^^',
                        db = 'boards') as db:
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM boards WHERE idx = %s;",(request.args.get('id')))
            data = cursor.fetchone()

            print(data)
        '''
            for i in range(1, len(data)):
                if data[i][0] == i:
                    cursor.execute("SELECT * FROM boards WHERE idx = %s;",(i))
                    t = cursor.fetchone()
'''

    return render_template('view.html', t=data)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    with pymysql.connect(host = "127.0.0.1", 
                    port=3306,
                    user='root',
                    passwd='snowsolhee^^',
                    db = 'boards') as db:
        
        with db.cursor() as cursor:

            a = int(request.args.get('id'))

            cursor.execute("DELETE FROM boards WHERE idx = %s;",(a))
            db.commit()

        return redirect(url_for('index'))
    
    return render_template('delete.html')



@app.route('/modify', methods=['GET', 'POST'])
def modify():

    if request.method == "GET":
        with pymysql.connect(host = "127.0.0.1", 
                        port=3306,
                        user='root',
                        passwd='snowsolhee^^',
                        db = 'boards') as db:
            
            with db.cursor() as cursor:

                cursor.execute("SELECT * FROM boards WHERE idx = %s", request.args.get('id'))

                data = cursor.fetchone()
                

                return render_template('modify.html', a=data)

    if request.method == "POST":
        

        new_title = request.form.get('title')
        new_comment = request.form.get('comment')

        # sql_template = "UPDATE boards SET %s, %s WHERE %s %s;",(title, comment)
        
        with pymysql.connect(host = "127.0.0.1", 
                        port=3306,
                        user='root',
                        passwd='snowsolhee^^',
                        db = 'boards') as db:
            
            with db.cursor() as cursor:

                a = int(request.args.get('id'))

                cursor.execute("UPDATE boards SET title = %s, content = %s WHERE idx = %s;",(new_title, new_comment, a))
                db.commit()
                print(a, new_comment)
            return redirect(url_for('index'))
            
    return render_template('modify.html', a=data)


@app.route('/search', methods=['GET'])
def search():
    # if request.method == "POST":

    keyword = request.args.get('keyword')
    data = None


    # sql_template = "UPDATE boards SET %s, %s WHERE %s %s;",(title, comment)
    
    with pymysql.connect(host = "127.0.0.1", 
                    port=3306,
                    user='root',
                    passwd='snowsolhee^^',
                    db = 'boards') as db:
        
        with db.cursor() as cursor:

            a = request.args.get('search_option')

            if a == 'title':
    
                cursor.execute("SELECT * FROM boards WHERE title=%s;", (keyword))
                data = cursor.fetchall()
                db.commit()

            if a == 'content':
    
                cursor.execute("SELECT * FROM boards WHERE content LIKE %s;", (f"%{keyword}%",))
                data = cursor.fetchall()
                db.commit()

            return render_template('search.html', data=data)
    return redirect(url_for('index'))
            




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)