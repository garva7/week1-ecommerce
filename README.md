# ShopEasy — Flask + MySQL (Week 3)

A small e-commerce site built with **Flask**, **Jinja2 templates**, and a
database via **Flask-SQLAlchemy**. It runs on **SQLite** with zero setup, and
switches to **MySQL** by changing one line.

---

## 1. Quick start (SQLite — works immediately)

From this folder, in a terminal:

```bash
# 1. Create a virtual environment (only the first time)
python -m venv .venv

# 2. Activate it
#    Windows (PowerShell):
.venv\Scripts\Activate.ps1
#    Windows (Git Bash):
source .venv/Scripts/activate

# 3. Install the libraries
pip install -r requirements.txt

# 4. Create the database tables + sample data
python seed.py

# 5. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

**Demo login:** `demo@shopeasy.com` / `demo123` (or create your own via *Sign Up*).

> `python seed.py` resets the database to its starting state any time you want.

---

## 2. Switching to MySQL (with XAMPP)

### Install & start MySQL
1. Download **XAMPP** from <https://www.apachefriends.org> and install it.
2. Open the **XAMPP Control Panel** and click **Start** next to **MySQL**
   (also start **Apache** if you want phpMyAdmin).
3. Click **Admin** next to MySQL to open **phpMyAdmin** in your browser
   (or go to <http://localhost/phpmyadmin>).

### Create the database
In phpMyAdmin → **New** → create a database named **`shopeasy`**.
(You can let the app create the tables, or run `schema.sql` under the
*SQL* tab to create them by hand — both work.)

### Point the app at MySQL
1. Make sure the MySQL driver is installed (it's in requirements.txt):
   `pip install PyMySQL`
2. Open **`config.py`** and switch the two database lines:
   ```python
   # SQLALCHEMY_DATABASE_URI = "sqlite:///shopeasy.db"
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/shopeasy"
   ```
   (XAMPP's default user is `root` with an **empty** password — that's the
   `root:` with nothing after the colon.)
3. Recreate the tables + data in MySQL:
   ```bash
   python seed.py
   ```
4. Run the app: `python app.py`

You can now see the `users`, `categories`, and `products` tables (and run
SELECT/INSERT/UPDATE/DELETE queries) inside phpMyAdmin.

---

## 3. Project structure

```
app.py            Flask routes (home, products, detail, register, login, logout)
models.py         Database tables as Python classes (User, Category, Product)
config.py         Database connection setting (SQLite <-> MySQL switch)
seed.py           Creates the tables and inserts sample data
schema.sql        The same tables written as raw MySQL (reference)
requirements.txt  Python packages to install
templates/        Jinja2 HTML (base + header + footer + pages)
static/           style.css and main.js

```
