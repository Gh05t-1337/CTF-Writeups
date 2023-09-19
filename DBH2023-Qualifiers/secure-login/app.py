#!/usr/bin/env python3
from Crypto.Cipher import AES
from flask import Flask, redirect, request, make_response, render_template
import hashlib
import secrets
import base64

app = Flask(__name__)

KEY = secrets.token_bytes(16)


class User:
    def __init__(self, name, password, flag):
        self.username = name
        self.password = hashlib.sha256(password.encode())
        self.flag = flag

    def check(self, pw):
        return hashlib.sha256(pw.encode()) == self.password


users = {}


def add_user(user):
    assert user.username not in users
    users[user.username] = user
    return user


def gen_token(user):
    cipher = AES.new(key=KEY, mode=AES.MODE_GCM)
    ciphertext = cipher.encrypt(user.username.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()


def get_user():
    if 'user' not in request.cookies:
        return None
    ciphertext = base64.b64decode(request.cookies['user'].encode())
    cipher = AES.new(key=KEY, mode=AES.MODE_GCM, nonce=ciphertext[:16])
    user = cipher.decrypt(ciphertext[16:])
    return users[user.decode()]

@app.route('/flag')
def getflag():
    user = get_user()
    if user:
        return user.flag
    else:
        return redirect("/login")

@app.get('/register')
def register_get():
    return render_template("register.html")

@app.post('/register')
def register():
    if 'username' not in request.form or 'password' not in request.form or 'flag' not in request.form:
        return 'Ungültige Anfrage', 400
    username = request.form['username']
    pw = request.form['password']
    flag = request.form['flag']
    if username in users:
        return "Nutzer existiert bereits"
    user = add_user(User(username, pw, flag))
    res = make_response(redirect("/flag"))
    res.set_cookie('user', gen_token(user))
    return res

@app.get('/')
def root():
    return redirect("/login")

@app.get('/login')
def login_get():
    return render_template("login.html")

@app.post('/login')
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return 'Ungültige Anfrage', 400
    user = request.form['username']
    pw = request.form['password']
    if user not in users:
        return "Ungültiger Nutzer"

    if not users[user].check(pw):
        return "Ungültiges Passwort"
    res = make_response(redirect("/flag"))
    res.set_cookie('user', gen_token(users[user]))
    return res


if __name__ == "__main__":
 #   tokn=secrets.token_hex(32)
#    print(tokn)
    with open('flag.txt', 'r') as f:
        add_user(User("admin", secrets.token_hex(32), f.read()))
        add_user(User("admni", secrets.token_hex(32), 'abc'))
    print(gen_token(users["admin"]))
    print(gen_token(users["admni"]))
    app.run(host='0.0.0.0', port=5000)
