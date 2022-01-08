import sqlite3
from sqlite3 import Error

from helpers.HelperMethods import relationship_status_calculator

class DBClient:
    
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection(self.db_file)

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print('Connected to db | version {}'.format(sqlite3.version))
        except Error as e:
            print(e)

        return conn

    def insert_new_user(self, user):

        sql = ''' INSERT INTO users(id, name)
                VALUES(?, ?) '''

        cur = self.conn.cursor()
        cur.execute(sql, user)
        self.conn.commit()
        return cur.lastrowid

    def create_relationship(self, user1, user2):
        try:
            cur = self.conn.cursor()
            cur.execute('''SELECT * FROM relationships WHERE (user_id_1=? AND user_id_2=?)''', (user1, user2))
            entry = cur.fetchone()

            if entry is None:
                cur.execute('''INSERT INTO relationships (user_id_1, user_id_2, points)
                                VALUES(?, ?, ?)''', (user1, user2, 0))
            else:
                print ('Entry found')
            self.conn.commit()
            return cur.lastrowid
        except Error as e:
            print(e)

    def positive_relationship(self, user1, user2):
        status = ''
        try:
            cur = self.conn.cursor()
            point_data = cur.execute('''SELECT points
                        FROM relationships
                        WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2)).fetchone()
            points = point_data[0]
            if points == 110:
                status = ', Cannot be more than lovers'
            else:
                cur.execute('''UPDATE relationships
                            SET points = points + 10
                            WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2))
                self.conn.commit()
                status = ''
            return status
        except Error as e:
            print(e)
    
    def negative_relationship(self, user1, user2):
        status = ''
        try:
            cur = self.conn.cursor()
            point_data = cur.execute('''SELECT points
                        FROM relationships
                        WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2)).fetchone()
            points = point_data[0]
            print(points)
            if points == -100:
                status = ', Cannot be more than enemies'
            else:
                cur.execute('''UPDATE relationships
                            SET points = points - 10
                            WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2))
                self.conn.commit()
                status = ''
            return status
        except Error as e:
            print(e)

    def relationship_status(self, user1, user2):
        try:
            cur = self.conn.cursor()
            point_data = cur.execute('''SELECT points
                        FROM relationships
                        WHERE user_id_1 = ? AND user_id_2 = ?''', (user1, user2)).fetchone()
            
            points = point_data[0]
            return relationship_status_calculator(points)
        except Error as e:
            print(e)