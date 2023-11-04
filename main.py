from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from models import Customer, Users  # Import your database models
from customer_forms import CustomerForm, SearchForm  # Import the SearchForm
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
