import sqlite3
from pathlib import Path
from typing import Dict


class sqlite3(object):
    def __init__(self, database_path=None):

        if not database_path:
            database_path = str(Path.home())

        self.conn = sqlite3.connect(database_path / 'jocasta.db')

    def send(self, data: Dict) -> bool:
        """
        Write data as JSON to file.
        """

        c = self.conn.cursor()

        # Create table
        for field, value in data:

            c.execute(
                '''CREATE TABLE stocks
                         (date text, trans text, symbol text, qty real, price real)'''
            )

        # Insert a row of data
        c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

        # Save (commit) the changes
        self.conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.conn.close()

        return True
