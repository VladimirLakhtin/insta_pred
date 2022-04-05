import instaloader
from prediction_part.insta_parse import get_info4acc
import pandas as pd
from joblib import load
import pickle
import scipy

vect_user_names = load(open('prediction_part/tfidf/vect_user_names.pk', 'rb'))
vect_posts = load(open('prediction_part/tfidf/vect_posts.pk', 'rb'))
vect_bios = load(open('prediction_part/tfidf/vect_bios.pk', 'rb'))
vect_names = load(open('prediction_part/tfidf/vect_full_names.pk', 'rb'))


def get_X(L, user_name, df):

    info = get_info4acc(L, user_name, df, num_posts=10)

    user_names = vect_user_names.transform(info.user_name)
    posts = vect_posts.transform(info.post_captions)
    bios = vect_bios.transform(info.biography)
    names = vect_names.transform(info.full_name)

    X_new = scipy.sparse.hstack([info.drop(['post_captions', 'full_name', 'biography', 'user_name'], axis=1), 
                                        names, posts, bios, user_names])

    return X_new

def get_pred(user_name):

    df = pd.read_csv('prediction_part/data_zero.csv')

    model = pickle.load(open('prediction_part/model/insta_model.sav', 'rb')) 

    L = instaloader.Instaloader()

    X = get_X(L, user_name, df)

    pred = model.predict(X)[0]

    return pred

