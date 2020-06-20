from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/shop'
db = SQLAlchemy(app)

class orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String(80))
    created_on = db.Column(db.String(120))
    email = db.Column(db.String(80))
    order_date = db.Column(db.String(20))

class customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    address = db.Column(db.String(80))
    phone = db.Column(db.Integer)
    age = db.Column(db.Integer)

class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    updated_on = db.Column(db.Integer)
    updated_by = db.Column(db.String(80))
    created_on = db.Column(db.Integer)
    created_by = db.Column(db.String(50))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    image = db.Column(db.String(50))
    description = db.Column(db.String(120))

class sellproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sell_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    temporary_id = db.Column(db.Integer)

class salestable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sales_date = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    total_charges = db.Column(db.Integer)

class supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    supplier_no = db.Column(db.Integer)
    email = db.Column(db.String(120))
    address = db.Column(db.String(80))
    phone = db.Column(db.Integer)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route("/")
def  welcome():
    return render_template("welcome.html")

@app.route("/home")
def home():
    products = product.query.filter_by().all()
    user = users.query.filter_by().all()
    return render_template("home.html", products=products, user=user)


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/customerlogin", methods=["GET", "POST"])
def clogin():
        if request.method == "POST":
            uname = request.form["uname"]
            passw = request.form["passw"]
            login = users.query.filter_by(username=uname, password=passw).first()
            if login is not None:
                return redirect(url_for("home" , un=uname))
        return render_template("customer_login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = users(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("customer_login"))
    return render_template("register.html")

@app.route('/viewproduct/<string:id>', methods=["GET"])
def view_product(id):
    view = product.query.filter_by(id=id).first()
    return render_template("viewproduct.html", view=view)


app.run(debug=True)