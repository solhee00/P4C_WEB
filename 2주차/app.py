from flask import Flask, render_template, request
from module import sign_upup
from module import loginin
from module import deldel_user

app = Flask(__name__)

file = open("user_file.txt", "a")

user_information = []
def load_user_information():
    global user_information 
    with open("user_file.txt", "r") as file:
        user_information = file.readlines()

    for i in range(len(user_information)):
        user_information[i] = user_information[i].strip()

    for i in range(len(user_information)):
        user_information[i] = user_information[i].split()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = None
    user_password = None
    result = " "

    if request.method == 'POST':
        user_id = request.form.get('id')
        user_password = request.form.get('password')

        load_user_information()

        result = loginin(len(user_information), user_information, user_id, user_password)


    return render_template('login.html', ss=result)



@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    user_id = None
    user_password = None
    result = " "

    if request.method == 'POST':
        user_id = request.form.get('id')
        user_password = request.form.get('password')
        
        load_user_information()
        
        result = sign_upup(len(user_information), user_information, user_id, user_password)

    print(user_id)
    print(user_password)

    return render_template('sign_up.html', ss=result)



@app.route('/del_user', methods=['GET', 'POST'])
def del_user():
    user_id = None
    user_password = None
    result = " "

    if request.method == 'POST':
        user_id = request.form.get('id')
        user_password = request.form.get('password')

        load_user_information()

        result = deldel_user(len(user_information), user_information, user_id, user_password)


    return render_template('del_user.html', ss=result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)




