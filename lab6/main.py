from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect('answer.db', check_same_thread=False)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Paste(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT);''')
conn.commit()

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/paste/{paste_id}')
def get_paste(paste_id: int):
    res = cur.execute('''SELECT ID, content
                      FROM Paste
                      WHERE ID = ?''', (paste_id,))
    data = res.fetchone()
    if data is not None:
        paste = Paste(content=data[1])
        return {'paste_id': data[0],
                'paste': paste}
    else:
        return {'paste_id': paste_id, 
                'paste': None}

class Paste(BaseModel):
    content: str

@app.post('/paste/')
def post_paste(paste: Paste):
    cur.execute('''INSERT INTO Paste (content) VALUES (?)''', (paste.content, ))
    conn.commit()
    paste_id = cur.lastrowid
    return {'paste_id': paste_id, 'paste': paste}


@app.put('/paste/{paste_id}')
def put_paste(paste_id: int, paste: Paste):
    res = cur.execute('''SELECT ID FROM Paste WHERE ID = ?''', (paste_id, ))
    data = res.fetchone()
    if data is not None:
        cur.execute('''UPDATE Paste SET content = ? WHERE ID = ?''', (paste.content, paste_id))
        conn.commit()
        return {'paste_id': paste_id, 'paste': paste}
    else:
        return {'paste_id': paste_id, 'paste': None}
    

@app.delete('/paste/{paste_id}')
def delete_paste(paste_id: int):
    res = cur.execute('''SELECT ID FROM Paste WHERE ID = ?''', (paste_id, ))
    data = res.fetchone()
    if data is not None:
        cur.execute('''DELETE FROM Paste WHERE ID = ?''', (paste_id,))
        conn.commit()
        return {'paste_id': paste_id, 'paste': Paste(content=data[1])}
    else:
        return {'paste_id': paste_id, 'paste': None}