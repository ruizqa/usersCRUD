from flask import Flask, render_template, redirect, request, session
# import the class from friend.py
from user import User
import datetime

app = Flask(__name__)
app.secret_key = 'secret'

@app.route("/")
def form():
    return render_template("create.html")


@app.route('/create', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "first_name": request.form["fname"],
        "last_name" : request.form["lname"],
        "email" : request.form["email"]
    }
    # We pass the data dictionary into the save method from the User class.
    User.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/users')            

@app.route("/users")
def read():
    # call the get all classmethod to get all users
    users = User.get_all()
    return render_template("read.html", users=users)

@app.route("/users/<int:id>")
def show_user(id):
    data = {
        'id': id,
        
    }
    user=User.get_user_info(data)
    user=user[0]
    user['created_at'] = user['created_at'].strftime("%B %d, %Y ")
    user['updated_at'] = user['updated_at'].strftime("%B %d, %Y at %I:%M %p")
    # call the get all classmethod to get all users
    return render_template("show_user.html", user=user)

@app.route("/users/<int:id>/edit")
def edit_user(id):
    data = {
        'id': id
    }
    user=User.get_user_info(data)
    user=user[0]
    # call the get all classmethod to get all users
    session['id'] = id
    return render_template("edit.html", user=user)

@app.route('/update', methods=["POST"])
def update_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    print("El request es", request.form)
    data = {
        'id': session['id'],
        "first_name": request.form["fname"],
        "last_name" : request.form["lname"],
        "email" : request.form["email"]
    }
    # We pass the data dictionary into the save method from the User class.
    User.update(data)
    # Don't forget to redirect after saving to the database.
    return redirect(f"/users/{session['id']}")  


@app.route("/users/<int:id>/destroy")
def destroy(id):
    data={
        'id': id
    }
    # call the get all classmethod to get all users
    User.remove(data)
    
    return redirect('/users')


if __name__ == "__main__":
    app.run(debug=True)
