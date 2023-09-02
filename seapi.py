from flask import Flask, request, abort, jsonify
import database as db
db.create_tables()

app = Flask(__name__)


@app.route("/")
def main():
    return "StoryTools API"


@app.route("/create", methods=["POST"])
def create():
    data = request.json

    owner = data['owner']
    token = data['token']
    out_date = data["endDate"]
    email = data['email']

    if not isinstance(data, dict):
        return abort(400)
    if 'owner' not in data or 'token' not in data or out_date in data or 'email' not in data:
        return abort(400)

    r = db.add_token(token, owner, out_date, email)

    return jsonify(r)


@app.route("/register", methods=["POST"])
def reg():
    data = request.json

    email = data['email']
    url = data['url']

    if not isinstance(data, dict):
        return abort(400)
    if 'email' not in data or 'url' not in data:
        return abort(400)

    r = db.register(email, url)

    return jsonify(r)


@app.route("/get/<token>")
def get(token):
    return db.get_token(token)
@app.route("/get2/<token>")
def get2(token):
    return db.get_token_small_info(token)

@app.route("/delete/<token>", methods=["DELETE"])
def delete(token):
    r = db.delete_token(token)
    return jsonify(r)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
