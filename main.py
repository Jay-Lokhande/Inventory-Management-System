from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# from models import Customer, Users, Employee  # Import your database models
from customer_forms import CustomerForm, SearchForm  # Import the SearchForm
from product_forms import ProductForm  # Import the SearchForm
from employee_forms import EmployeeForm  # Import the EmployeeForm class
from flask_bcrypt import Bcrypt
from flask import flash
from wtforms import Form, StringField

app = Flask(__name__)
app.secret_key = 'dah67uyrtghjerwer3gd32rrg4dwd'  # Replace with your own secret key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize Flask-Bcrypt
login_manager = LoginManager(app)
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
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
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/customers')
# def list_customers():
#     customers = Customer.query.all()
#     return render_template('customers.html', customers=customers)
@app.route('/customers', methods=['GET', 'POST'])
def list_customers():
    search_form = SearchForm()
    customers = []

    if search_form.validate_on_submit():
        search_term = search_form.search_term.data
        # Use SQLAlchemy to filter customers based on the search term (first or last name)
        customers = Customer.query.filter(
            (Customer.first_name.like(f'%{search_term}%')) | (Customer.last_name.like(f'%{search_term}%'))
        ).all()
    else:
        customers = Customer.query.all()

    return render_template('customers.html', customers=customers, search_form=search_form)
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
# @login_required
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
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = Users(username=form.username.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created!', 'success')
#         return redirect(url_for('login'))
#
#     return render_template('register.html', title='Register', form=form
@app.route('/employees')
def list_employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)
@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone_number = form.phone_number.data

        employee = Employee(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('list_employees'))

    return render_template('add_employee.html', form=form)

@app.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get(id)
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        form.populate_obj(employee)
        db.session.commit()
        return redirect(url_for('list_employees'))

    return render_template('edit_employee.html', form=form, employee=employee)
@app.route('/employees/delete/<int:id>')
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('list_employees'))
@app.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('products.html', products=products)
@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        qty_stock = form.qty_stock.data
        price = form.price.data

        product = Product(name=name, description=description, qty_stock=qty_stock, price=price)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('list_products'))

    return render_template('add_product.html', form=form)

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get(id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        return redirect(url_for('list_products'))

    return render_template('edit_product.html', form=form, product=product)
@app.route('/products/delete/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('list_products'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
