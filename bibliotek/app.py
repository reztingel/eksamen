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