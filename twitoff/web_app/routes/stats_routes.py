from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

from flask import Blueprint, jsonify, request , render_template, flash, redirect

from web_app.models import User
from web_app.stats_models import load_model
from web_app.services.basilica_service import connection as basilica_connection

stats_routes = Blueprint("stats_routes", __name__)

# TODO: accept some inputs related to the iris training data (x values)
@stats_routes.route('/stats/iris')
def iris():    
    X, y = load_iris(return_X_y=True)
    # clf = LogisticRegression(random_state=42, solver='lbfgs', multi_class='multinomial')
    clf = load_model() # make sure to pre-train the model first!
    result = str(clf.predict(X[:2, :]))
    print('PREDICTION', result)
    return result # TODO: return as JSON

@stats_routes.route('/stats/predict', methods=['POST'])
def twitoff_predict():    
    print("PREDICT ROUTE...")
    print("FORM DATA:", dict(request.form))
    #> {'screen_name_a': 'elonmusk', 'screen_name_b': 's2t2', 'tweet_text': 'Example tweet text here'}
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]
    
    print(screen_name_a, screen_name_b, tweet_text)

    #
    # train a model
    #

    tweet_embeddings = []
    tweet_labels = []
    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()
    tweets_a = user_a.tweets
    tweets_b = user_b.tweets
    all_tweets = tweets_a + tweets_b 
    # [1,2,3] + [4,5,6]
    # = [1, 2, 3, 4, 5, 6]

    for tweet in all_tweets:
        # add embeddings and the corresponding user name to the lists above
        tweet_embeddings.append(tweet.embedding)
        tweet_labels.append(tweet.user.screen_name)

    print('EMBEDDINGS:', len(tweet_embeddings), 'LABELS:', len(tweet_labels))

    classifier = LogisticRegression(random_state=42, solver='lbfgs', multi_class='multinomial')
    classifier.fit(tweet_embeddings, tweet_labels)

    # fetch - refer to book_routes.py

    # TODO: make a prediction and return it

    example_tweet_embedding = basilica_connection.embed_sentence(tweet_text, model='twitter')
    result = classifier.predict([example_tweet_embedding])
    # Reshape your data either using array.reshape(-1, 1) if your data has a single feature 
    # or array.reshape(1, -1) if it contains a single sample.
    # fix - put 'example_tweet_embedding' in brackets to make it into a list
    print('RESULT:', result[0])

    return render_template('prediction_results.html', 
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely=result[0]
    )