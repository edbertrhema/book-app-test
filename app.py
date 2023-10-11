from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', books=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        keywords = request.form['keywords']
        price = request.form['price']
        stock = request.form['stock']
        publisher = request.form['publisher']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, description, category, keywords, price, stock, publisher) VALUES (%s, %s, %s, %s, %s, %s, %s)", (title, description, category, keywords, price, stock, publisher))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']

        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        keywords = request.form['keywords']
        price = request.form['price']
        stock = request.form['stock']
        publisher = request.form['publisher']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE books SET title=%s, description=%s, category=%s, keywords=%s, price=%s, stock=%s, publisher=%s
        WHERE id=%s
        """, (title, description, category, keywords, price, stock, publisher, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)