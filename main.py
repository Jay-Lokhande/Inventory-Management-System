# app.py
import base64
import datetime
# from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin

from flask import render_template, redirect, url_for, request, flash, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# login_manager = LoginManager(app)

# app.py (continuation)
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50))
    lastName = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50), nullable=False)


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    order = relationship("Order", back_populates="orderedCustomer")


class Employees(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    job = relationship("Job", back_populates="jobEmployee")


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    jobEmployee = relationship("Employees", back_populates="job")


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(100))
    productImg = db.Column(db.LargeBinary)
    productDiscription = db.Column(db.String(255))
    productPrice = db.Column(db.Integer)
    # productCategory = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship("Category", back_populates="product")

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    supplier = relationship("Supplier", back_populates="product")


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    product = relationship("Product", back_populates="category")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(250), nullable=False)
    productQuantity = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date, default=datetime.date.today)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    orderedCustomer = relationship("Customer", back_populates="order")


class Supplier(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.Integer)
    product = relationship("Product", back_populates="supplier")


db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    # user = User.query.filter_by(username=username).first()
    # if user and user.check_password(password):
    #     login_user(user)
    #     flash('Logged in successfully.', 'success')
    #     return redirect(url_for('index'))
    # else:
    #     flash('Invalid username or password.', 'error')
    return render_template('login.html')


@app.route('/dashboard')
def index():
    data = {
        'username': 'John Doe',
        'analytics_data': [
            {'metric': 'Visitors', 'value': 1000},
            {'metric': 'Page Views', 'value': 5000},
            # Add more data as needed
        ]
    }
    return render_template('dashboard.html', data=data)


@app.route('/analytics')
def analytics():
    analytics_data = [
        {'metric': 'Clicks', 'value': 300},
        {'metric': 'Conversions', 'value': 25},
        # Add more analytics data as needed
    ]
    return render_template('analytics.html', analytics_data=analytics_data)


@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        supplier_name = request.form.get('company_name')
        phone_number = request.form.get('phone_number')
        new_supplier = Supplier(company_name=supplier_name, phone_number=phone_number)
        db.session.add(new_supplier)
        db.session.commit()
        print(f"Added supplier: {supplier_name}")
        return redirect(url_for('index'))
    return render_template('add_supplier.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Handle the form submission
        username = request.form.get('username')
        # Add additional logic to save the user data to the database or perform any other actions
        print(f"Added user: {username}")
    return render_template('add_user.html')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    suppliers = Supplier.query.all()
    categories = Category.query.all()
    if request.method == 'POST':
        # Handle the form submission
        username = request.form.get('username')
        # Add additional logic to save the user data to the database or perform any other actions
        print(f"Added user: {username}")
    return render_template('addProduct.html', suppliers=suppliers, categories=categories)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        if request.method == 'POST':
            upload = Job(
                job_title=request.form.get('job_title'),
                salary=request.form.get('salary')
            )
            db.session.add(upload)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add_job.html')


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    jobs = Job.query.all()
    if request.method == 'POST':
        print()
        filter_ = request.form.getlist('job_title')
        job = Job.query.filter(Job.job_title == filter_[0]).first()
        print(job)
        upload = Employees(
            firstName=request.form.get('fName'),
            middleName=request.form.get('mName'),
            lastName=request.form.get('lName'),
            userName=request.form.get('uName'),
            password=request.form.get('password'),
            job_id=job.id
        )
        db.session.add(upload)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_employee.html', jobs=jobs)



@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        upload = Category(
            name=request.form.get('name'),
            description=request.form.get('description')
        )
        db.session.add(upload)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addCategory.html')


@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/view_user')
def view_user():
    # Add logic to fetch and display user data
    return render_template('view_user.html')


@app.route('/view_supplier')
def view_supplier():
    suppliers = Supplier.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_supplier.html', suppliers=suppliers)


@app.route('/view_category')
def view_category():
    # Add logic to fetch and display supplier data
    categories = Category.query.all()
    return render_template('view_category.html', categories=categories)


@app.route('/view_customers')
def view_customers():
    customers = Customer.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_customers.html', customers=customers)


@app.route('/view_products')
def view_products():
    products = Product.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_products.html', products=products)


@app.route('/view_employees')
def view_employees():
    employees = Employees.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_employees.html', employees=employees)


@app.route('/view_orders')
def view_orders():
    orders = Order.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_orders.html', orders=orders)


@app.route('/view_jobs')
def view_jobs():
    jobs = Job.query.all()
    # Add logic to fetch and display supplier data
    return render_template('view_jobs.html', jobs=jobs)


# @app.route('/add-products', methods=['GET', 'POST'])
# def addProduct():
#     suppliers = Supplier.query.all()
#     categories = Category.query.all()
#
#     if request.method == 'POST':
#         filter_ = request.form.getlist('comp_name')
#         cat_filter = request.form.get('category')
#         print(cat_filter)
#         category = Category.query.filter(Category.name == cat_filter).first()
#
#         supplier = Supplier.query.filter(Supplier.company_name == filter_[0]).first()
#         file = request.files['file']
#         upload = Product(
#             productName=request.form.get('productName'),
#             productImg=file.read(),
#             productDiscription=request.form.get('discription'),
#             productPrice=request.form.get('price'),
#             # productCategory=request.form.get('category'),
#             category_id=category.id,
#             supplier_id=supplier.id
#         )
#         db.session.add(upload)
#         db.session.commit()
#         return render_template('addproduct.html', suppliers=suppliers, categories=categories)
#     return render_template('addproduct.html', suppliers=suppliers, categories=categories)


@app.route('/settings')
def settings():
    return render_template('settings.html')


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Logged out successfully.', 'success')
#     return redirect(url_for('index'))
# @app.route('/protected')
# @login_required
# def protected():
#     return f'Hello, {current_user.username}!'

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        userName = request.form.get('userName')
        password = request.form.get('password')
        user = Users.query.filter_by(userName=userName).first()
        category = request.form.get('category')
        category_product = Product.query.filter(and_(Product.category == category))
        return render_template('userInterface.html', user=user, category_product=category_product)
    return render_template('admin.html')


@app.route('/products', methods=["GET", "POST"])
def product():
    products = Product.query.all()
    today = datetime.date.today()
    day_month_year = today.strftime("%d %B, %Y")
    if request.method == "POST":
        filter_ = request.form.get('product_selection')
        print(filter_)
        print(filter_)
        products = Product.query.filter(and_(Product.productCategory == filter_))
        products = products or 0
        print(products)
        return render_template('userInterface.html', products=products)

    return render_template('userInterface.html', products=products)


@app.template_filter('b64encode')
def b64encode_filter(s):
    if s:
        return base64.b64encode(s).decode('utf-8')
    else:
        return ""




@app.route('/add-employee', methods=['GET', 'POST'])
def addEmployee():
    jobs = Job.query.all()
    if request.method == 'POST':
        print()
        filter_ = request.form.getlist('job_title')
        job = Job.query.filter(Job.job_title == filter_[0]).first()
        print(job)
        upload = Employees(
            firstName=request.form.get('fName'),
            middleName=request.form.get('mName'),
            lastName=request.form.get('lName'),
            userName=request.form.get('uName'),
            password=request.form.get('password'),
            job_id=job.id
        )
        db.session.add(upload)
        db.session.commit()
    return render_template('addEmployee.html', jobs=jobs)


@app.route('/add-supplier', methods=['GET', 'POST'])
def addSupplier():
    if request.method == 'POST':
        upload = Supplier(
            company_name=request.form.get('company_name'),
            phone_number=request.form.get('phone_num')
        )
        db.session.add(upload)
        db.session.commit()
    return render_template('addSupplier.html')


if __name__ == '__main__':
    app.run(debug=True)
