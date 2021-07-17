
from flask import Flask, jsonify, request, make_response
import product_data
from db import create_tables
import jwt 
import datetime
from functools import wraps
print ("JWT VERSION:::",jwt.__version__)
app = Flask(__name__)


app.config['SECRET_KEY'] = 'thisisthesolutionkeyiconnect'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') 

        if not token:
            return jsonify({'message' : 'Token is Missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is Invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/products', methods=["GET"])
@token_required
def get_products():
    prods = product_data.get_products()
    return jsonify(prods)


@app.route("/product", methods=["POST"])
def insert_products():
    prod_details = request.get_json()
    productname = prod_details["productname"]
    companyname = prod_details["companyname"]
    rate = prod_details["rate"]
    result = product_data.insert_product(productname, companyname, rate)
    return jsonify(result)


@app.route("/product", methods=["PUT"])
def update_products():
    prod_details = request.get_json()
    id = prod_details["id"]
    productname = prod_details["productname"]
    companyname = prod_details["companyname"]
    rate = prod_details["rate"]
    result = product_data.update_product(id, productname, companyname, rate)
    return jsonify(result)


@app.route("/product/<id>", methods=["DELETE"])
def delete_products(id):
    result = product_data.delete_product(id)
    return jsonify(result)


@app.route("/product/<id>", methods=["GET"])
def get_products_by_id(id):
    result = product_data.get_by_id(id)
    return jsonify(result)

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'secret':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        print("encoded",token)
        print("decoded:",token.decode('UTF-8'))
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" 
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


if __name__ == "__main__":
    create_tables()
    app.run(host="localhost", port=8000, debug=False)
