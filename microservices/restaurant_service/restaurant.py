from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
import config, pyodbc

app = Flask(__name__)
app.secret_key = os.urandom(24)
#conn = pyodbc.connect(config.DATABASE_CONNECTION_STRING)
engine = create_engine(config.DATABASE_CONNECTION_STRING)
Base = declarative_base()

class Dish(Base):
    __tablename__ = 'Dishes'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100))
    Description = Column(String(500))
    Price = Column(Float)
    PreparationTime = Column(Integer)
    DeliveryRange = Column(Integer)
    RestaurantId = Column(Integer, ForeignKey('Restaurant.id'))
    restaurant = relationship("Restaurant", back_populates="dishes")

class RestaurantMenu(Base):
    __tablename__='RestaurantMenus'

    Id = Column(Integer,primary_key=True, autoincrement=True)
    RestaurantId = Column(Integer, ForeignKey('Restaurant.Id'))
    Name = Column(String(100))
    Description = Column(String(255))

class MenuCategories(Base):
    __tablename__='MenuCategories'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100))
    RestaurantMenuId = Column(Integer, ForeignKey('RestaurantMenu.Id'))
    Description = Column(String(255))
    
class RestaurantCategory(Base):
    __tablename__ = "RestaurantCategories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    CategoryName = Column(String(50))

    

class Restaurant(Base):
    __tablename__= "Restaurant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    RestaurantName = Column(String(50))
    RestaurantAddress = Column(String(200))
    RestaurantCategory = Column(String(50))
    dishes = relationship("Dish", back_populates="restaurant")

Session = sessionmaker(bind=engine)

def get_categories():
        session = Session()
        categories = session.query(RestaurantCategory).all()
        session.close()
        return categories

@app.route("/RestaurantService/restaurant", methods=['GET', 'POST'])
def register_service():
    categories = get_categories()
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        category_id = request.form.get('category')

        session = Session()
        try:
            new_restaurant = Restaurant(RestaurantName=name, RestaurantAddress=address, RestaurantCategory=category_id)
            session.add(new_restaurant)
            session.commit()
            flash('Restoran başarıyla eklendi', 'success')
        except Exception as e:
            session.rollback()
            flash(f'Hata oluştu: {str(e)}', 'danger')
        finally:
            session.close()

        return redirect(url_for('register_service'))

    session = Session()
    try:
        restaurants = session.query(Restaurant).all()
    finally:
        session.close()

    return render_template("restaurant.html", categories=categories, restaurants=restaurants)

"""@app.route("/RestaurantService/menu", methods=['GET'])
def list_restaurants():
    session = Session()
    try:
        restaurants = session.query(Restaurant).all()
        return render_template('list_restaurants.html', restaurants=restaurants)
    finally:
        session.close()"""

@app.route("/RestaurantService/menu/<int:restaurant_id>", methods=['GET', 'POST'])
def restaurant_menu(restaurant_id):
    session = Session()
    try:
        restaurant = session.query(Restaurant).get(restaurant_id)
        if restaurant is None:
            flash('Restoran bulunamadı', 'error')
            return redirect(url_for('register_service'))

        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price'))
            prep_time = int(request.form.get('prep_time'))
            delivery_range = int(request.form.get('delivery_range'))

            new_dish = Dish(
                Name=name,
                Description=description,
                Price=price,
                PreparationTime=prep_time,
                DeliveryRange=delivery_range,
                RestaurantId=restaurant_id
            )
            session.add(new_dish)
            session.commit()
            flash('Yemek başarıyla eklendi', 'success')
            return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))

        dishes = session.query(Dish).filter_by(RestaurantId=restaurant_id).all()
        
        return render_template('restaurant_menu.html', 
                               restaurant=restaurant, 
                               dishes=dishes)
    except Exception as e:
        session.rollback()
        flash(f'Hata oluştu: {str(e)}', 'error')
        return redirect(url_for('register_service'))
    finally:
        session.close()



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

