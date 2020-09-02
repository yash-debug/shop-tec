#this is the python flask E-commerce website

from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
import os

params = {"admin_user":'spd' , "admin_pass":'white'}
app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/shop'
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
    updated_on = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    image = db.Column(db.String(50), nullable=True)
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

@app.route("/dashboard", methods=["GET", "POST"])
def  dashboard():
    if('user' in session and session['user'] == params['admin_user']):
        products = product.query.filter_by().all()
        return render_template("dashboard.html", products=products)


    if request.method=="POST":
        username = request.form.get("aname")
        userpass = request.form.get("apass")
        if (username == params['admin_user'] and userpass == params['admin_pass']):
            session['user'] = username
            products = product.query.filter_by().all()
            return render_template("dashboard.html", products=products)
            
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')
 
@app.route("/home", methods=["POST", "GET"])
def home():
    person = users.query.filter_by().all()
    if('user' in session):
        products = product.query.filter_by().all()
        return render_template("home.html", products=products)          

    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        session['user'] = uname
        products = product.query.filter_by().all()
        return render_template("home.html", products=products)
    
    return render_template("customer_login.html")    

@app.route('/clogout')
def clogout():
    session.pop('user')
    return redirect('/')


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/customerlogin", methods=["GET", "POST"])
def clogin():
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

        return render_template("customer_login.html")
    return render_template("register.html")

@app.route('/viewproduct/<string:id>', methods=["GET"])
def view_product(id):
    view = product.query.filter_by(id=id).first()
    return render_template("viewproduct.html", view=view)

@app.route('/delete/<string:id>', methods=["GET","POST"])
def delete(id):
    if('user' in session and session['user'] == params['admin_user']):
        item = product.query.filter_by(id=id).first()
        db.session.delete(item)
        db.session.commit()
    return redirect('/dashboard')

@app.route('/edit/<string:id>', methods=["GET","POST"])
def edit(id):
    if('user' in session and session['user'] == params['admin_user']):

        if request.method == "POST":
            prod_name = request.form.get('name')
            prod_price = request.form.get('price')
            prod_quantity = request.form.get('quantity')
            prod_description = request.form.get('description')

            if id=="0":
                newitem = product(name=prod_name, price=prod_price, quantity=prod_quantity, description=prod_description)
                db.session.add(newitem)
                db.session.commit()
                return redirect('/dashboard')
            else:
                item = product.query.filter_by(id=id).first()
                item.name = prod_name
                item.price = prod_price
                item.quantity = prod_quantity
                item.description = prod_description
                db.session.commit()
                return redirect('/dashboard')
        items = product.query.filter_by(id=id).first()
        return render_template('edit.html', id=id, item=items)             
             


app.run(debug=True)