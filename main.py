# app.py
import base64
import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# app.py (continuation)
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    order = relationship("Order", back_populates="orderedUser")


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
    productCategory = db.Column(db.String(100))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    supplier = relationship("Supplier", back_populates="product")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(250), nullable=False)
    productQuantity = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date, default=datetime.date.today)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    orderedUser = relationship("Users", back_populates="order")


class Supplier(db.Model):
    __tablename__ = "supplier"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.Integer)
    product = relationship("Product", back_populates="supplier")


db.create_all()


@app.route('/')
def home():
    # users = Users.query.all()
    # upload = Users(
    #     firstName="Jay",
    # middleName="Ashok",
    # lastName="Lokhande",
    # userName="jaylokhande",
    # password="123456789"
    # )
    # db.session.add(upload)
    # db.session.commit()
    # print(users)
    # return render_template('index.html', users=users)
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def login():
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


@app.route('/add-products', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'POST':
        file = request.files['file']
        upload = Product(
            productName=request.form.get('productName'),
            productImg=file.read(),
            productDiscription=request.form.get('discription'),
            productPrice=request.form.get('price'),
            productCategory=request.form.get('category')
        )
        db.session.add(upload)
        db.session.commit()
        return render_template('addproduct.html')
    return render_template('addproduct.html')


@app.route('/add-jobs', methods=['GET', 'POST'])
def addJobs():
    if request.method == 'POST':
        upload = Job(
            job_title=request.form.get('job_title'),
            salary=request.form.get('salary')
        )
        db.session.add(upload)
        db.session.commit()
        jobs = Job.query.all()
        return render_template('addJobs.html', jobs=jobs)
    return render_template('addJobs.html')


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
