from flask import *
from mongodb3 import MongoDBHelper
import datetime
import hashlib
from datetime import datetime

web_app = Flask('Bike And Care')


@web_app.route("/")
def login():
    return render_template("home.html")

@web_app.route("/register")
def register():
    return render_template("register1.html")


@web_app.route("/home")
def home():
    return render_template("home.html")


@web_app.route("/register-serviceStation", methods=['POST'])
def register_service_station():
    email = request.form['email']

    db = MongoDBHelper(collection="bike customers")
    existing_station = db.fetch_one({'email': email})

    if existing_station:
        return render_template('error1.html', message=f'{email} already registered')

    station_data = {
        'name': request.form['name'],
        'service_station': request.form['service_station'],
        'email': request.form['email'],
        'bike_company': request.form['bike_company'],
        'bike_model': request.form['bike_model'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
        'createdOn': datetime.now()
    }
    print(station_data)

    db.insert(station_data)

    session['service_station_id'] = str(station_data['_id'])
    session['service_station_name'] = station_data['name']
    session['service_station_email'] = station_data['email']

    return render_template('home.html')


@web_app.route("/login-serviceStation", methods=['POST'])
def login_service_station():
    service_station_data = {
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
    }
    print(service_station_data)

    db = MongoDBHelper(collection="bike customer")
    documents = list(db.fetch(service_station_data))
    if len(documents) == 1:
        session['id'] = str(documents[0]['_id'])
        session['email'] = documents[0]['email']
        session['service_station_id'] = str(documents[0]['_id'])
        session['name'] = documents[0]['name']
        session['service_station_name'] = documents[0]['service_station']
        session['service_station_email'] = documents[0]['email']
        print(vars(session))
        return render_template('register.html')
    else:
        return render_template('error.html', message="Incorrect Email And Password ")


# @web_app.route("/add-customer-service-station", methods=['POST'])
# def add_customer_service_station():
#     service_station_customer_data = {
#         'name': request.form['name'],
#         'phone_number': request.form['phone_number'],
#         'email': request.form['email'],
#         'bike_company': request.form['bike_company'],
#         'bike_model': request.form['bike_model'],
#         'bike_number': request.form['bike_number'],
#         'address': request.form['address'],
#         'bike_next_service': request.form['bike_next_service'],
#         'service_station_email': request.form['service_station_email'],
#         'service_station_id': request.form['service_station_id'],
#         'createdOn': datetime.now()
#     }
#     if len(service_station_customer_data['name']) == 0 or len(service_station_customer_data['phone_number']) == 0 or len(
#             service_station_customer_data['email']) == 0:
#         return render_template('error2.html', message="Name, Phone and Email cannot be Empty")
#     print(service_station_customer_data)
#
#     db = MongoDBHelper(collection="bike customer")
#     db.insert(service_station_customer_data)
#
#     return render_template('success1.html',
#                            message="{} added successfully".format(service_station_customer_data['name']))
#
#
# # @web_app.route("/update-customer-service-station", methods=['POST'])
# # def update_customer_service_station():
# #     customer_data_to_update = {
# #         'name': request.form['name'],
# #         'phone_number': request.form['phone_number'],
# #         'email': request.form['email'],
# #         'address': request.form['address'],
# #         'bike_company': request.form['bike_company'],
# #         'bike_model': request.form['bike_model'],
# #         'bike_number': request.form['bike_number'],
# #         'bike_next_service': request.form['bike_next_service'],
# #     }
# #     if len(customer_data_to_update['name']) == 0 or len(customer_data_to_update['phone_number']) == 0 or len(
# #             customer_data_to_update['email']) == 0:
# #         return render_template('error2.html', message="Name, Phone and Email cannot be Empty")
# #     print(customer_data_to_update)
# #
# #     db = MongoDBHelper(collection="service station customers")
# #     query = {'email': request.form['email']}
# #
# #     print(customer_data_to_update)
# #     print(query)
# #     db.update(customer_data_to_update, query)
# #
# #     return render_template('success1.html',
# #                            message="{} updated successfully".format(customer_data_to_update['name']))
#
#
# @web_app.route("/logout")
# def logout():
#     session['_id'] = ""
#     session['email'] = ""
#     return redirect("/")
#
#
# @web_app.route("/fetch-Customers-of-Service-Station")
# def fetch_customers_of_service_station():
#     db = MongoDBHelper(collection="service station customers")
#     query = {'service_station_id': session['service_station_id']}
#     print("Query:", query)
#     documents = db.fetch(query)
#     print(documents, type(documents))
#     return render_template('customer1.html', documents=documents)
#
#
# @web_app.route("/delete-customer/<id>")
# def delete_customer(id):
#     db = MongoDBHelper(collection="service station customers")
#     query = {'_id': ObjectId(id)}
#     customer = db.fetch(query)[0]
#     db.delete(query)
#     return render_template("success1.html", message="customer with ID {} and name {} Deleted...".format(id, customer['name']))
#
#
# # @web_app.route("/update-customer/<id>")
# # def update_customer(id):
# #     db = MongoDBHelper(collection="service station customers")
# #     query = {'_id': ObjectId(id)}
# #     customer = db.fetch(query)[0]
# #     return render_template("update-customer1.html", customer=customer)
# #
#
# @web_app.route("/search")
# def search():
#     return render_template("search1.html")
#
#
# @web_app.route("/search-customer", methods=["POST"])
# def search_customer():
#     service_station_email = session.get('service_station_email')
#
#     if not service_station_email:
#         print("Service station email not found in the session.")
#         return render_template("error2.html", message="Service station email not found in the session.")
#
#     customer_email = request.form['email']
#
#     print(f"Searching for customer with email: {customer_email} for service station: {service_station_email}")
#
#     db = MongoDBHelper(collection="bike customers")
#
#     query = {
#         'email': customer_email,
#         'service_station_email': service_station_email
#     }
#
#     print("Querying the database with query:", query)
#
#     customers_cursor = db.fetch(query)
#     customers = list(customers_cursor)
#
#     if len(customers) == 1:
#         customer = customers[0]
#         return render_template("customer-profile1.html", customer=customer)
#     else:
#         return render_template("error2.html", message="Customer not found.")
#
#
# @web_app.route("/add-bike/<id>")
# def add_bike(id):
#     db = MongoDBHelper(collection="bike customers")
#     query = {'_id': ObjectId(id)}
#     customers = db.fetch(query)
#     customer = customers[0]
#     return render_template("add-car1.html",
#                            _id=session['service_station_id'],
#                            email=session['service_station_email'],
#                            name=session['service_station_name'],
#                            customer=customer)
#
#
# @web_app.route("/save-bike", methods=["POST"])
# def save_bike():
#     service_station_email = session.get('service_station_email')
#
#     if not service_station_email:
#             print("Service station email not found in the session.")
#             return render_template("error2.html", message="Service station email not found in the session.")
#
#     car_data = {
#         'bike_model': request.form['bike_model'],
#         'bike_number': request.form['bike_number'],
#         'kms_driven': request.form['kms_driven'],
#         'cid': request.form['cid'],
#         'customer_email': request.form['customer_email'],
#         'service_station_id': session['service_station_id'],
#         'service_station_email': service_station_email,
#         'createdOn': datetime.now()
#         }
#
#     if len(car_data['car_name']) == 0 or len(car_data['car_number']) == 0:
#         return render_template('error2.html', message="Name and colour cannot be Empty")
#
#     print(car_data)
#     db = MongoDBHelper(collection="bike customer")
#     db.insert(car_data)
#
#     return render_template('success1.html', message="{} added for customer {} successfully.."
#                            .format(car_data['car_name'], car_data['customer_email']))
#
#
# @web_app.route("/fetch-all-cars")
# def fetch_all_cars():
#     db = MongoDBHelper(collection="bike customer")
#     query = {'service_station_id': session['service_station_id']}
#     documents = db.fetch(query)
#     print(documents, type(documents))
#     return render_template('cars1.html',
#                            email=session['service_station_email'],
#                            name=session['service_station_name'],
#                            documents=documents)
#
#
# @web_app.route("/fetch-cars/<customer_email>")
# def fetch_cars_of_customer(customer_email):
#     service_station_email = session.get('service_station_email')
#
#     if not service_station_email:
#         print("Service station email not found in the session.")
#         return render_template("error2.html", message="Service station email not found in the session.")
#
#     db = MongoDBHelper(collection="bike customer")
#     query = {'email': customer_email}
#     customer = db.fetch(query)[0]
#
#     db_cars = MongoDBHelper(collection="bike customer")
#     query = {'service_station_id': session['service_station_id'], 'customer_email': customer_email}
#     documents = db_cars.fetch(query)
#
#     return render_template('cars1.html',
#                            email=service_station_email,
#                            name=session['service_station_name'],
#                            customer=customer,
#                            documents=documents)
#
#
# @web_app.route("/delete-car/<id>")
# def delete_car(id):
#     db = MongoDBHelper(collection="bike customer")
#     query = {'_id': ObjectId(id)}
#     car = db.fetch(query)[0]
#     db.delete(query)
#     return render_template("success1.html", message="customer with ID {} and car name {} Deleted...".format(id, car['car_name']))
#
#
# @web_app.route("/update-car-service-station/<customer_email>", methods=['POST'])
# def update_car_service_station(customer_email):
#     car_data_to_update = {
#         'bike_model': request.form['bike_model'],
#         'bike_number': request.form['bike_number'],
#         'kms_driven': request.form['kms_driven'],
#         'bike_id': request.form['bike_id'],
#         'customer_email': customer_email,
#         'service_station_id': session['service_station_id'],
#         'createdOn': datetime.now()
#     }
#
#     db = MongoDBHelper(collection="service station cars")
#     query = {'_id': ObjectId(request.form['car_id'])}
#
#     print(car_data_to_update)
#     print(query)
#     db.update(car_data_to_update, query)
#
#     if len(car_data_to_update['car_name']) == 0 or len(car_data_to_update['car_number']) == 0:
#         return render_template('error2.html', message="car name and car number cannot be Empty")
#
#     return render_template('success1.html',
#                            message="{} updated successfully".format(car_data_to_update['car_name']))
#
#
# @web_app.route("/update-bike/<id>")
# def update_bike(id):
#     db = MongoDBHelper(collection="service station cars")
#     query = {'_id': ObjectId(id)}
#     car = db.fetch(query)[0]
#     return render_template("update-cars1.html", car=car, customer_email=car['customer_email'])
#
#
# @web_app.route("/add-service/<id>")
# def add_service(id):
#     db = MongoDBHelper(collection="service station cars")
#     query = {'_id': ObjectId(id)}
#     cars = db.fetch(query)
#     car = cars[0]
#
#     db_customer = MongoDBHelper(collection="service station customers")
#     query_customer = {'email': car['customer_email']}
#     customer = db_customer.fetch(query_customer)[0]
#
#     return render_template("add-services1.html",
#                            _id=session['service_station_id'],
#                            email=session['service_station_email'],
#                            name=session['service_station_name'],
#                            car=car,
#                            customer=customer)
#
#
# @web_app.route("/save-service", methods=["POST"])
# def save_service():
#     service_due_str = request.form['service_due']
#
#     try:
#         service_due = datetime.strptime(service_due_str, "%Y-%m-%d")
#     except ValueError:
#         print("Invalid date format. Use YYYY-MM-DD.")
#         return render_template("error2.html", message="Invalid date format. Use YYYY-MM-DD.")
#
#     print("Parsed service_due:", service_due)
#
#     customer_email = request.form['customer_email']
#     customer_name = request.form['customer_name']
#     phone_number = request.form['phone_number']
#
#     service_data = {
#         'problem': request.form['problem'],
#         'Repaired Parts': request.form['Repaired Parts'],
#         'replaced parts': request.form['replaced parts'],
#         'car type': request.form['car type'],
#         'price': request.form['price'],
#         'service_due': service_due,
#         'cid': request.form['cid'],
#         'customer_email': customer_email,
#         'customer_name': customer_name,
#         'phone_number': phone_number,
#         'car_id': request.form['car_id'],
#         'car_number': request.form['car_number'],
#         'car_name': request.form['car_name'],
#         'service_station_name': session['service_station_name'],
#         'service_station_email': session['service_station_email'],
#         'createdOn': datetime.now()
#     }
#
#     if len(service_data['problem']) == 0:
#         return render_template('error2.html', message="Problem cannot be empty")
#
#     print("Service data:", service_data)
#
#     db = MongoDBHelper(collection="bike customer")
#     db.insert(service_data)
#
#     return render_template('success1.html', message="Service added successfully..")
#
#
# @web_app.route("/fetch-services-cars/<car_number>", methods=["GET", "POST"])
# def fetch_services_of_car(car_number):
#     service_station_email = session.get('service_station_email')
#
#     if not service_station_email:
#         print("Service station email not found in the session.")
#         return render_template("error2.html", message="Service station email not found in the session.")
#
#     if request.method == "POST":
#         service_due_str = request.form['service_due']
#
#         try:
#             service_due = datetime.strptime(service_due_str, "%Y-%m-%d")
#         except ValueError:
#             print("Invalid date format. Use YYYY-MM-DD.")
#             return render_template("error2.html", message="Invalid date format. Use YYYY-MM-DD.")
#
#         print(f"Searching for services for car {car_number} with service_due: {service_due}")
#
#         db_services = MongoDBHelper(collection="bike customer")
#
#
#         query_services = {
#             'bike_number': car_number,
#             'service_station_email': service_station_email,
#         }
#         services_cursor = db_services.fetch(query_services)
#         services = list(services_cursor)
#
#         if services:
#             print(f"Found {len(services)} services for car {car_number}.")
#         else:
#             print(f"No services found for car {car_number} on {service_due}.")
#
#         return render_template('services-cars.html', services=services, car_number=car_number, search_date=service_due_str, service_station_email=service_station_email)
#
#     db_services = MongoDBHelper(collection="bike customer")
#
#     query_services = {
#         'bike_number': car_number,
#         'service_station_email': service_station_email,
#     }
#     services_cursor = db_services.fetch(query_services)
#     services = list(services_cursor)
#     print(services, type(services))
#
#     return render_template('services-cars.html', services=services, car_number=car_number, service_station_email=service_station_email)
#
#
# @web_app.route("/search-service")
# def search_service():
#     return render_template("search-services.html")
#
#
# @web_app.route("/search-service-cars", methods=["POST"])
# def search_service_of_car():
#     service_due_str = request.form['service_due']
#
#     try:
#         service_due = datetime.strptime(service_due_str, "%Y-%m-%d")
#     except ValueError:
#         print("Invalid date format. Use YYYY-MM-DD.")
#         return render_template("error2.html", message="Invalid date format. Use YYYY-MM-DD.")
#
#     service_station_email = session.get('service_station_email')
#
#     if not service_station_email:
#         print("Service station email not found in the session.")
#         return render_template("error2.html", message="Service station email not found in the session.")
#
#     print("Searching for service with service_due:", service_due)
#
#     db = MongoDBHelper(collection="service-station-services")
#     query = {'service_due': service_due, 'service_station_email': service_station_email}
#
#     print("Querying the database with query:", query)
#
#     services_cursor = db.fetch(query)
#     services = list(services_cursor)
#
#     if services:
#         print(f"Found {len(services)} services.")
#         return render_template("service-profile.html", services=services, service_station_email=service_station_email)
#     else:
#         print("No services found.")
#         return render_template("error2.html", message="No services found.")
#
#
# @web_app.route("/search-service-by-car-number")
# def search_service_by_car_number():
#     return render_template("search-services-by-number.html")
#
#
# @web_app.route("/search-service-of-car-by-number", methods=["POST"])
# def search_service_of_car_by_number():
#     car_number = request.form['car_number']
#
#     print("Searching for services for car number:", car_number)
#
#     service_station_email = session.get('service_station_email')
#
#     if not service_station_email:
#         print("Service station email not found in the session.")
#         return render_template("error2.html", message="Service station email not found in the session.")
#
#     db = MongoDBHelper(collection="service-station-services")
#
#     query = {
#         'bike_number': car_number,
#         'service_station_email': service_station_email
#     }
#
#     print("Querying the database with query:", query)
#
#     services_cursor = db.fetch(query)
#     services = list(services_cursor)
#
#     if services:
#         print(f"Found {len(services)} services for car number {car_number}.")
#         return render_template("search-services-by-number-profile.html",
#                                services=services)
#     else:
#         print(f"No services found for car number {car_number}.")
#         return render_template("error2.html", message=f"No services found for car number {car_number}.")
#
#
# @web_app.route("/service-of-cars")
# def customer_index():
#     return render_template("search-service-by-number-for-customer.html")
#
#
# @web_app.route("/search-service-of-car-by-number-profile", methods=["POST"])
# def search_service_of_car_by_number_for_customer():
#     car_number = request.form['car_number']
#
#     print("Searching for services for car number:", car_number)
#     db = MongoDBHelper(collection="service-station-services")
#
#     query = {
#         'bike_number': car_number,
#     }
#
#     print("Querying the database with query:", query)
#
#     services_cursor = db.fetch(query)
#     services = list(services_cursor)
#
#     if services:
#         print(f"Found {len(services)} services for car number {car_number}.")
#         return render_template("search-service-by-number-for-customer-profile.html", services=services)
#     else:
#         print(f"No services found for {car_number}.")
#         return render_template("error3.html", car_number=car_number)
#

def main():
    web_app.secret_key = 'your_secret_key'
    web_app.run(port=8888)


if __name__ == "__main__":
    main()