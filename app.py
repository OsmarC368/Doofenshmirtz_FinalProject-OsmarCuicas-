from flask import Flask, request, render_template, flash, redirect, url_for
from DB.db import category, medicalInstructions, examService, user, User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from bson.objectid import ObjectId

app = Flask(__name__, template_folder="./templates")
app.config['SECRET_KEY'] = "twiceot9"
userLoged = {}
login_manager = LoginManager()
login_manager.init_app(app)


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

@login_manager.user_loader
def load_user(user_id):
    userX = user.find_one({'_id': ObjectId(user_id)})
    if userX:
        user_obj = User()
        user_obj.id = str(user['_id'])
        return user_obj
    return None

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
        userFound = user.find_one({'username': username, 'password': password})
        if not userFound:
            flash('Please check your login details and try again.')
            return render_template('login.html.jinja')
        else:
            user_obj = User()
            user_obj.id = str(user['_id'])
            login_user(user_obj)
            return render_template('home.html.jinja', userLoged = userLoged)
    return render_template('login.html.jinja')

@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#=========================================================
#  CATEGORY
#=========================================================

@app.route("/category", methods=["GET", "POST"])
@login_required
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
#  MEDICAL INSTRUCTIONS
#=========================================================
@app.route("/instruction", methods=["GET", "POST"])
def saveInstruction():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']

        newInstruction = {
            'name': name,
            'description': description
        }

        medicalInstructions.insert_one(newInstruction)
        return redirect(url_for('saveInstruction'))

    return render_template('./medicalInstruction/medicalInstruction.html.jinja')

@app.route("/instructionList", methods=["GET"])
def isntructionsListView():
    intructionList = medicalInstructions.find()
    return render_template('./medicalInstruction/instructionList.html.jinja', instructionList = intructionList)

@app.route("/delInstruction/<id>", methods=["GET"])
def delInstruction(id):
    oid = ObjectId(id)
    intructionFound = medicalInstructions.find_one_and_delete({'_id' : oid})
    return redirect(url_for('isntructionsListView'))

@app.route("/updateInstruction/<id>", methods=["GET", "POST"])
def modifyInstruction(id):
    oid = ObjectId(id)
    intructionFound = medicalInstructions.find_one({'_id': oid})
    if request.method == "POST":
        new_instruction = request.form
        instructionX = medicalInstructions.replace_one({'_id': oid},
                                                        {
                                                            'name': new_instruction['name'],
                                                            'description': new_instruction['description']
                                                        })
        return redirect(url_for('isntructionsListView'))
    return render_template("./medicalInstruction/updateInstruction.html.jinja", instruction=intructionFound)

#=========================================================

#=========================================================
#  Exams / Service
#=========================================================
@app.route("/ExamsServices", methods=["GET", "POST"])
def saveExam():

    categories = category.find()
    instructionList = medicalInstructions.find()

    if request.method == "POST":
        code = request.form['examCode']
        name = request.form['name']
        categoryX = request.form['category']
        sampleType = request.form['sampleType']
        cost = request.form['cost']
        medicalInstructionsX = request.form['instruction']

        newExam = {
            'code': code,
            'name': name,
            'categoryCode': categoryX,
            'sampleType': sampleType,
            'cost': float(cost),
            'medicalInstructionCode': medicalInstructionsX,
            'category': category.find_one({'_id': ObjectId(categoryX)})['name'],
            'medicalInstruction': medicalInstructions.find_one({'_id': ObjectId(medicalInstructionsX)})['name']
        }

        examService.insert_one(newExam)
        return redirect(url_for('saveExam'))

    return render_template('./examService/examService.html.jinja', categories = categories, instructionsList = instructionList)

@app.route("/ExamsServices/List", methods=["GET"])
def examListView():
    examList = examService.find()
    instructions = medicalInstructions.find()
    categories = category.find()
    return render_template('./examService/examServiceList.html.jinja', examList = examList, instructions = instructions, categories = categories)

@app.route("/ExamsServices/DelExamService/<id>", methods=["GET"])
def delExamService(id):
    oid = ObjectId(id)
    examFound = examService.find_one_and_delete({'_id' : oid})
    return redirect(url_for('examListView'))

@app.route("/ExamsServices/Update/<id>", methods=["GET", "POST"])
def modifyExam(id):
    oid = ObjectId(id)
    categories = category.find()
    instructionList = medicalInstructions.find()
    examFound = examService.find_one({'_id': oid})
    if request.method == "POST":
        new_exam = request.form
        examX = examService.replace_one({'_id': oid},
                                                        {
                                                            'code': new_exam['examCode'],
                                                            'name': new_exam['name'],
                                                            'categoryCode': new_exam['category'],
                                                            'sampleType': new_exam['sampleType'],
                                                            'cost': float(new_exam['cost']),
                                                            'medicalInstructionCode': new_exam['instruction'],
                                                            'category': category.find_one({'_id': ObjectId(new_exam['category'])})['name'],
                                                            'medicalInstruction': medicalInstructions.find_one({'_id': ObjectId(new_exam['instruction'])})['name']
                                                        })
        return redirect(url_for('examListView'))
    return render_template("./examService/updateExam.html.jinja", exam=examFound, categories = categories, instructionsList = instructionList)

@app.route("/ExamsServices/Details/<id>", methods=["GET"])
def examDetails(id):
    oid = ObjectId(id)
    examFound = examService.find_one({'_id' : oid})
    return render_template("./examService/examDetails.html.jinja", exam=examFound)

#=========================================================
#  CATALOG
#=========================================================
@app.route("/Catalog", methods=["GET", "POST"])
def catalog():
    examList = examService.find()
    instructionList = medicalInstructions.find()
    if request.method == "POST":
        if request.form["instructions"] != "0":
            examList = examService.find({'medicalInstruction': request.form["instructions"]})
        if request.form['sampleType'] != "":
            examList = [exam for exam in examList if exam['sampleType'] == request.form["sampleType"]]
        return render_template('./Catalog/catalog.html.jinja', examList=examList, instructionList=instructionList)
            

    return render_template('./Catalog/catalog.html.jinja', examList=examList, instructionList=instructionList)



#=========================================================
#  REPORT
#=========================================================
@app.route("/Report", methods=["GET"])
def report():

    catNewList = []
    top = 0
    instruction = {}

    interval = {
        'int1': 0,
        'int2': 0,
        'int3': 0,
        'int4': 0,
        'int5': 0
    }

    for exam in examService.find():
        if exam['cost'] <= 100:
            interval['int1'] += 1
        elif exam['cost'] <= 200:
            interval['int2'] += 1
        elif exam['cost'] <= 300:
            interval['int3'] += 1
        elif exam['cost'] <= 500:
            interval['int4'] += 1
        elif exam['cost'] > 500:
            interval['int5'] += 1

    for inst in medicalInstructions.find():
        i = 0
        for exam in examService.find():
            if exam['medicalInstruction'] == inst['name']:
                i += 1
        if i > top:
            top = i
            instruction = {'name': inst['name'], 'description': inst['description']}
        

    for cat in category.find():
        i = 0
        for exam in examService.find():
            if exam['category'] == cat['name']:
                i += 1
        catNewList.append({'name': cat['name'], 'num': str(i)})

    return render_template('./Catalog/report.html.jinja', interval=interval , categoryList=catNewList, medicalInstruction=instruction)



#=========================================================

if __name__=='__main__':
    app.run(debug=True)