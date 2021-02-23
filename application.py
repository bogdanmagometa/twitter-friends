from flask import Flask, render_template, request
from mapper import create_map_for_user

app = Flask(__name__)

FIRST_TERM_GRADE = ["96,42", "96.42"]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/genmap", methods=['POST'])
def genmap():
    username = request.form.get('username')
    token = request.form.get('token')

    if token in FIRST_TERM_GRADE:
        token = None

    if username.startswith('@'):
        username = username[1:]

    if is_valid(username):
        world_map = create_map_for_user(username, token)

        if world_map is not None:
            return world_map

    return render_template('failure.html', username=username)


@app.route("/friends", methods=['POST'])
def friends():
    token = request.form.get("token")
    grade = request.form.get("grade")
    grade = grade.strip()

    if grade in FIRST_TERM_GRADE:
        return render_template("friends.html", token=grade)
    elif token:
        return render_template("friends.html", token=token)
    else:
        return 'Grade is not correct and Bearer token is unspecified.'


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
    app.run(host="0.0.0.0", port=55000, debug=True)
