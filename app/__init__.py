#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html
from libsql_client  import create_client_sync
from app.helpers.session import init_session
from app.helpers.db import connect_db
from app.helpers.errors import register_error_handlers, not_found_error
from dotenv         import load_dotenv
import os
# Create the app
app = Flask(__name__)

# Setup a session for messages, etc.
init_session(app)

# Handle 404 and 500 errors
register_error_handlers(app)

load_dotenv()
TURSO_URL = os.getenv("TURSO_URL")
TURSO_KEY = os.getenv("TURSO_KEY")

client = None

def connect_db():
    global client
    if client==None:
     client = create_client_sync(url=TURSO_URL, auth_token=TURSO_KEY)
    return client


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
     with connect_db() as client:
        # Get all the things from the DB
         sql = "SELECT id, name FROM tasks ORDER BY name ASC"
         result = client.execute(sql)
         things = result.rows

     return render_template("pages/home.jinja")


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------


#-----------------------------------------------------------
# Things page route - Show all the things, and new thing form


#-----------------------------------------------------------
# Thing page route - Show details of a single thing
#-----------------------------------------------------------


#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_thing():
    # Get the data from the form
    name  = request.form.get("name")
    price = request.form.get("price")

    # Sanitize the inputs
    name = html.escape(name)
    price = html.escape(price)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO tasks (name, price) VALUES (?, ?)"
        values = [name, price]
        client.execute(sql, values)

        # Go back to the home page
        flash(f"Task '{name}' added", "success")
        return redirect("/things")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_a_thing(id):
    with connect_db() as client:
        # Delete the thing from the DB
        sql = "DELETE FROM tasks WHERE id=?"
        values = [id]
        client.execute(sql, values)

        # Go back to the home page
        flash("Task deleted", "warning")
        return redirect("/things")


