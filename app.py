from flask import Flask, request, render_template, flash, redirect, url_for
from DB.db import category, medicalInstructions, examService, user
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
            'cost': cost,
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
                                                            'cost': new_exam['cost'],
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
    
    return render_template('./Catalog/catalog.html.jinja', examList=examList)



#=========================================================

if __name__=='__main__':
    app.run(debug=True)