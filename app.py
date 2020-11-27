from flask import Flask, render_template, url_for, g
import sqlite3

app = Flask(__name__)



###### db utils ########
def connect_db():
    sql = sqlite3.connect('my.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'my.db'):
        g.sqlite3_db.close()


###### basic routes #########
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/view')
def view():
    return render_template('day.html')


@app.route('/food')
def food():
    return render_template('add_food.html')





if __name__ == "__main__":
    app.run(debug=True)