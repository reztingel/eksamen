from flask import Flask,request
from flask_cors import CORS
import sqlite3



app = Flask(__name__)
CORS(app)


con = sqlite3.Connection("./database.db", check_same_thread=False)
cur = con.cursor()






@app.route('/', methods=['GET'])
def index():
    try:
        cur.execute("SELECT * from bøker")
        bøker = cur.fetchall
        response = []
        for book in bøker:
            if book[0] is not None:
                response.append(
                    {"tittel":book[0],
                     "forfatter":book[1],
                     "isbn":book[2],
                     "nummer":book[3]
                     }
                )
        return response, 200
    except sqlite3.Error as e:
        return {"error": str(e)}, 500





@app.route('/book/<nummer>', methods=['GET'])
def get_book(nummer):
    try:
        cur.execute("SELECT * FROM bøker WHERe nummer = ?", (nummer,))
        book = cur.fetchone()
        if book[0] is None:
            return {"error": "fant ikke boken"}, 404
        response = {
            "tittel": book[0],
            "forfatter": book[1],
            "isbn": book[2],
            "nummer": nummer
        }
        return response, 200
    except sqlite3.Error as e:
        return {"error": str(e)}, 500


@app.route("/filter/<streng>", methods=["GET"])
def filter(streng):
    try:

        cur.execute("SELECT * FROM bøker WHERE tittel LIKE ? OR forfatter LIKE ?",(f"%{streng}%", f"%{streng}%"),)
        bøker = cur.fetchall()
        if not bøker:
            return {"melding": f"Fant ingen bøker etter søkerordet: {streng}"}, 404
        response = []
        for book in bøker:
            response.append(
                {"tittel": book[0],
                "forfatter": book[1],
                "isbn": book[2],
                "nummer": book[3]
                }
            )
        return response,200
    except sqlite3.Error as e:
        return {"error": str(e)},500

@app.route('/slettbook/<int:nummer>', methods=['DELETE'])
def slettbook(nummer):
    try:
        cur.execute("SELECT * FROM bøker WHERE nummer = ?", (nummer))
        row = cur.fetchone()
        if row[0] is None:
            return {"melding": "boke finnes ikke i databasen"}, 404
        cur.execute("UPDATE bøker SET tittel = NULL, forfatter = NULL, isbn = NULL WHERE nummer = ?",
                    (nummer,)
        )
        con.commit()
        return{"melding": "boken ble slettet fra databasen"}, 200
    except sqlite3.Error as e:
        return{"error": str(e)},500
    


@app.route('/leggtilbok', methods=['POST'])
def legg_til_bok():
    try:
        tittel = request.get_json()["tittel"]
        forfatter = request.get_json()["forfatter"]
        isbn = request.get_json()["isbn"]
        nummer = request.get_json()["nummer"]
        cur.execute("SELECT * FROM bøker WHERE tittel IS NULL")
        space = cur.fetchone()
        if space is None:
            return{"melding": "det er ikke plass til flere bøker"}, 409
        cur.execute("SELECT * FROM bøker WHERE nummer = ?", (nummer,))
        book = cur.fetchone
        if book[0] is not None:
            return{"melding": "boken finnes fra før"},409
        cur.execute("UPDATE bøker SET tittel = ?, forfatter = ?, isbn = ? WHERE nummer = ?",
                    (tittel, forfatter, isbn, nummer)
        )
        con.commit()
        return{"melding": f"{tittel}ble registrert"},200
    except sqlite3.Error as e:
        return{"error": str(e)},500


if __name__ == '__main__':
    app.run(debug=True, port=5001)