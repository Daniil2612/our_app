import sqlite3 
import json 
import random 
 
def add_card(login : int, subject : str, term : str, meaning : str): 
    db_lp = sqlite3.connect('login_password.db') 
    cursor_db = db_lp.cursor() 
    cursor_db.execute('SELECT cards from passwords WHERE login = ?', (login,)) 
    req_res = cursor_db.fetchone() 
 
    if req_res: 
        d = json.loads(req_res[0]) 
    else: 
        d = {} 
 
    if subject in d: 
        if term not in d[subject]: 
            d[subject][term] = meaning 
        else: 
            pass 
    else: 
        d[subject] = {} 
        d[subject][term] = meaning         
         
 
    cursor_db.execute('UPDATE passwords SET cards = ? WHERE login = ?', (json.dumps(d), login)) 
    db_lp.commit() 
    cursor_db.close() 
    db_lp.close() 
 
     
 
def add_subject(login : int, subject : str): 
    db_lp = sqlite3.connect('login_password.db') 
    cursor_db = db_lp.cursor() 
    cursor_db.execute('SELECT cards from passwords WHERE login = ?', (login,)) 
    req_res = cursor_db.fetchall() 
    d = json.loads(req_res) 
    if subject in d: 
        pass 
    else: 
        d[subject] = {} 
 
    cursor_db.execute('UPDATE passwords SET cards = ? WHERE login = ?', (json.dumps(d), login)) 
    db_lp.commit() 
    cursor_db.close() 
    db_lp.close() 
 
def delete_card(login : int, subject : str, term : str): 
    db_lp = sqlite3.connect('login_password.db') 
    cursor_db = db_lp.cursor() 
    cursor_db.execute('SELECT cards from passwords WHERE login = ?', (login,)) 
    req_res = cursor_db.fetchone() 
    d = json.loads(req_res) 
 
    if subject in d: 
        if term in d[subject]: 
            d[subject].pop(term) 
        else: 
            pass 
    else: 
        pass 
     
    cursor_db.execute('UPDATE passwords SET cards = ? WHERE login = ?', (json.dumps(d), login)) 
    db_lp.commit() 
    cursor_db.close() 
    db_lp.close() 
 
def delete_subject(login : int, subject : str): 
    db_lp = sqlite3.connect('login_password.db') 
    cursor_db = db_lp.cursor() 
    cursor_db.execute('SELECT cards from passwords WHERE login = ?', (login,)) 
    req_res = cursor_db.fetchone() 
    d = json.loads(req_res) 
 
    if subject in d: 
        d.pop(subject) 
    else: 
        pass 
     
    cursor_db.execute('UPDATE passwords SET cards = ? WHERE login = ?', (json.dumps(d), login)) 
    db_lp.commit() 
    cursor_db.close() 
    db_lp.close() 
 
 
 
def all_subjects(login : int) -> list: 
    db_lp = sqlite3.connect('login_password.db') 
    cursor_db = db_lp.cursor() 
    cursor_db.execute('SELECT cards from passwords WHERE login = ?', (login,)) 
    req_res = cursor_db.fetchall() 
    d = json.loads(req_res) 
    db_lp.commit() 
    cursor_db.close() 
    db_lp.close() 
 
    return list(d.keys()) 
 
def all_subj_cards(login : int, subject : str) -> dict: 
    db_lp = sqlite3.connect('login_password.db') 
    cursor_db = db_lp.cursor() 
    cursor_db.execute('SELECT cards from passwords WHERE login = ?', (login,)) 
    req_res = cursor_db.fetchall() 
    d = json.loads(req_res) 
    db_lp.commit() 
    cursor_db.close() 
    db_lp.close() 
 
    if subject in list(d.keys()): 
        return d[subject]  
    else: 
        pass 
 
def all_cards(login : int) -> dict: 
    db_lp = sqlite3.connect('login_password.db') 
    cursor_db = db_lp.cursor() 
    cursor_db.execute('SELECT cards from passwords WHERE login = ?', (login,)) 
    req_res = cursor_db.fetchall() 
    d = json.loads(req_res) 
    db_lp.commit() 
    cursor_db.close() 
    db_lp.close() 
 
    res = {} 
 
    for key in list(d.keys()): 
        res.update(d[key]) 
    return res 
 
def flip_dict(d : dict) -> dict: 
    flipped = {j : i for i, j in d.items()} 
    return flipped 
 
def quiz(login: int, subject : str, quiz_mode : str, quiz_length : int) -> dict:    
    # возможные значения quiz_mode : term, meaning 
    d = all_subj_cards(login, subject) 
    l = list(d.items()) 
    random.shuffle(l) 
    d_shuffled = dict(l) 
    res = {} 
    m = min(quiz_length, len(l)) 
    count = 0 
    if quiz_mode == "meaning":
        for i in l: 
            if (count < m): 
                res[i[0]] = i[1] 
            else: 
                break 
    else: 
        for i in l: 
            if (count < m): 
                res[i[1]] = i[0] 
            else: 
                break 
    return {i : {"question" : key, "answer" : res[key]} for (i, key) in enumerate(res, start = 1)} 
     
 
db_lp = sqlite3.connect('login_password.db') 
cursor_db = db_lp.cursor() 
sql_create = '''CREATE TABLE passwords( 
login TEXT PRIMARY KEY, 
password TEXT NOT NULL, 
cards TEXT);''' 
 
#cursor_db.execute(sql_create) 
db_lp.commit() 
 
cursor_db.close() 
db_lp.close()