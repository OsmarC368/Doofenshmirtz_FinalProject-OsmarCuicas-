from flask import Flask, request, render_template, flash, redirect, url_for
from DB.db import category, medicalInstructions, testService, user
from bson.objectid import ObjectId

app = Flask(__name__, template_folder="./templates")
app.config['SECRET_KEY'] = "twiceot9"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        newUser = {
            'email' : email,
            'password' : password,
            'username' : username
        }

        user.insert_one(newUser)
        return redirect(url_for('login'))

    return render_template('register.html.jinja')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        userFound = user.find_one({'username': username})
        if not userFound:
            return render_template('login.html.jinja')
        else:
            if userFound['password'] == password:
                return render_template('home.html.jinja')

    return render_template('login.html.jinja')

@app.route("/category", methods=["GET", "POST"])
def category():
    if request.method == "POST":
        p = 0

    return render_template('./category/category.html.jinja')


if __name__=='__main__':
    app.run(debug=True)