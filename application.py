from flask import Flask, render_template, request
from mapper import create_map_for_user

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/friends", methods=['POST'])
def friends():
    username = request.form.get('username')

    user_exists = create_map_for_user(username)

    if user_exists:
        return render_template("map.html")

    return render_template('failure.html', username=username)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
