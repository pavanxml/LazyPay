from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)
my_client = MongoClient("localhost", 27017)
my_db = my_client["payments"] 
merchant = my_db["lazy_pay"]
@app.route("/",methods=["GET"]) 
def homepage():
    return render_template("index.html")
def payments():
    return render_template("payment.html")
@app.route("/reg_data",methods=["GET"])
def registration():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password=request.form["password"]
        phone = request.form["phone"]
        address = request.form["address"]

        merchant.insert_one({
            "name":name, "email":email, "phone":phone,"password":password, "address":address
        })
        return redirect("/reg_data")
    else:
        return render_template("register.html")
       