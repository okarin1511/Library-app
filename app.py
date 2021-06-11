from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)


class Publisher(db.Model):
    pub_id = db.Column(db.Integer, primary_key=True)
    pub_name = db.Column(db.String(20))
    address = db.Column(db.String(20))

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(60))
    author = db.Column(db.String(20))
    # available
    pub_id = db.Column(db.Integer, db.ForeignKey(Publisher.pub_id))

    def __repr__(self):
        return '<Books %r>' % self.book_id

class Member(db.Model):
    mem_id = db.Column(db.Integer, primary_key=True)
    mem_name = db.Column(db.String(20))
    # join_date = db.Column(db.DateTime, default = datetime.utcnow)


Borrowed = db.Table('borrowed',
    db.Column('book_id', db.Integer, db.ForeignKey(Book.book_id)),
    db.Column('issue_date', db.DateTime, default = datetime.utcnow)
    # due_date 
)
    
@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/collection', methods = ['POST', 'GET'])
def collection():
    books = Book.query.order_by(Book.book_id).all()  
    return render_template('collection.html', books = books)

@app.route('/addbook', methods = ['POST', 'GET'])
def addbook():
    if request.method == 'POST':
        b_name = request.form['book_name']
        a_name = request.form['author']
        new_book = Book(book_name = b_name, author = a_name)
        

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding your book'
    else:
        books = Book.query.order_by(Book.book_id).all()
        return render_template('addbook.html', books = books)

@app.route('/returnbook', methods = ['POST', 'GET'])
def returnbook():
    if request.method == 'POST':
        b_name = request.form['book_name']
        a_name = request.form['author']
        new_book = Book(book_name = b_name, author = a_name)
        

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding your book'
    else:
        books = Book.query.order_by(Book.book_id).all()
        return render_template('returnbook.html', books = books)


@app.route('/member', methods = ['POST', 'GET'])
def member():
    if request.method == 'POST':
        m_name = request.form[Member.mem_name]
        new_mem = Member(mem_name = m_name)

        try:
            db.session.add(new_mem)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding the member'

    else:
        return render_template('member.html')

@app.route('/borrow', methods = ['POST', 'GET'])
def borrow():
    books = Book.query.order_by(Book.book_id).all()  
    return render_template('borrow.html', books = books)

@app.route('/delete/<int:book_id>')
def delete(book_id):
    book_to_delete = Book.query.get_or_404(book_id) 

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/borrow')
    except:
        return 'There was a problem borrowing that book'


if __name__ == "__main__":
    app.run(debug=True)