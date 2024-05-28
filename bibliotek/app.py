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
    book = Bok.query.filter_by(nummer=nummer).first()
    if book:
        return jsonify(book.to_dict())
    else:
        return jsonify({'error': 'Book not found'}), 404



@app.route('/filter/<string:streng>', methods=['GET'])
def filter_boker(streng):
    boker = Bok.query.filter((Bok.tittel.contains(streng)) | (Bok.forfatter.contains(streng))).all()
    return jsonify([bok.to_dict() for bok in boker])


@app.route('/slettbok/<int:nummer>', methods=['DELETE'])
def delete_bok(nummer):
    bok = Bok.query.filter_by(nummer=nummer).first()
    if bok:
        db.session.delete(bok)
        db.session.commit()
        return jsonify({'resultat': 'Boken ble slettet fra databasen'})
    else:
        return jsonify({'resultat': 'Boken finnes ikke i databasen'}), 404


@app.route('/leggtilbok', methods=['POST'])
def legg_til_bok():
    data = request.json
    eksisterende_bok = Bok.query.filter_by(nummer=data['nummer']).first()
    if eksisterende_bok:
        return jsonify({'resultat': 'Boken finnes fra før'}), 400
    ny_bok = Bok(
        tittel=data['tittel'],
        forfatter=data['forfatter'],
        isbn=data['isbn'],
        nummer=data['nummer']
    )
    db.session.add(ny_bok)
    db.session.commit()
    return jsonify({'resultat': f"{data['tittel']} ble registrert"})


if __name__ == '__main__':
    app.run(debug=True, port=5001)