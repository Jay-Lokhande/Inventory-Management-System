from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from models import Customer  # Import the Customer model from your models module
from customer_forms import CustomerForm  # Import the CustomerForm class
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize Flask-Bcrypt

# Define your database models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    hired_date = db.Column(db.Date)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_title = db.Column(db.String(255))
    salary = db.Column(db.Numeric(10, 2))

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    province = db.Column(db.String(255))
    city = db.Column(db.String(255))
    street = db.Column(db.String(255))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    qty_stock = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    password = db.Column(db.String(60), nullable=False)  # Store hashed passwords
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    phone_number = db.Column(db.String(20))

class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255))

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(255))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    phone_number = db.Column(db.String(20))

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))

# Commit the models to the database
# db.create_all()
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customers')
def list_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

# @app.route('/customers/add', methods=['GET', 'POST'])
# def add_customer():
#     if request.method == 'POST':
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         phone_number = request.form['phone_number']
#
#         customer = Customer(first_name=first_name, last_name=last_name, phone_number=phone_number)
#         db.session.add(customer)
#         db.session.commit()
#         return redirect(url_for('list_customers'))
#
#     return render_template('add_customer.html')
@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    form = CustomerForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data

        customer = Customer(first_name=first_name, last_name=last_name, phone_number=phone_number)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('list_customers'))

    return render_template('add_customer.html', form=form)
# @app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
# def edit_customer(id):
#     customer = Customer.query.get(id)
#
#     if request.method == 'POST':
#         customer.first_name = request.form['first_name']
#         customer.last_name = request.form['last_name']
#         customer.phone_number = request.form['phone_number']
#
#         db.session.commit()
#         return redirect(url_for('list_customers'))
#
#     return render_template('edit_customer.html', customer=customer)
@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get(id)
    form = CustomerForm(obj=customer)

    if form.validate_on_submit():
        form.populate_obj(customer)
        db.session.commit()
        return redirect(url_for('list_customers'))

    return render_template('edit_customer.html', form=form, customer=customer)
@app.route('/customers/delete/<int:id>')
def delete_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('list_customers'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
