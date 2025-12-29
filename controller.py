from flask import Flask, request, current_app, g
import sqlite3
from datetime import datetime
import click

import db

def create_app():
    app = Flask(__name__)
    # existing code omitted

    db.init_app(app)

    return app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()    

@app.route('/api/products', methods=['POST'])
def create_product():
    if request.method == 'POST':
        data = request.get_json()
    
    # Create new product
    product = Product(
        name=data['name'],
        sku=data['sku'],
        price=data['price'],
        warehouse_id=data['warehouse_id']
    )
    
    db.session.add(product)
    # db.session.commit()	# can be done in a single line
    
    # Update inventory count
    inventory = Inventory(
        product_id=product.id,
        warehouse_id=data['warehouse_id'],
        quantity=data['initial_quantity']
    )
    
    db.session.add(inventory)
    db.session.commit()
    
    return {"message": "Product created", "product_id": product.id}

@app.route("/api/products", methods=['GET'])
def welcome():
    return request.get_json()