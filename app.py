from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Database connection
try:
    my_client = MongoClient("localhost", 27017)
    my_db = my_client["payments"]
    merchant = my_db["lazy_pay"]
except Exception as e:
    print("Error connecting to database:", e)

@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/reg", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["u_name"]
        email = request.form["u_email"]
        password = request.form["password"]
        phone = int(request.form["u_num"])
        address = request.form["u_add"]

        merchant.insert_one({
            "name": name, "email": email, "phone":phone, "password": password, "address":address
        })
        return redirect("/reg")
    
    else:
        return render_template("registration.html")

@app.route("/lgn", methods=["GET", "POST"])
def lgn_data():
    if request.method == "POST":
        email = request.form["u_email"]
        password = request.form["u_pwd"]
        user = merchant.find_one({"email": email, "password": password})
        if user:
            return redirect("/lgn")
        else:
            return "Invalid credentials"
    else:
        return render_template("login.html")
@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    if request.method == "POST":
        user = request.form["user-id"]
        payment = request.form["payment-id"]
        app = request.form["app"]
        amount = int(request.form["amount"])
        date = request.form["date"]

        merchant.insert_one({
            "user": user, "payment": payment, "app":app, "amount": amount, "date":date
        })
        return redirect("/purchase")
    
    else:
        return render_template("/purchase.html")


@app.route("/home")
def home():
    return "Welcome to your dashboard!"

if __name__ == "__main__":
    app.run(debug=True)
