from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

db_name = 'book_information_data.db'

@app.route('/')
def menu():
    return render_template('main.html')

@app.route('/details')
def details():
    query = request.args.get('query', '')  # Get the value of the query from the request parameters
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Setting up a row factory to access column information
    cur = conn.cursor()
    if query:
       
        cur.execute('''
            SELECT * FROM books
            WHERE "Book-Title" LIKE ? OR "Book-Author" LIKE ? OR "Publisher" LIKE ? OR "Year-Of-Publication" LIKE ?
            ''', ('%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'))
    else:
        cur.execute('SELECT * FROM books LIMIT 3000')
    filtered_books = cur.fetchall()
    conn.close()
    return render_template('book_datails.html', books=filtered_books)

if __name__ == '__main__':
    app.run(debug=True)


