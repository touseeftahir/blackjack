import sqlite3
from datetime import datetime
from object import Session


class DBController():
    def __init__(self):
        self.conn = sqlite3.connect("session_db.sqlite")
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS sessions (sessionID INTEGER PRIMARY KEY AUTOINCREMENT, startTime TEXT, startMoney REAL, stopTime TEXT, stopMoney REAL)""")
        self.conn.commit()
        if self.get_last_session() == None:
            self.cur.execute(
                f"INSERT INTO sessions VALUES (0, '{datetime.now()}', 199, '{datetime.now()}', 199)")
            self.conn.commit()

    def get_last_session(self):
        self.cur.execute(
            "SELECT stopMoney as money FROM sessions ORDER BY sessionID DESC")
        stopMoney = self.cur.fetchone()
        if stopMoney != None:
            stopMoney, = stopMoney
        return stopMoney

    def add_session(self, session: Session):
        startMoney = self.get_last_session()
        self.cur.execute(
            "INSERT INTO sessions(startTime, startMoney, stopTime, stopMoney) VALUES(:startTime, :startMoney, :stopTime, :stopMoney)", {'startTime': session.get_start_time(), 'startMoney': startMoney, 'stopTime': datetime.now(), 'stopMoney': session.get_stop_money()})
        self.conn.commit()

    def __del__(self):
        self.conn.close()
