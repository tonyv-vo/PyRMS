from app import app, db
from app.models import *

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Account': Account,
        'Employee': Employee,
        'Driver': Driver,
        'Review': Review,
        'Restaurant': Restaurant,
        'Menu': Menu,
        'Customer': Customer,
        'Order': Order,
        'Delivery_Car': Delivery_Car,
        'Item': Item,
        'IngredientComponent': IngredientComponent,
        'FoodItem': FoodItem,
        'DrinkItem': DrinkItem,
        'Manager': Manager
        }