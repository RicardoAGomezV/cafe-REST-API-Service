
import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
        
        #Method 2. Alternatively, do the same thing.
        #return {column.name: getattr(self, column.name) for column in self.__table__.columns}
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """
    Renders the home page.
    """
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    """
    Returns a JSON object containing a random cafe's details.
    """
    
    # Retrieve all cafes from the database, ordered by their ID
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    
    # Select a random cafe from the list of all cafes
    random_cafe = random.choice(all_cafes)
    
    # Return the details of the random cafe in JSON format
    return jsonify(cafe={
        # Omit the id from the response
        # "id": random_cafe.id,
        
        # Include the name of the cafe
        "name": random_cafe.name,
        
        # Include the map URL of the cafe
        "map_url": random_cafe.map_url,
        
        # Include the image URL of the cafe
        "img_url": random_cafe.img_url,
        
        # Include the location of the cafe
        "location": random_cafe.location,
        
        # Put some properties in a sub-category called "amenities"
        "amenities": {
            # Include the number of seats available at the cafe
            "seats": random_cafe.seats,
            
            # Include whether the cafe has a toilet
            "has_toilet": random_cafe.has_toilet,
            
            # Include whether the cafe has WiFi
            "has_wifi": random_cafe.has_wifi,
            
            # Include whether the cafe has power sockets
            "has_sockets": random_cafe.has_sockets,
            
            # Include whether the cafe allows phone calls
            "can_take_calls": random_cafe.can_take_calls,
            
            # Include the price of coffee at the cafe
            "coffee_price": random_cafe.coffee_price,
        }
    })



@app.route("/all")
def all():
    """
    Returns a JSON object containing details of all cafes.
    """
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    
    list_of_cafes_dics=[]
    for cafe in all_cafes:
        cafe_dict=cafe.to_dict()
        list_of_cafes_dics.append(cafe_dict)
        
    return jsonify(list_of_cafes_dics)



@app.route("/search")
def search():
    """
    Returns a JSON object containing details of cafes at a specific location.
    """
    
    
    # Get the location query parameter from the request
    query_location = request.args.get("loc")
    
    # other way to do it
    # result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    # Note, this may get more than one cafe per location
    
    # Perform a database query to find cafes at the specified location
    result = db.session.execute(db.select(Cafe).filter_by(location=query_location))

    # Retrieve all cafes that match the location from the database
    all_cafes = result.scalars().all()
    
    # Check if any cafes were found
    if len(all_cafes) > 0:
        
        # Return a JSON response containing details of all cafes at the location
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        
        # Return a 404 error if no cafes were found at the location
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def post_new_cafe():
    """
    Adds a new cafe to the database.
    """
    
    # Retrieve the API key from the request arguments
    api_key = request.args.get("api_key")
    
    
    # Check if the API key is correct
    if api_key == "TopSecretAPIKey":
            
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()   
        
        return jsonify(response={"success": "Successfully added the new cafe."})
    else:
        # Return an error message if the API key is incorrect
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


# HTTP PUT/PATCH - Update Record
# Updating the price of a cafe based on a particular id:
# example "http://127.0.0.1:5000/update-price/CAFE_ID?new_price=£5.67"

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
# https://flask.palletsprojects.com/en/3.0.x/quickstart/#variable-rules
def patch_new_price(cafe_id):
    
    # Retrieve the new price from the request arguments
    new_price = request.args.get("new_price")
    try:
        
        # Get the cafe object with the given id from the database
        cafe = db.get_or_404(Cafe, cafe_id)
    
    except:
        # Return an error message if the cafe with the given id is not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

    
    # Update the coffee_price attribute of the cafe object
    cafe.coffee_price = new_price
    
    # Commit the changes to the database
    db.session.commit()
    
    # Return a success message in JSON format
    return jsonify(response={"success": "Successfully updated the price."})

  
        

# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    """
    Delete a coffee shop from the database
    """
    
    # Retrieve the API key from the request arguments
    api_key = request.args.get("api_key")
    
    # Check if the API key is correct
    if api_key == "TopSecretAPIKey":
        
        # Get the cafe object with the given id from the database
        cafe = db.get_or_404(Cafe, cafe_id)
        
        # Check if the cafe exists
        if cafe:
            # Delete the cafe object from the database
            db.session.delete(cafe)
            
            # Commit the changes to the database
            db.session.commit()
            
            # Return a success message in JSON format
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        
        else:
            # Return an error message if the cafe with the given id is not found
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        # Return an error message if the API key is incorrect
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

    
if __name__ == '__main__':
    app.run(debug=True)
