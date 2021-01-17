import sqlite3

class Connection():
    
    def getConnection():
        connection = sqlite3.connect('example.db')
        return connection
