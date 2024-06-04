
### Title
cafe-REST-API-Service

### Description
Web application developed with Flask and SQLAlchemy that manages a database of cafes. It provides endpoints to perform CRUD operations (Create, Read, Update, Delete) on cafe information, including details such as name, location, coffee price, and available amenities (WiFi, toilets, sockets, etc.). This API is ideal for applications that need to programmatically access and manage cafe information.

### Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [GET /](#get-)
  - [GET /random](#get-random)
  - [GET /all](#get-all)
  - [GET /search](#get-search)
  - [POST /add](#post-add)
  - [PATCH /update-price/\<int:cafe_id>](#patch-update-priceintcafe_id)
  - [DELETE /report-closed/\<int:cafe_id>](#delete-report-closedintcafe_id)
- [Tools Used](#tools-used)
- [Results and Achievements](#results-and-achievements)


### Installation
1. Clone the repository: `git clone https://github.com/username/cafe-wifi-api.git`
2. Navigate to the project directory: `cd cafe-wifi-api`
3. Install the dependencies: `pip install -r requirements.txt`
4. Start the application: `python app.py`

### Usage
To use the API, ensure the application is running and make HTTP requests to the available endpoints. You can use tools like Postman to test the various functionalities.

### API Endpoints
#### GET /
Renders the home page.

#### GET /random
Returns a JSON object containing a random cafe's details.

#### GET /all
Returns a JSON object containing details of all cafes.

#### GET /search
Returns a JSON object containing details of cafes at a specific location. Use the query parameter `loc`.

#### POST /add
Adds a new cafe to the database. Requires a valid `api_key`. Cafe data is sent in the request body.

#### PATCH /update-price/\<int:cafe_id>
Updates the coffee price of a specific cafe. Use the query parameter `new_price`.

#### DELETE /report-closed/\<int:cafe_id>
Deletes a cafe from the database. Requires a valid `api_key`.

### Tools Used
- Flask: Web framework for Python.
- SQLAlchemy: ORM (Object-Relational Mapping) for database interaction.
- SQLite: Lightweight database used for data storage.
- Postman: Tool for testing and documenting the API.

### Results and Achievements
- **Cafe Management**: The API allows efficient management of cafe information.
- **CRUD Operations**: Complete implementation of CRUD operations to handle data.
- **Ease of Use**: The API is user-friendly and can be integrated into other applications.
- **Comprehensive Documentation**: The API is well-documented, making it easy for other developers to use.
