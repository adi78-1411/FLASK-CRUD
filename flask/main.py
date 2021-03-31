import urllib

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "Secret Key"

params = urllib.parse.quote_plus(
    'DRIVER={SQL Server};SERVER=DESKTOP-DFUHK8I;DATABASE=FlaskCRUD;Trusted_Connection=yes;')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.String(100))
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    dateOfBirth = db.Column(db.String(100))
    dueAmount = db.Column(db.Integer)

    def __init__(self, studentId, firstName, lastName, dateOfBirth, dueAmount):
        self.studentId = studentId
        self.firstName = firstName
        self.lastName = lastName
        self.dateOfBirth = dateOfBirth
        self.dueAmount = dueAmount


@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", students=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        studentId = request.form['studentId']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        dateOfBirth = request.form['dateOfBirth']
        dueAmount = request.form['dueAmount']

        new_data = Data(studentId, firstName, lastName, dateOfBirth, dueAmount)
        db.session.add(new_data)
        db.session.commit()
        flash("Student Details are Added Successfully")
        return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        new_data = Data.query.get(request.form.get('id'))
        new_data.studentId = request.form['studentId']
        new_data.firstName = request.form['firstName']
        new_data.lastName = request.form['lastName']
        new_data.dateOfBirth = request.form['dateOfBirth']
        new_data.dueAmount = request.form['dueAmount']

        db.session.commit()
        flash("Student Data are Updated")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    new_data = Data.query.get(id)
    db.session.delete(new_data)
    db.session.commit()
    flash("Student Data Deleted..!")
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
