from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.sqlite'
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = "static\images"


db = SQLAlchemy(app)
app.app_context().push()


class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    number = db.Column(db.Text)
    image = db.Column(db.Text)

    def __init__(self, name, number, image):
        self.name = name
        self.number = number
        self.image = image


db.create_all()


# Create your views here


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/add")
def add():
    return render_template('add.html')


@app.route("/addthankyou", methods=['GET', 'POST'])
def addthankyou():
    if request.method == 'POST':

        if Contact.query.filter(Contact.number == request.form['number']).first():
            flash('Number already exists', 'error')
            return render_template('add.html')

        if not request.form['number'].isdigit() or not len(request.form['number']) == 10:
            flash('Phone number must have only 10 digits', 'error')
            return render_template('add.html')

        else:
            name = request.form['name']
            number = request.form['number']
            image = request.files['image']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(filepath)
            a = Contact(name, number, image.filename)
            db.session.add(a)
            db.session.commit()
            return render_template('addthankyou.html', name=name, number=number, image=image.filename)

    return render_template('add.html')


@app.route("/delete")
def delete():
    return render_template('delete.html')


@app.route("/deletebyid")
def deletebyid():
    return render_template('deletebyid.html')


@app.route("/deletebyname")
def deletebyname():
    return render_template('deletebyname.html')


@app.route("/delthankyou", methods=['GET', 'POST'])
def delthankyou():
    if request.method == 'POST':

        if Contact.query.filter(Contact.id == request.form['id']):
            id = request.form['id']
            a = Contact.query.filter_by(id=id).first()
            db.session.delete(a)
            db.session.commit()
            return render_template('delthankyou.html', id=id, name=a.name, number=a.number, image=a.image)

        else:
            flash('No such ID', 'error')
            return render_template('deletebyid.html')

    return render_template('deletebyid.html')


@app.route("/delthankyou1", methods=['GET', 'POST'])
def delthankyou1():
    if request.method == 'POST':

        if Contact.query.filter(Contact.name == request.form['name']):
            name = request.form['name']
            a = Contact.query.filter_by(name=name).first()
            db.session.delete(a)
            db.session.commit()
            return render_template('delthankyou1.html', name=name, number=a.number, image=a.image)

        else:
            flash('No such name', 'error')
            return render_template('deletebyname.html')

    return render_template('deletebyname.html')


@app.route("/update")
def update():
    return render_template('update.html')


@app.route("/updatebyname")
def updatebyname():
    return render_template('updatebyname.html')


@app.route("/updatebynumber")
def updatebynumber():
    return render_template('updatebynumber.html')


@app.route("/updatethankyou", methods=['GET', 'POST'])
def updatethankyou():
    if request.method == 'POST':

        if not request.form['nn'].isdigit() or not len(request.form['nn']) == 10:
            flash('Phone number must have only 10 digits', 'error')
            return render_template('updatebynumber.html')

        if Contact.query.filter(Contact.number == request.form['nn']).first():
            flash('Number already exists', 'error')
            return render_template('updatebynumber.html')

        if Contact.query.filter(Contact.number == request.form['on']):
            on = request.form['on']
            nn = request.form['nn']
            a = Contact.query.filter_by(number=on).first()
            b = a.number
            a.number = nn
            db.session.commit()
            return render_template('updatethankyou.html', name=a.name, on=b, nn=nn, image=a.image)

        else:
            flash('No such number', 'error')
            return render_template('updatebynumber.html')

    return render_template('updatebynumber.html')


@app.route("/updatethankyou1", methods=['GET', 'POST'])
def updatethankyou1():
    if request.method == 'POST':

        if not request.form['nn'].isdigit() or not len(request.form['nn']) == 10:
            flash('Phone number must have only 10 digits', 'error')
            return render_template('updatebyname.html')

        if Contact.query.filter(Contact.number == request.form['nn']).first():
            flash('Number already exists', 'error')
            return render_template('updatebyname.html')

        if Contact.query.filter(Contact.name == request.form['name']):
            name = request.form['name']
            nn = request.form['nn']
            a = Contact.query.filter_by(name=name).first()
            b = a.number
            a.number = nn
            db.session.commit()
            return render_template('updatethankyou1.html', name=name, on=b, nn=nn, image=a.image)

        else:
            flash('No such Name', 'error')
            return render_template('updatebyname.html')

    return render_template('updatebyname.html')


@app.route("/search")
def search():
    return render_template('search.html')


@app.route("/searchbyname")
def searchbyname():
    return render_template('searchbyname.html')


@app.route("/searchbynumber")
def searchbynumber():
    return render_template('searchbynumber.html')


@app.route("/searchthankyou", methods=['GET', 'POST'])
def searchthankyou():
    if request.method == 'POST':

        if Contact.query.filter(Contact.name == request.form['name']):
            name = request.form['name']
            a = Contact.query.filter_by(name=name).all()
            db.session.commit()
            return render_template('searchthankyou.html', all=a)

        else:
            flash('No such contact', 'error')
            return render_template('searchbyname.html')

    return render_template('searchbyname.html')


@app.route("/searchthankyou1", methods=['GET', 'POST'])
def searchthankyou1():
    if request.method == 'POST':

        if Contact.query.filter(Contact.number == request.form['number']):
            number = request.form['number']
            a = Contact.query.filter_by(number=number)
            db.session.commit()
            return render_template('searchthankyou.html', all=a)

        else:
            flash('No such contact', 'error')
            return render_template('searchbynumber.html')

    return render_template('searchbynumber.html')


@app.route("/sort")
def sort():
    all = Contact.query.order_by(Contact.name).all()
    return render_template('sort.html', all=all)


@app.route("/table")
def table():
    all = Contact.query.all()
    return render_template('table.html', all=all)


app.run(debug=True)
