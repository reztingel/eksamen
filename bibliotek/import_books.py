import csv
import sqlite3  # eller en annen databaseconnector du bruker

# Tilpass tilkoblingen til din database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Opprett tabellen hvis den ikke eksisterer
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    tittel TEXT NOT NULL,
    forfatter TEXT NOT NULL,
    isbn TEXT NOT NULL,
    nummer INTEGER NOT NULL
)
''')

# Les og importer CSV-filen
with open('bøker.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
        INSERT INTO books (tittel, forfatter, isbn, nummer)
        VALUES (?, ?, ?, ?)
        ''', (row['tittel'], row['forfatter'], row['isbn'], row['nummer']))

conn.commit()
conn.close()