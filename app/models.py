from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Account(UserMixin, db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    permission_Type = db.Column(db.Integer)
    phone = db.Column(db.Integer, unique=True)
    address = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_id(self):
        return self.account_id
        
class Employee(Account):
    employee_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), primary_key=True)
    
    wage = db.Column(db.Float)
    position = db.Column(db.String(64))
    sin = db.Column(db.Integer, index=True, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("restaurant.store_id"))
    restaurant = db.relationship("Restaurant")

    def __repr__(self):
        return '<Employee {}>'.format(self.employee_id)

class Driver(Employee):
    drivers_license = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
    orders = db.relationship("Order", back_populates="driver")

    def __repr__(self):
        return '<Driver {}>'.format(self.drivers_license)
        
class Manager(Employee):
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)

    def __repr__(self):
        return '<Customer {}>'.format(self.manager_id)
        
class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    store_id = db.Column(db.Integer, db.ForeignKey('restaurant.store_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    customer = db.relationship("Customer")

    def __repr__(self):
        return '<Review {}>'.format(self.review_id)
        
class Restaurant(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    opening_hours = db.Column(db.String(200))
    address = db.Column(db.String(150))
    delivery_range = db.Column(db.Integer)
    location_name = db.Column(db.String(150))
    employees = db.relationship("Employee", back_populates="restaurant")
    manager = db.relationship("Manager", overlaps="employees,restaurant")

    def __repr__(self):
        return '<Restaurant {}>'.format(self.location_name)

class Menu(db.Model):
    menu_name = db.Column(db.String(100), primary_key=True)
    category = db.Column(db.String(100))
    description = db.Column(db.String(200))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    store_id = db.Column(db.Integer, db.ForeignKey('restaurant.store_id'))

    def __repr__(self):
        return '<Restaurant {}>'.format(self.menu_name)

class Customer(Account):
    customer_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), primary_key=True)
    orders = db.relationship("Order", backref="customer", lazy="dynamic")
    comments = db.relationship("Review", back_populates="customer")

    def __repr__(self):
        return '<Customer {}>'.format(self.customer_id)

class Order(db.Model):
    order_number = db.Column(db.Integer, primary_key=True)
    transaction_time = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_time = db.Column(db.DateTime)
    total_cost = db.Column(db.Float)
    items = db.relationship("Item", backref="order", lazy="dynamic")
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    is_current = db.Column(db.Boolean, default=True)
    drivers_license = db.Column(db.Integer, db.ForeignKey('driver.drivers_license'))
    driver = db.relationship("Driver")
    # items = db.relationship("Customer", backref="order", lazy="dynamic")

    def __repr__(self):
        return '<Order {}>'.format(self.order_number)

class Delivery_Car(db.Model):
    license_plate = db.Column(db.String(10), primary_key=True)
    mileage = db.Column(db.Integer)
    car_colour = db.Column(db.String(10))
    car_model = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __repr__(self):
        return '<Delivery Car {}>'.format(self.license_plate)

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    size = db.Column(db.String(20))
    cost = db.Column(db.Float)
    description = db.Column(db.String(200))
    ingredient_component = db.relationship("IngredientComponent", back_populates="item")
    order_number = db.Column(db.Integer, db.ForeignKey('order.order_number'), nullable=True)
    
    def __repr__(self):
        return '<Item {}>'.format(self.name)

class IngredientComponent(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    cost = db.Column(db.Float)
    calories = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'))
    item = db.relationship("Item", back_populates="ingredient_component")

    def __repr__(self):
        return '<IngredientComponent {}>'.format(self.name)

class FoodItem(Item):
    food_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), primary_key=True)
    allergens = db.Column(db.String(100))

    def __repr__(self):
        return '<FoodItem {}>'.format(self.food_id)

class DrinkItem(Item):
    drink_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), primary_key=True)
    drink_capacity = db.Column(db.Integer)

    def __repr__(self):
        return '<DrinkItem {}>'.format(self.drink_id)

@login.user_loader
def load_user(account_id):
    return Account.query.get(int(account_id))