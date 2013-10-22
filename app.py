from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    user_id = session.get("user_id")
    if user_id:
        username = model.get_username(user_id)
        return "User %s is logged in!"%username
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)
    if user_id != None:
        flash("User authenticated!")
        session['user_id'] = user_id
    else:
        flash("Password incorrect, there may be a ferret stampede in progress")
    return redirect(url_for("index"))

@app.route("/clear")
def clear_session():
    session.clear()
    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/user/<username>")
def get_user_id(username):
    user_id = model.get_user_id(username)
    return user_id

@app.route("/view_user/<username>")
def view_user(username):
    user_id = (model.get_user_id(username))[0]
    row = model.get_wall_posts(user_id)
    return render_template("wall.html", posts = row, username=username)

@app.route("/view_user/<username>", methods = ["POST"])
def post_to_wall(username):
    content = request.form.get("post")
    user_id = session['user_id']
    return user_id
    model.make_wall_post(user_id, content)
    return redirect("/view_user/<username>")




if __name__ == "__main__":
    app.run(debug = True)
