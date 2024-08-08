#order.py
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
import config
from flask import session as flask_session
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Flash mesajları için gerekli

engine = create_engine(config.DATABASE_CONNECTION_STRING)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class RestaurantCategory(Base):
    __tablename__ = "RestaurantCategories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(50))
    restaurants = relationship("Restaurant", back_populates="category")

class Restaurant(Base):
    __tablename__ = 'Restaurant'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Restaurantname = Column(String(50))
    Restaurantaddress = Column(String(200))
    RestaurantCategory = Column(Integer, ForeignKey('RestaurantCategories.id'))
    category = relationship("RestaurantCategory", back_populates="restaurants")

class Dishes(Base):
    __tablename__ ="Dishes"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100))
    Description = Column(String(255))
    Price = Column(DECIMAL(10,2))
    PreparationTime = Column(Integer)
    RestaurantId = Column(Integer, ForeignKey('Restaurant.Id'))

@app.route("/OrderService/restaurantcategories", methods=['GET', 'POST'])
def order_service():
    session = Session()
    categories = session.query(RestaurantCategory).all()
    
    if request.method == 'POST':
        category_id = request.form.get('category')
        if category_id and category_id.isdigit():
            return redirect(url_for('category_restaurants', category_id=int(category_id)))
        else:
            flash("Lütfen geçerli bir kategori seçin.", "error")
    
    session.close()
    return render_template("Order.html", categories=categories)

@app.route("/OrderService/restaurantcategories/<int:category_id>")
def category_restaurants(category_id):
    session = Session()
    try:
        category = session.query(RestaurantCategory).filter_by(id=category_id).first()
        if category:
            restaurants = session.query(Restaurant).filter_by(RestaurantCategory=category_id).all()
            return render_template("category_restaurants.html", restaurants=restaurants, category_name=category.CategoryName)
        else:
            flash("Kategori bulunamadı", "error")
            return redirect(url_for('order_service'))
    except Exception as e:
        flash(f"Bir hata oluştu: {str(e)}", "error")
        return redirect(url_for('order_service'))
    finally:
        session.close()

@app.route("/OrderService/restaurant/<int:restaurant_id>")
def restaurant_dishes(restaurant_id):
    session = Session()
    try:
        restaurant = session.query(Restaurant).filter_by(Id=restaurant_id).first()
        if restaurant:
            dishes = session.query(Dishes).filter_by(RestaurantId=restaurant_id).all()
            return render_template("restaurant_dishes.html", restaurant=restaurant, dishes=dishes)
        else:
            flash("Restoran bulunamadı", "error")
            return redirect(url_for('order_service'))
    except Exception as e:
        flash(f"Bir hata oluştu: {str(e)}", "error")
        return redirect(url_for('order_service'))
    finally:
        session.close()

@app.route("/OrderService/add_to_cart", methods=['POST'])
def add_to_cart():
   
    cart = json.loads(request.headers.get('X-Session-Cart', '[]'))
    
    dish_id = request.form.get('dish_id')
    restaurant_id = request.form.get('restaurant_id')
    
    session = Session()
    try:
        dish = session.query(Dishes).filter_by(Id=dish_id).first()
        if dish:
            cart_item = {
                'dish_id': dish.Id,
                'name': dish.Name,
                'price': float(dish.Price),
                'restaurant_id': restaurant_id
            }
            cart.append(cart_item)
            flash(f"{dish.Name} sepete eklendi!", "success")
        else:
            flash("Yemek bulunamadı.", "error")
    except Exception as e:
        flash(f"Bir hata oluştu: {str(e)}", "error")
    finally:
        session.close()
    
  
    response = make_response(redirect(url_for('restaurant_dishes', restaurant_id=restaurant_id)))
    response.headers['X-Session-Cart'] = json.dumps(cart)
    return response


@app.route("/cart")
def view_cart():
   
    cart = json.loads(request.headers.get('X-Session-Cart', '[]'))
    total = sum(item['price'] for item in cart)
    
   
    response = make_response(render_template("cart.html", cart=cart, total=total))
    response.headers['X-Session-Cart'] = json.dumps(cart)
    return response
@app.route("/remove_from_cart", methods=['POST'])
def remove_from_cart():
    item_index = int(request.form.get('item_index'))
    cart = flask_session.get('cart', [])
    if 0 <= item_index < len(cart):
        removed_item = cart.pop(item_index)
        flask_session.modified = True
        flash(f"{removed_item['name']} sepetten çıkarıldı.", "success")
    else:
        flash("Ürün bulunamadı.", "error")
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)