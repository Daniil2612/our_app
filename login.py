
from concurrent.futures import process, thread 
from db import * 
import classes 
 
from flask import Flask, request, render_template, redirect, jsonify, url_for, session 
from flask_socketio import SocketIO, emit 
import sqlite3 
 
 
 
 
app = Flask(__name__) 
socketio = SocketIO(app) 
app.secret_key = "super secret key" 
 
@app.route('/') 
def profile(): 
    return render_template('profile.html')  
 
@app.route('/add_card') 
def call_add_card(): 
    add_card() 
    return 'add_card called' 
 
@app.route('/submitParams', methods=['POST', 'GET']) 
def submit_params(): 
    data = request.get_json() 
    action = data['action'] 
    subject = data['subject'] 
    term = data['term'] 
    meaning = data['meaning'] 
 
    if action == 'add_card': 
        add_card(session['login'], subject, term, meaning) 
        return 'card added' 
    elif action == 'add_subject': 
        add_subject(session['login'], subject) 
        return 'subject added' 
    else: 
        return 'Invalid action' 
 
@app.route('/authorization', methods=['GET', 'POST']) 
# def form_authorization(): 
#    if request.method == 'POST': 
#        Login = request.form.get('Login') 
#        Password = request.form.get('Password') 
 
#        db_lp = sqlite3.connect('login_password.db') 
#        cursor_db = db_lp.cursor() 
#        cursor_db.execute(('''SELECT password FROM passwords 
#                                                WHERE login = '{}'; 
#                                                ''').format(Login)) 
#        pas = cursor_db.fetchall() 
#        if pas [0][0] == Password: 
#            return redirect('/profile') 
#        cursor_db.close() 
#        try: 
#            if pas[0][0] != Password: 
#                return render_template('auth_bad.html') 
#        except: 
#            return render_template('auth_bad.html') 
 
#        db_lp.close() 
#        return render_template('successfulauth.html') 
 
#    return render_template('authorization.html') 
 
def form_authorization(): 
    if request.method == 'POST': 
        Login = request.form.get('Login') 
        Password = request.form.get('Password') 
 
        db_lp = sqlite3.connect('login_password.db') 
        cursor_db = db_lp.cursor() 
        cursor_db.execute(('''SELECT password FROM passwords 
                                           WHERE login = '{}'; 
                                           ''').format(Login)) 
        pas = cursor_db.fetchall() 
        if pas and pas[0][0] == Password: 
            session['login'] = Login  # Сохранение логина пользователя в сессии 
            cursor_db.close() 
            db_lp.close() 
            return redirect('/profile') 
        cursor_db.close() 
        db_lp.close() 
        try: 
            if pas[0][0] != Password: 
                return render_template('auth_bad.html') 
        except: 
            return render_template('auth_bad.html') 
 
    return render_template('authorization.html') 
 
@app.route('/registration', methods = ['GET', 'POST']) 
def registration(): 
    if request.method == "POST": 
        Login = request.form.get('Login') 
        Password = request.form.get('Password') 
        crd = () 
 
        db_lp = sqlite3.connect('login_password.db') 
        cursor_db = db_lp.cursor() 
        sql_insert = '''INSERT INTO passwords VALUES('{}','{}', '{}');'''.format(Login, Password, crd) 
 
        cursor_db.execute(sql_insert) 
 
        cursor_db.close() 
 
        db_lp.commit() 
        db_lp.close() 
        # return render_template('successfulregis.html') 
        return redirect('/authorization') 
     
 
    return render_template('registration.html') 
 
# �������� ��������(������� ��������) 
 
@app.route('/profile', methods = ['GET', 'POST']) 
def info(): 
    if request.method == 'POST': 
            if 'singleplayer' in request.form: 
            # Handle singleplayer button click 
                return redirect('/singleplayer')  # Redirect to singleplayer route 
            elif 'multiplayer' in request.form: 
            # Handle multiplayer button click
                return redirect('/research_of_game') 
    return render_template('profile.html') 
 
 
 
questions = { 
    1: {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin"], "answer": "Paris"}, 
    2: {"question": "What is the largest planet in our solar system?", "options": ["Jupiter", "Saturn", "Mars"], "answer": "Jupiter"}, 
    # �������� ������ �������� ����� 
} 
 
# ��������� ���� 
 
user_scores = {} 
 
@app.route('/competition/singleplayer') 
def singleplayer_route():    
    return render_template('index.html') 
 
@app.route('/get_question', methods=['POST']) 
def get_question(): 
    question_id = int(request.json['question_id']) 
    question = questions[question_id] 
    return jsonify(question) 
 
@app.route('/check_answer', methods=['POST']) 
def check_answer(): 
    question_id = int(request.json['question_id']) 
    answer = request.json['answer'] 
    correct_answer = questions[question_id]["answer"] 
    return jsonify({"result": answer == correct_answer}) 
 
# ������ (������ ��� ���������� �������������) 
 
user_scores = {} 
 
@socketio.on('connect') 
def handle_connect(): 
    emit('question', questions[1]) 
 
@socketio.on('answer') 
def handle_answer(data): 
    question_id = data['question_id'] 
    answer = data['answer'] 
    correct_answer = questions[question_id]["answer"] 
    if answer == correct_answer: 
        user_id = data['user_id'] 
        if user_id not in user_scores: 
            user_scores[user_id] = 0 
        user_scores[user_id] += 1 
        emit('result', {'result': 'Correct!'}) 
        emit('score', {'user_id': user_id, 'score': user_scores[user_id]}) 
    else: 
        emit('result', {'result': 'Incorrect!'}) 
 
 
# �������� ����� 
lobbies = {} 
 
@app.route('/research') 
def index(): 
    return render_template('lobby.html', lobbies=lobbies) 
 
@app.route('/create_lobby', methods=['POST']) 
def create_lobby(): 
    lobby_name = request.form['lobby_name'] 
    lobbies[lobby_name] = [] 
    return redirect(url_for('lobby')) 
 
@app.route('/join_lobby', methods=['POST']) 
def join_lobby(): 
    lobby_name = request.form['lobby_name'] 
    player_name = request.form['player_name'] 
     
    lobbies[lobby_name].append(player_name) 
     
    return redirect(url_for('lobby')) 
 
# ������ ������������ 
   
@app.route('/competition/multiplayer') 
def multiplayer_route(): 
    # Code for multiplayer route 
    print( "You have selected multiplayer mode.") 
    return render_template('miltuplay.html') 
 
 
if __name__ == "__main__": 
   socketio.run(app, host = '0.0.0.0', port = 8080, debug=True)