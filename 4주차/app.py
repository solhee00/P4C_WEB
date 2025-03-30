from flask import Flask , render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

from module import connection
from module import sign_up_check
from module import login_check


import os 
import pymysql # 모듈 import

app = Flask(__name__)

app.secret_key = os.urandom(24)

UPLOAD_FOLDER = "4주차/static/images"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.chmod(UPLOAD_FOLDER, 0o777)  # 쓰기 권한 부여

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = pymysql.connect( host='127.0.0.1', 
        port=3306, 
        user='root',
        passwd='snowsolhee^^',
        db='boards'
    ) # boards 데이터베이스 연결

cursor = db.cursor() # cursor 객체를 만들어 객체를 통해 데이터베이스의 데이터에 접근
cursor.execute("CREATE DATABASE IF NOT EXISTS boards")
cursor.execute("USE boards")

# sql 쿼리 작성
# CREATE TABLE : 새로운 테이블을 생성 
# IF NOT EXISTS : 같은 이름의 테이블 ( boards )이 존재하지 않을 때만 생성
# boards 는 테이블 이름
# idx INT AUTO_INCREMENT PRIMARY KEY -> idx는 테이블의 기본 키 역할을 하는 컬럼(열)이며 이는 정수이고 새로 레코드가 삽입될 때마다 자동으로 1씩 증가
# title VARCHAR (100) NOT NULL -> title은 게시글의 제목을 저장하며 최대 100자 까지 저장가능하고, NULL값이면 안됨. 즉 반드시 값이 입력되어야함
# content TEXT -> 게시글의 내용을 저장하며 긴 문자열을 저장할 수 있는 데이터 타입인 TEXT타입으로 선언
boards_sql = """
CREATE TABLE IF NOT EXISTS boards ( 
    idx INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR (100) NOT NULL,
    content TEXT,
    board_file VARCHAR (255),
    writer VARCHAR (100),
    writer_idx VARCHAR (500),
    post_password VARCHAR(255)
)
"""
cursor.execute(boards_sql) # sql 쿼리 실행

user_sql = """
CREATE TABLE IF NOT EXISTS boards (
    idx INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR (100) NOT NULL,
    user_password VARCHAR (100) NOT NULL,
    user_name VARCHAR (10) NOT NULL,
    user_school VARCHAR (100) NOT NULL,
    profile_img VARCHAR (255) DEFAULT 'cat.jpg'
)
"""
cursor.execute(user_sql)

db.commit() # 수정 사항 db에 저장

cursor.close()
db.close() # db 닫기기


@app.route('/', methods=['GET', 'POST'])
def home(): # home.html (게시글 목록)페이지에 접속시 실행되는 코드
    global data # data변수를 global을 이용해 전역변수로 만들어줌

    db = connection() # db를 연결하는 모듈을 실행 connection() <- db연결 모듈듈
    cursor = db.cursor() # cursor이라는 객체를 만들어 이를 이용해 db에 접근

    cursor.execute("SELECT * FROM boards") 
    data = cursor.fetchall() 

    cursor.execute("SELECT * FROM users")
    user_data = cursor.fetchall()

    cursor.close()
    db.close()


    if 'user_id' not in session:
        return render_template('logout.html')

    return render_template('home.html', data = data, user_data=user_data)


@app.route('/login', methods=['GET', 'POST'])
def login():

    user_id = None
    user_password = None 
    result = ""

    if request.method == 'POST':
        user_id = request.form.get('id')
        user_password = request.form.get('password')

        db = connection()
        cursor = db.cursor()

        result = login_check(cursor,"user_id","user_password",user_id,user_password)

        if result == "로그인에 성공하셨습니다.":
            session['user_id'] = user_id
        
            return redirect(url_for('home'))

        db.commit()
        cursor.close()
        db.close()


    return render_template('login.html', result = result)

@app.route('/logout', methods = ['GET','POST'])
def logout():
    session.clear()

    return render_template('logout.html')


@app.route('/post_modify', methods=['GET','POST'])
def post_modify():

    if request.method == "GET":

        db = connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM boards WHERE idx = %s", request.args.get('id'))
    
        data = cursor.fetchone()

        cursor.close()
        db.close()

        return render_template('post_modify.html', a = data)
    
    if request.method == "POST":

        new_title = request.form.get('title')
        new_contents = request.form.get('contents')

        db = connection()
        cursor = db.cursor()

        a = int(request.args.get('id'))
        cursor.execute("UPDATE boards SET title = %s, content = %s WHERE idx = %s;",(new_title, new_contents, a))

        db.commit()
        print(a,new_title, new_contents)

        cursor.close()
        db.close()

        return redirect(url_for('home'))


    return render_template('post_modify.html', a=data)

@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    user_id = None
    user_password = None 

    result = ''

    if request.method == "POST":
        user_id = request.form.get('id')
        user_password = request.form.get('password')
        user_name = request.form.get('name')
        user_school = request.form.get('school')

        if user_id or user_password or user_name or user_school == "":
            result = "입력되지 않은 값이 있습니다. 입력해주세요"

            return render_template('sign_up.html', result=result)
        
        db = connection()
        cursor = db.cursor()

        user_data = sign_up_check(cursor,"user_id", user_id)
        if user_data:
            result = f"{user_id}는(은) 이미 존재하는 id입니다. 다시 입력해주세요."
            
            return render_template('sign_up.html',result=result)

        cursor.execute("insert into users (user_id,user_password,user_name,user_school) values(%s,%s,%s,%s);", (user_id, user_password, user_name, user_school))

        db.commit()
        cursor.close()
        db.close()

        print(user_id,user_password,user_name,user_school)

        return redirect(url_for('login'))


    return render_template('sign_up.html')

@app.route('/view', methods=['GET', 'POST'])
def view():
    t = None

    db = connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM boards WHERE idx = %s;", (request.args.get('id')))
    data = cursor.fetchone()

    cursor.close()
    db.close()

    print(data)

    return render_template('view.html', t=data)

@app.route('/secret_view', methods=['GET','POST'])
def secret_view():

    if 'user_id' not in session:
        return render_template('logout.html')
    
    db = connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM boards WHERE idx = %s;", (request.args.get('id'),))
    data = cursor.fetchone()

    cursor.close()
    db.close()

    if not data[6]:
        return render_template('view.html', t=data)
    
    if request.method == "POST":
        password = request.form.get('post_password')

        if data[6] == password:
            return render_template('view.html', t=data)

        else:
            redirect(url_for('home'))

    return render_template('secret_view.html', t=data)

@app.route('/write', methods=['GET', 'POST'])
def write():

    if 'user_id' not in session:
        return render_template('logout.html')

    if request.method == "POST":
        title = request.form.get("title")
        contents = request.form.get("contents")

        print(title, contents)

        db = connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = %s",(session['user_id'],))
        user_data = cursor.fetchone()

        writer = user_data[1]
        writer_idx = user_data[0]

        print(writer)

        cursor.execute("insert into boards (title,content,writer,writer_idx) values(%s, %s, %s, %s);", (title, contents, writer,writer_idx))

        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('home'))
        
    return render_template('write.html')

@app.route('/secret_write', methods=['GET','POST'])
def secret_write():
    if 'user_id' not in session:
        return render_template('logout.html')

    if request.method == "POST":
        title = request.form.get("title")
        contents = request.form.get("contents")
        post_password = request.form.get("post_password") 

        print(title, contents, post_password)

        db = connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = %s",(session['user_id'],))
        user_data = cursor.fetchone()
        writer = user_data[1]
        writer_idx = user_data[0]

        print(writer)

        cursor.execute("INSERT INTO boards (title, content, writer, writer_idx, post_password) VALUES (%s, %s, %s, %s, %s)",(title, contents, writer, writer_idx, post_password))

        print(post_password)

        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('home'))
        
    return render_template('secret_write.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if 'user_id' not in session:
        return render_template('logout.html')
    
    #user_id = request.args.get('user_id')
    
    db = connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users WHERE user_id = %s",(session['user_id'],))
    #cursor.execute("SELECT * FROM users WHERE user_id=%s",(user_id,))
    user_data = cursor.fetchone()
    print(user_data)

    if request.method == 'POST':
        file = request.files['file']

        db = connection()
        cursor = db.cursor()

        if file and allowed_file(file.filename): 
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            
            print(f'파일 저장 경로: {file_path}')

            file.save(file_path)

            # DB에 파일 경로 저장
            if 'user_id' in session:
                sql = "UPDATE users SET profile_img = %s WHERE user_id = %s"
                cursor.execute(sql, (file.filename, session['user_id']))

            cursor.execute("SELECT * FROM users WHERE user_id = %s",(session['user_id'],))
            user_data = cursor.fetchone()
                
            db.commit()
            cursor.close()
            db.close()

        return render_template('profile.html', user_data=user_data)
    
    return render_template('profile.html', user_data=user_data)

@app.route('/profile_modify', methods=['GET', 'POST'])
def profile_modify():
    
    if request.method == "GET":
        db = connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = %s",(session['user_id'],))
        user_data = cursor.fetchone()

        cursor.close()
        db.close()

        return render_template('profile_modify.html', user_data=user_data)
    
    if request.method == "POST":

        new_name = request.form.get('user_name')
        new_school = request.form.get('user_school')

        db = connection()
        cursor = db.cursor()

        if 'user_id' in session:
            sql = "UPDATE users SET user_name = %s, user_school = %s WHERE user_id = %s;"
            cursor.execute(sql, (new_name,new_school,session['user_id']))

        db.commit()
        print(new_name,new_school)

        cursor.close()
        db.close()

        return redirect(url_for('home'))

    return render_template('profile_modify.html', user_data=user_data)


@app.route('/user_profile', methods=['GET','POST'])
def user_profile():

    user_id = request.args.get('id')

    print(user_id)

    db = connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE idx = %s;", (user_id,))
    data = cursor.fetchone()

    cursor.close()
    db.close()

    print(data)
    return render_template('user_profile.html', data=data)

@app.route('/find_id', methods=['GET','POST'])
def find_id():
    result = None

    if request.method == "POST":
        name = request.form.get('name')
        school = request.form.get('school')

        db = connection()
        cursor = db.cursor()

        cursor.execute("SELECT user_id FROM users WHERE user_name = %s AND user_school = %s", (name, school))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            result = f"아이디는 {user[0]} 입니다."
        else:
            result = "일치하는 사용자가 없습니다."
    
    return render_template('find_id.html', result=result)

@app.route('/find_password', methods=["GET",'POST'])
def find_password():

    result = None

    if request.method == "POST":
        id = request.form.get('id')
        name = request.form.get('name')
        school = request.form.get('school')

        db = connection()
        cursor = db.cursor()

        cursor.execute("SELECT user_password FROM users WHERE user_id = %s AND user_name = %s AND user_school = %s", (id,name, school))
        user = cursor.fetchone()

        print(user)

        cursor.close()
        db.close()

        if user:
            result = f"비밀번호는 {user[0]} 입니다."
        else:
            result = "일치하는 사용자가 없습니다."

    return render_template('find_password.html', result=result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)



# mysql을 연결하기 위해 mysql도 다운로드 받아야함 이를 다운로드 받고 sql workbencher을 이용해 데이터베이스를 실시간으로 확인하며 작업하였다. 
# sql 워커벤처를 사용하는 과정에서 제대로 연결이 되었는지 확인해야한다. 
# 또한 자잘한 sql쿼리문의 오타나 프로그램을 작성하며 생기는 오타를 유의해서 살펴볼것. ( 오타로 인한 오류가 굉장히 많이 난다.. )
# 또한 중간중간 프로그래밍을 할 때 오류를 확인하기 위해 디버깅을 이용한다. 
# print()를 이용해 내가 받고자 한 값을 제대로 받았는지, 내가 보내고자한 값이 제대로 보내졌는지 어느 부분에서 오류가 났는지 확인하기 위해 이를 사용하면 편하다
