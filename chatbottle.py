#!/usr/bin/env python3
# pip3 install bottle
from bottle import route, run, template, post, request, redirect
import sqlite3
import os
import datetime
db = sqlite3.connect(":memory:")

conn = db.cursor()
# UTC time, since no timezone conversion here
conn.execute("CREATE TABLE IF NOT EXISTS msgs (msg TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP)")

@route('/hello/<name>')
def hello(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/')
def index():
    conn = db.cursor()
    conn.execute("SELECT msg,ts FROM msgs")
    msgs = [ (row[0],row[1]) for row in conn.fetchall()]
    return template('''
        <title>chatbottle</title>
        <form action=/msg method=post>
        <p>text <input name=text></input></p>
        <input type=submit value=go>
        </form>
        <ul>
          % for item in msgs:
            <code>{{item[1]}}</code><br> <code>
            % if item[0].startswith('https://') or item[0].startswith('http://'):
            <a target=_blank href={{item[0]}}>{{item[0]}}</a>
            % else:
            {{item[0]}}
            % end
            </code>
            <br>
            <hr>
          % end
</ul>
    ''', msgs = msgs)

@post("/msg")
def msg():
    text = request.forms.get('text')
    conn = db.cursor()
    conn.execute("INSERT INTO msgs (msg) VALUES (?)", (text,))
    return redirect('/')

host = '0.0.0.0'

if os.getenv("DEBUG"):
    run(host='127.0.0.1', port=7000,debug=True)
else:
    run(host='0.0.0.0', port=7000)