from flask import Flask, request, render_template, flash, redirect, url_for
from DB.db import category, medicalInstructions, testService, user
from bson.objectid import ObjectId

app = Flask(__name__, template_folder="./templates")
app.config['SECRET_KEY'] = "twiceot9"
userLoged = {}


#=========================================================
#  Default
#=========================================================
@app.route("/", methods=["GET"])
def default():
    return redirect(url_for('login'))

@app.route("/home", methods=["GET"])
def home():
    return render_template('home.html.jinja', userLoged=userLoged)

#=========================================================
#  LOGIN
#=========================================================
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
                userLoged = userFound
                return render_template('home.html.jinja', userLoged = userLoged)

    return render_template('login.html.jinja')

#=========================================================
#  CATEGORY
#=========================================================

@app.route("/category", methods=["GET", "POST"])
def saveCategory():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']

        newCategory = {
            'name': name,
            'description': description
        }

        category.insert_one(newCategory)
        return redirect(url_for('saveCategory'))

    return render_template('./category/category.html.jinja')

@app.route("/categoriesList", methods=["GET"])
def categoriesListView():
    categoriesList = category.find()
    return render_template('./category/categoriesList.html.jinja', categoriesList = categoriesList)

@app.route("/delCategory/<id>", methods=["GET"])
def delCategory(id):
    oid = ObjectId(id)
    catFound = category.find_one_and_delete({'_id' : oid})
    return redirect(url_for('categoriesListView'))

@app.route("/updateCategory/<id>", methods=["GET", "POST"])
def modifyCategory(id):
    oid = ObjectId(id)
    catFound = category.find_one({'_id': oid})
    if request.method == "POST":
        new_category = request.form
        categoryX = category.replace_one({'_id': oid},
                                        {
                                            'name': new_category['name'],
                                            'description': new_category['description']
                                        })
        return redirect(url_for('categoriesListView'))
    return render_template("./category/updateCategory.html.jinja", category=catFound)


#=========================================================


if __name__=='__main__':
    app.run(debug=True)