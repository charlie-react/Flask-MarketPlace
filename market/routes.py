

from market import app,db
from flask import render_template,redirect,url_for,flash,request
from market.models import Item,User
from market.form import RegisterForm, LoginForm,PurchaseForm
from flask_login import login_user,logout_user,login_required,current_user

app.config["SECRET_KEY"] = "4f0c682ff4a41c84201e484e"

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/market",methods=["GET","POST"])
@login_required
def market_page():

    purchase_form = PurchaseForm()
    if request.method == "POST":
       purchased_item =request.form.get('purchased_item')
       item =Item.query.filter_by(name=purchased_item).first()
       if item:
          item.owner =current_user.id
          current_user.budget -= item.price
          db.session.add(item)
          db.session.add(current_user)
          db.session.commit()
    items = Item.query.all()
    return render_template("market.html",items=items,purchase_form=purchase_form)

@app.route("/register",methods=["GET","POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Account created. Logged In Successfully,{user.username}",category="success")
        return redirect(url_for("market_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg,category="danger")
    return render_template("register.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.verify_password(password_plaintext=form.password.data):
            login_user(attempted_user)
            flash(f"Logged In Successfully,{attempted_user.username}",category="success")
            return redirect(url_for("market_page"))
        else:
            flash(f'Login details incorrect.Please try again ',category="danger")
    return render_template("login.html",form=form)
@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("Logged Out",category="info")
    return redirect(url_for("home_page"))


