from flask import Flask, render_template, request
from mapper import create_map_for_user

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/friends", methods=['POST'])
def friends():
    username = request.form.get('username')

    if username.startswith('@'):
        username = username[1:]

    if is_valid(username):
        world_map = create_map_for_user(username)

        if world_map is not None:
            return world_map

    return render_template('failure.html', username=username)


def is_valid(username: str) -> bool:
    """
    Return True if specified username is valid, False otherwise.
    """

    for char in username:
        if (97 <= ord(char) <= 122) or (65 <= ord(char) <= 90) or char == '_':
            continue
        return False

    return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
