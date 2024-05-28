import sqlite3


con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()


cur.execute("""CREATE TABLE IF NOT EXISTS bøker(
            tittel TEXT,
            forfatter TEXT,
            isbn INTEGER,
            nummer INTEGER unique NOT NULL
            )""")
con.commit()


cur.executemany("INSERT INTO bøker(nummer) VALUES(?)", [(nummer,) for nummer in range(1,52)])

booklist = []
with open("C:\\Users\\tobia\\Desktop\\eksamen\\bibliotek\\bøker.csv", "r", encoding="utf-8") as file:
    bøker = [book for book in file.read().split("\n")]
    for book in bøker:
        d_book = book.split(",")
        if len(d_book) >=4:
            booklist.append(
                { "tittel": d_book[0],
                "forfatter": d_book[1],
                "isbn": d_book[2],
                "nummer": d_book[3]
                }
            )

cur.executemany("UPDATE bøker SET tittel = ?, forfatter = ?, isbn = ? WHERE nummer = ?",
                [(book["tittel"], book["forfatter"], book["isbn"], book["nummer"]) for book in booklist],)
con.commit()