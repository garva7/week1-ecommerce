"""ShopEasy - Flask application (Week 3).

Routes:
  /                 home page (categories from the database)
  /products         product listing, optional ?category=Men filter
  /product/<id>     single product detail (discount + stock)
  /about            about page
  /register         create an account (INSERT into users, hashed password)
  /login            log in (fetch user, check hashed password, start session)
  /logout           end the session
"""

from flask import (
    Flask, render_template, request, redirect, url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Category, Product

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# ----------------------------------------------------------------------
# Public pages
# ----------------------------------------------------------------------
@app.route("/")
def index():
    # Only top-level categories (the ones without a parent) on the homepage.
    categories = Category.query.filter_by(parent_id=None).all()
    return render_template("index.html", categories=categories)


@app.route("/products")
def products():
    category_name = request.args.get("category")  # None when not provided

    if category_name:
        category = Category.query.filter_by(name=category_name).first()
        items = category.products if category else []
        # Correct possessive: Men's / Women's / Kids'
        possessive = category_name + "'" if category_name.endswith("s") else category_name + "'s"
        heading = possessive + " Products"
    else:
        items = Product.query.all()
        heading = "All Products"

    return render_template("products.html", products=items, heading=heading)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)

    # Calculate the discounted price (kept as whole rupees).
    discount = float(product.discount_percent or 0)
    final_price = round(float(product.price) - float(product.price) * discount / 100)

    return render_template("product_detail.html", product=product, final_price=final_price)


@app.route("/about")
def about():
    return render_template("about.html")


# ----------------------------------------------------------------------
# Authentication
# ----------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        password = request.form.get("password", "")

        # Server-side validation.
        error = None
        if not name or not email or not password:
            error = "Name, email and password are required."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif User.query.filter_by(email=email).first():
            error = "An account with that email already exists."

        if error:
            flash(error, "danger")
            return render_template("register.html", name=name, email=email,
                                   phone=phone, address=address)

        # Store the password as a secure hash, never as plain text.
        user = User(
            name=name, email=email, phone=phone, address=address,
            password=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        # check_password_hash compares the typed password to the stored hash.
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash("Welcome back, " + user.name + "!", "success")
            return redirect(url_for("index"))

        flash("Invalid email or password.", "danger")
        return render_template("login.html", email=email)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()  # destroy the session
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
