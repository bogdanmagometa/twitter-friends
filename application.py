from flask import Flask, render_template, request
from mapper import create_map_for_user

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/friends")
def friends():
    user_id = request.form.get('user_id')

    create_map_for_user(user_id)

    return render_template("map.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
