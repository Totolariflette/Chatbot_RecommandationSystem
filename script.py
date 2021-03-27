import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

jokes_number = 158
new_user = [0 for i in range(158)]


def initialize():
    # Downloading data
    ratings = pd.read_csv(
        'April 2015 to Nov 30 2019 - Transformed Jester Data.csv', header=None,
        delimiter=';')
    jokes = pd.read_csv('Dataset4JokeSet.csv', header=None, sep=';')

    # Normalizing data
    number_of_ratings = ratings[0]
    ratings = ratings.iloc[:, 1:]

    for i in range(1, jokes_number + 1):
        ratings[i] = ratings[i].astype('float')

    jokes_dict = {}
    for i in range(1, jokes_number + 1):
        jokes_dict[i] = jokes.iloc[i - 1, 0]

    ratings = ratings.replace(99, 0)

    mean_ratings = pd.DataFrame()
    for i in range(1, 159):
        mean_ratings[i] = [ratings[i][ratings[i] != 0].mean()]
    mean_ratings = mean_ratings.fillna(0)
    mean_ratings = mean_ratings.T
    mean_ratings.rename(columns={0: 'mean_joke_ratings'}, inplace=True)

    return ratings, jokes, jokes_dict, mean_ratings, number_of_ratings


def get_popular_jokes(mean_ratings, jokes_dict, n=3):
    # Recommend the top n most popular jokes
    top_ratings = mean_ratings.sort_values(ascending=False,
                                           by='mean_joke_ratings')[:n]

    top_ids = top_ratings.index.tolist()

    popular_jokes = []
    for e in top_ids:
        popular_jokes.append(jokes_dict[e])
        print(jokes_dict[e] + '\n')
    return popular_jokes


def get_worst_jokes(mean_ratings, jokes_dict, n=3):
    bottom_ratings = mean_ratings.sort_values(ascending=False,
                                              by='mean_joke_ratings')[-n:].iloc[
                     ::-1]
    bottom_ids = bottom_ratings.index.tolist()

    worst_jokes = []
    for e in bottom_ids:
        worst_jokes.append(jokes_dict[e])
        print(jokes_dict[e] + '\n')
    return worst_jokes


def get_recommanded_joke(ratings, jokes_dict, number_of_ratings, user_historic):
    ratings_T = ratings.T
    users_like = ratings_T.corrwith(pd.Series(user_historic))

    users_like_frame = pd.DataFrame(users_like, columns=['Correlation'])

    users_like_frame['Count'] = number_of_ratings
    users_like_frame = users_like_frame[
        users_like_frame['Count'] > 5].sort_values('Correlation',
                                                   ascending=False)

    joke_to_show = 0
    indexs = users_like_frame.index.tolist()

    class Found(Exception): pass
    try:
        for i in indexs:
            for j in range(1, jokes_number + 1):
                if ratings.iloc[i, j] > 5 and user_historic[j] == 0:
                    raise Found
    except Found:
        joke_to_show = j

    print(jokes_dict[j])
    return j, jokes_dict[j]


def write_rating(rate, question_id):
    new_user[question_id] = rate


if __name__ == '__main__':
    ratings, jokes, jokes_dict, mean_ratings, number_of_ratings = initialize()
    get_popular_jokes(mean_ratings, jokes_dict)
    get_worst_jokes(mean_ratings, jokes_dict)

    # Fake user
    new_user = [0 for i in range(158)]
    new_user[72] = new_user[105] = new_user[53] = new_user[89] = new_user[
        32] = 7
    new_user[19] = new_user[155] = new_user[156] = new_user[151] = -7

    get_recommanded_joke(ratings, jokes_dict, number_of_ratings, new_user)

