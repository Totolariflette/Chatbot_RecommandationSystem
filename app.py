import flask
import script
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
ratings, jokes, jokes_dict, mean_ratings, number_of_ratings = script.initialize()
current_joke_id = 1
users = {}


@app.route('/api/get', methods=['GET'])
def get_one_joke():
    global current_joke_id
    global users

    user_id = request.args.get("user_id", type=int)
    if user_id not in users:
        users[user_id] = [0 for i in range(158)]
    current_joke_id, joke = script.get_recommanded_joke(ratings, jokes_dict,
                                                        number_of_ratings,
                                                        users[user_id])
    response = {'joke': joke}
    return response


@app.route('/api/getbest', methods=['GET'])
def get_best_jokes():
    n = request.args.get("number", default=3, type=int)
    jokes = script.get_popular_jokes(mean_ratings, jokes_dict, n)
    response = {'jokes': jokes}
    return jsonify(response)


@app.route('/api/getworst', methods=['GET'])
def get_worst_jokes():
    n = request.args.get("number", default=3, type=int)
    jokes = script.get_worst_jokes(mean_ratings, jokes_dict, n)
    response = {'jokes': jokes}
    return jsonify(response)


@app.route('/api/rate', methods=['POST'])
def post_rating():
    global users
    rate = request.json["rate"]
    user_id = request.json["user_id"]

    if user_id not in users:
        users[user_id] = [0 for i in range(158)]
    users[user_id][current_joke_id] = rate

    return f'rate: {rate}'


app.run(host='0.0.0.0')
