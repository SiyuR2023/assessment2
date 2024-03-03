import csv
import sqlite3
from pathlib import Path

# Specify CSV file path
csv_file_path = 'bookData/Books.csv'

# Print the current working directory
print("Current working directory:", Path.cwd())

# Check if the CSV file exists
if not Path(csv_file_path).is_file():
    print(f"file {csv_file_path} not found. Please check if the file path is correct.")
else:
    print(f"file {csv_file_path} remain. ")

    # Open a database connection
    conn = sqlite3.connect('book_information_data.db')
    cur = conn.cursor()

    # Delete existing tables to avoid duplicate data additions
    conn.execute('DROP TABLE IF EXISTS books')
    print("Form deleted successfully")

    # Creating a New Table
    conn.execute('''
    CREATE TABLE books (
        "Book-Title" TEXT,
        "Book-Author" TEXT,
        "Year-Of-Publication" INTEGER,
        Publisher TEXT
    )
    ''')
    print("Books form created successfully")

    # Trying to open and read a CSV file
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Preparing multiple rows of data for batch insertion using list derivatives
            to_db = [(row['Book-Title'], row['Book-Author'], row['Year-Of-Publication'], row['Publisher']) for row in reader]
            # Performs a multi-row insertion, using parameters that match the column names in the CSV file and the newly created table
            cur.executemany("INSERT INTO books (\"Book-Title\", \"Book-Author\", \"Year-Of-Publication\", Publisher) VALUES (?, ?, ?, ?);", to_db)
        conn.commit()

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
    finally:
        conn.close()

# Book details display code for Flask apps
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('main.html')

@app.route('/details')
def details():
    query = request.args.get('query', '')
    conn = sqlite3.connect('book_information_data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if query:
        cur.execute('''
            SELECT * FROM books
            WHERE "Book-Title" LIKE ? OR "Book-Author" LIKE ? OR Publisher LIKE ? OR "Year-Of-Publication" LIKE ?
            ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cur.execute('SELECT * FROM books LIMIT 50')
    filtered_books = cur.fetchall()
    conn.close()
    #  Make sure the books variable in render_template is passed to the template
    return render_template('book_details.html', books=filtered_books)

if __name__ == '__main__':
    app.run(debug=True)


def search_books(search_query):
    conn = sqlite3.connect('book_information_data.db')
    cur = conn.cursor()

    # 使用LIKE运算符构建模糊匹配查询
    query = f"""
    SELECT * FROM books
    WHERE 
    Book_Title LIKE '%{search_query}%' OR 
    Book_Author LIKE '%{search_query}%' OR 
    Publisher LIKE '%{search_query}%' OR 
    Year_Of_Publication LIKE '%{search_query}%'
    """
    cur.execute(query)
    results = cur.fetchall()

    # 如果有搜索结果，则打印出来
    if results:
        for result in results:
            print(f"书名: {result[0]}, 作者: {result[1]}, 出版年份: {result[2]}, 出版社: {result[3]}")
    else:
        print("没有找到匹配的结果。")
    
    conn.close()
