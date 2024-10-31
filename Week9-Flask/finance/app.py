import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
     # Query for the user's stock holdings
    rows = db.execute(
        "SELECT symbol, price AS cost, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id
    )

    holdings = []
    grand_total = 0

    # Calculate each stock's current value and total holdings value
    for row in rows:
        stock = lookup(row["symbol"])
        total_value = stock["price"] * row["shares"]
        total_cost = row["cost"] * row["shares"]
        holdings.append({
            "symbol": stock["symbol"],
            "shares": row["shares"],
            "unit_cost": row["cost"],
            "price": usd(stock["price"]),
            "total_cost": usd(total_cost),
            "total": usd(total_value),
        })
        grand_total += total_value

    # Get the user's available cash balance
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]

    # Add cash to the grand total
    grand_total += cash

    # Render the index page with holdings, cash, and grand total
    return render_template("index.html", holdings=holdings, cash=usd(cash), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # Validate symbol
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol is required.")

        # Validate and parse shares input
        shares_input = request.form.get("shares")
        try:
            # Attempt to convert shares to a float, then check if it's an integer
            shares = float(shares_input)
            if shares != int(shares) or shares <= 0:
                return apology("Shares must be a positive integer.")
            shares = int(shares)  # Convert to integer since it's validated as an integer
        except ValueError:
            return apology("Shares must be a number.")

        # Look up the stock
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Symbol doesn't exist.")

        # Calculate transaction value
        transaction_value = shares * stock["price"]

        # Retrieve user cash
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        # Check for sufficient funds
        if user_cash < transaction_value:
            return apology("Unable to proceed: low balance.")

        # Update user cash and transactions
        balance = user_cash - transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user_id)

        # Record the transaction
        date = datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, stock["price"], date)

        flash("Succeed")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transaction_db = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transaction_db)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to user's account"""
    if request.method == "GET":
        return render_template("add.html")
    else:
        new_cash = int(request.form.get("new_cash"))

        if not new_cash or not new_cash > 0:
            return apology("invalid amount")

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        balance = user_cash + new_cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user_id)

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol is required.")
        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol doesn't exist.")

    return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Username is required.")

        if not password:
            return apology("Password is required.")

        if not confirmation:
            return apology("Confirmation is required.")

        if password != confirmation:
            return apology("Passwords do not match. Please try again.")

        hashed_password = generate_password_hash(password)

        # Check if username already exists in the database
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return apology("Username already exists. Please choose a different one.")

        # Insert the new user into the database
        new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                              username, hashed_password)

        session["user_id"] = new_user
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", symbols=symbols_user)
    else:
        user_id = session["user_id"]

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol is required.")
        shares = int(request.form.get("shares"))
        if shares <= 0:
            return apology("Shares must be a positive integer.")

        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Symbol doesn't exist.")

        transaction_value = shares * stock["price"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        user_shares_db = db.execute(
            "SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        user_shares = user_shares_db[0]["shares"]
        if shares > user_shares:
            return apology("Not enough shares.")

        balance = user_cash + transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, user_id)

        date = datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], (-1)*shares, stock["price"], date)
        flash("Succeed")
        return redirect("/")
