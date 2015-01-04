from ute.model import DB

def openInterval(id, type, desc, open, close = None):
    if id == -1:
        return DB.insert(
            "INSERT INTO interval (id, type, desc, open, close) VALUES (NULL, ?, ?, ?, ?)",
            (type, desc, open, close)
        )
    DB.execute(
        "UPDATE interval SET type=?, desc=?, open=?, close=? WHERE id=?",
        (type, desc, open, close, id)
    )
    return id

def closeInterval(id, close):
    DB.execute(
        "UPDATE interval SET close=? WHERE id=?",
        (close, id)
    )

def getIntervalsAfter(when):
    return DB.query(
        "SELECT id FROM interval WHERE open > ?",
        [when]
    )

def getOpeninterval():
    return DB.query(
        "SELECT * FROM interval WHERE close IS NULL"
    )

def getInterval(id):
    return DB.query1(
        "SELECT * FROM interval WHERE id=?",
        [id]
    )

def getTypes():
    return DB.query(
        "SELECT DISTINCT type FROM interals"
    )
