from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite.///'
db = SQLAlchemy(app)


class Bok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tittel = db.Column(db.String(120), nullable=False)
    forfatter = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(13), nullable=False)
    nummer = db.Column(db.Integer, unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'tittel': self.tittel,
            'forfatter': self.forfatter,
            'isbn': self.isbn,
            'nummer': self.nummer
        }
    
db.create_all()



@app.route('/boker', methods=['GET'])
def get_boker():
    boker = Bok.query.all()
    return jsonify([bok.to_dict() for bok in boker])

@app.route('/bok/<int:nummer>', methods=['GET'])
def get_bok(nummer):
    bok = Bok.query.filter_by(nummer=nummer).first()
    if bok:
        return jsonify(bok.to_dict())
    else:
        return jsonify({'resultat': 'Boken finnes ikke i databasen'}), 404

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
    app.run(debug=True, host='0.0.0.0')