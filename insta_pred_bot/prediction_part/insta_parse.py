import instaloader
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
import re
import pandas as pd

def get_info4acc(L, user_name, df, num_posts=10):
    feats = {}
    prof = instaloader.Profile.from_username(L.context, user_name)
    
    feats['user_name'] = re.sub('[_.]', ' ', user_name)
    feats['is_business'] = 1 if prof.is_business_account else 0
    feats['is_private'] = 1 if prof.is_private else 0
    feats['count_posts'] = prof.mediacount
    feats['count_followers'] = prof.followers
    feats['count_followees'] = prof.followees
    feats['biography'] = prof.biography if prof.biography != None else ' '
    feats['full_name'] = prof.full_name if prof.full_name != None else ' '
    feats['count_igtv'] = prof.igtvcount

    business_category = prof.business_category_name if prof.business_category_name != None else '0'
    feats['business_category_' + business_category] = 1

    num_post, title_len, likes, comms, hashtags, time = np.zeros(6)
    time_1 = datetime.today()
    captions = ''

    for post in prof.get_posts():

        num_post += 1
        pc = post.caption
        captions += ' ' + pc if pc != None else ''
        title_len += len(pc) if pc != None else 0
        likes += post.likes
        comms += post.comments
        hashtags += len(post.caption_hashtags)

        time_2 = post.date_utc
        delta = time_1 - time_2
        time += delta.days * 24 + delta.seconds / 60 / 60
        time_1 = time_2

        if num_post == num_posts:
            break

    feats['post_captions'] = captions[1:] if captions != None else ' '
    feats['lenth_title4post'] = title_len / num_post if num_post != 0 else 0
    feats['likes4post'] = likes / num_post if num_post != 0 else 0
    feats['comms4post'] = comms / num_post if num_post != 0 else 0
    feats['hashtags4post'] = hashtags / num_post if num_post != 0 else 0
    feats['publications_period'] = (time / num_post).round() if num_post != 0 else 0

    for key in feats:
        if key not in df.columns:
            df.loc[0, 'business_category_Other'] = feats[key]
            continue
        df.loc[0, key] = feats[key]
    
    df.fillna(0, inplace=True)

    return df
