from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import Bok  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

def import_books_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        next(file)
        
        for line in file:
            data = line.strip().split(',')
            tittel, forfatter, isbn, nummer = data

    
            book = Bok(
                tittel=tittel,
                forfatter=forfatter,
                isbn=isbn,
                nummer=nummer
            )

    
            with app.app_context():
                db.create_all()

                
                db.session.add(book)
                db.session.commit()

if __name__ == '__main__':
    csv_file_path = 'C:/Users/Ton/OneDrive - Innlandet fylkeskommune/Skrivebord/eksamen/bibliotek/bøker.csv'
    import_books_from_csv(csv_file_path)


