import flask
import script
from flask import jsonify, request


app = flask.Flask(__name__)
app.config["DEBUG"] = True
ratings, jokes, jokes_dict, mean_ratings, number_of_ratings = script.initialize()
new_user = [0 for i in range(158)]
current_joke_id = 1


@app.route('/api/get', methods=['GET'])
def get_one_joke():
    global current_joke_id
    current_joke_id, joke = script.get_recommanded_joke(ratings, jokes_dict,
                                                        number_of_ratings,
                                                        new_user)
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
    rate = request.json["rate"]
    new_user[current_joke_id - 1] = rate
    print(new_user[current_joke_id -1])
    return f'rate: {rate}'


app.run()
