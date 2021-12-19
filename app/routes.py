from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ReviewForm, EditEmployeeForm
from app.models import Account, Restaurant, Order, Delivery_Car, Employee, Manager, Review
from sqlalchemy import func

@app.route('/')
@app.route('/index')
def index():
    restaurants = Restaurant.query.all()
    return render_template('index.html', title='Home', restaurants=restaurants)

@app.route('/delivery')
def delivery():
    orders = Order.query.all()
    cars = Delivery_Car.query.all()
    return render_template('delivery.html', title='Delivery', orders=orders, cars=cars)

@app.route('/manager/<manager_id>', methods=['GET', 'POST'])
def manager(manager_id):
    employees = Employee.query.all()
    manager = Manager.query.get(manager_id)
    restaurant = Restaurant.query.filter(manager.manager_id==manager.manager_id).first_or_404()
    cars = Delivery_Car.query.all()
    reviews = Review.query.filter(Review.store_id==manager.store_id)
    rating_average = Review.query.filter(Review.store_id==manager.store_id).with_entities(func.avg(Review.rating).label("average")).first().average
    editEmployeeForm = EditEmployeeForm()

    if editEmployeeForm.validate_on_submit():
        user = Employee.query.get(editEmployeeForm.hidden.data)
    elif request.method == 'GET':
        if editEmployeeForm.hidden.data is not None:
            user = Employee.query.get(editEmployeeForm.hidden.data)
            editEmployeeForm.name = user.name
            print("DATA: " + editEmployeeForm.hidden.data)

    return render_template('manager.html', title='Manager', employees=employees, restaurant=restaurant, cars=cars, reviews=reviews, rating_average=rating_average, editEmployeeForm=editEmployeeForm)
    
@app.route('/review', methods=['GET', 'POST'])
def review():
    restaurants = Restaurant.query.all()
    locations = [(r.store_id, r.location_name) for r in restaurants]
    form = ReviewForm()
    form.store.choices = locations

    if form.validate_on_submit():
        review = Review(rating=form.rating.data, comment=form.comment.data, store_id=form.store.data)
        db.session.add(review)
        db.session.commit()
        flash('Thanks for leaving us a review!')
        return redirect(url_for('index')) 

    return render_template('review.html', title='Manager', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Account(email=form.email.data, name=form.name.data, phone=form.phone.data, address=form.address.data, permission_Type=1)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
