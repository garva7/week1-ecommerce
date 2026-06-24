from flask import (
    Flask, render_template, request, redirect, url_for, session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Category, Product, Enquiry
from admin import admin



app = Flask(__name__)
app.register_blueprint(admin)
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
    category_name = request.args.get("category")
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 6

    query = Product.query

    if category_name:
        category = Category.query.filter_by(name=category_name).first()
        if category:
            # collect ids: the category itself + all its subcategories
            ids = [category.id] + [sub.id for sub in category.subcategories]
            query = query.filter(Product.subcategory_id.in_(ids))
        possessive = category_name + "'" if category_name.endswith("s") else category_name + "'s"
        heading = possessive + " Products"
    else:
        heading = "All Products"

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
        heading = f'Search results for "{search}"'

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("products.html",
                           products=pagination.items,
                           heading=heading,
                           pagination=pagination,
                           category=category_name or "",
                           search=search)


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
            session["user_email"] = user.email
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

@app.route("/enquiry", methods=["POST"])
def enquiry():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    enquiry_type = data.get("type", "").strip()
    description = data.get("description", "").strip()

    if not name or not email or not phone or not enquiry_type or not description:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    enq = Enquiry(name=name, email=email, phone=phone,
                  type=enquiry_type, description=description)
    db.session.add(enq)
    db.session.commit()

    return jsonify({"success": True, "message": "Thank you! We'll get back to you soon."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
