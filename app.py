from flask import Flask, render_template, url_for, g, request
import sqlite3
from datetime import datetime


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
@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()

    if request.method == 'POST':
        date = request.form['date']
        dt = datetime.strptime(date, '%Y-%m-%d')
        database_date = datetime.strftime(dt, '%Y%m%d')

        db.execute('insert into log_date(entry_date) values(?)', [database_date])
        db.commit()

    cur = db.execute('select * from log_date order by entry_date desc')
    results = cur.fetchall()
    pretty_results = []
    for el in results:
        single_date = {}
        d = datetime.strptime(str(el['entry_date']), '%Y%m%d')
        single_date['entry_date'] = datetime.strftime(d, '%B %d, %Y')
        pretty_results.append(single_date)

    return render_template('home.html', results=pretty_results)


@app.route('/view/<date>', methods=['GET', 'POST'])
def view(date):
    if request.method == 'POST':
        return '<h1>The food item {} added!</h1>'.format(request.form['food-select'])
    db = get_db()
    cur = db.execute('select entry_date from log_date where entry_date = ?', [date])
    result = cur.fetchone()
    d = datetime.strptime(str(result['entry_date']), '%Y%m%d')
    pretty_date = datetime.strftime(d, '%B %d, %Y')

    food_cur = db.execute('select id, name from food')
    food_results = food_cur.fetchall()

    return render_template('day.html', date=pretty_date, food_results=food_results)


@app.route('/food', methods=['GET', 'POST'])
def food():
    db = get_db()


    if request.method == 'POST':
        name = request.form['food-name']
        protein = int(request.form['proteins'])
        carbohydrates = int(request.form['carbons'])
        fat = int(request.form['fats'])
        calories = protein * 4 + carbohydrates * 4 + fat * 9

        db.execute('insert into food (name, protein, carbohydrates, fat, calories) values(?, ?, ?, ?, ?)',\
            [name, protein, carbohydrates, fat, calories] )
        db.commit()

        return '<h1>Name: {}, Protein: {}, Carb: {}, Fat: {}</h1>'.format(name, protein, carbohydrates, fat)

    cur = db.execute('select * from food')
    results = cur.fetchall()
    return render_template('add_food.html', results=results)





if __name__ == "__main__":
    app.run(debug=True)