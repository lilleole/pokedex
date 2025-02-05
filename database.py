import sqlite3 as lite
import json


class Database:
    def __init__(self):
        self.added = 0
        try:
            # Connect to DB and create a cursor
            self.connection = lite.connect('sql.db')
            self.cursor = self.connection.cursor()
            print('DB Init')

            # Write a query and execute it with cursor
            query = 'SELECT sqlite_version();'
            self.cursor.execute(query)

            # Fetch and output result
            result = self.cursor.fetchall()
            print(f'SQLite Version is {result}')

        # Handle errors
        except lite.Error as error:
            print('Error occurred -', error)

    def createTable(self):
        try:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS pokemon (
                    id          INTEGER PRIMARY KEY NOT NULL,
                    NAME        TEXT    NOT NULL,
                    TYPE        TEXT    NOT NULL,
                    TOTAL       INTEGER NOT NULL,
                    HP          INTEGER NOT NULL,
                    ATTACK      INTEGER NOT NULL,
                    DEFENSE     INTEGER NOT NULL,
                    SP_ATTACK   INTEGER NOT NULL,
                    SP_DEFENSE  INTEGER NOT NULL,
                    SPEED       INTEGER NOT NULL,
                    Match_UP    TEXT    NOT NULL
                );
            ''')
            self.connection.commit()  # Commit changes
            print("Table created successfully!")

        except lite.Error as error:
            print("Error occurred while creating the table -", error)

    def insertPokemon(self, data):
        try:
            self.cursor.execute("SELECT id FROM pokemon WHERE id = ?", (data['id'],))
            exists = self.cursor.fetchone()

            if exists:
                print(f"Pokémon with ID {data['id']} ({data['NAME']}) already exists. Skipping insertion.")
                return
            # Convert Match_UP dictionary to JSON string
            data['Match_UP'] = json.dumps(data['Match_UP'])

            self.connection.execute('''
                INSERT INTO pokemon (id, NAME, TYPE, TOTAL, HP, ATTACK, DEFENSE, SP_ATTACK, SP_DEFENSE, SPEED, Match_UP)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', (
                data['id'], data['NAME'], data['TYPE'], data['TOTAL'],
                data['HP'], data['ATTACK'], data['DEFENSE'],
                data['SP_ATTACK'], data['SP_DEFENSE'], data['SPEED'],
                data['Match_UP']
            ))

            self.connection.commit()
            self.added += 1
            print(f"Inserted Pokemon {data['NAME']} successfully!")

        except lite.Error as error:
            print("Error occurred while inserting data -", error)

    def close(self):
        if self.connection:
            self.connection.close()
            print('Database connection closed.')

