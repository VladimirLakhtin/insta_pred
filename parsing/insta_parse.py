import instaloader
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
import pandas as pd

def get_info(L, user_name, num_posts=10):
    
    feats = {}
    prof = instaloader.Profile.from_username(L.context, user_name)
    
    feats['user_name'] = user_name
    feats['is_business'] = prof.is_business_account
    feats['business_category'] = prof.business_category_name if prof.is_business_account else None
    feats['is_private'] = prof.is_private
    feats['count_posts'] = prof.mediacount
    feats['count_followers'] = prof.followers
    feats['count_followees'] = prof.followees
    feats['is_verified'] = prof.is_verified
    feats['biography'] = prof.biography if prof.biography != '' else None
    feats['full_name'] = prof.full_name if prof.full_name != '' else None
    feats['count_igtv'] = prof.igtvcount

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
    
    feats['post_captions'] = captions[1:] if captions != '' else None
    feats['lenth_title4post'] = title_len / num_post if num_post != 0 else 0
    feats['likes4post'] = likes / num_post if num_post != 0 else 0
    feats['comms4post'] = comms / num_post if num_post != 0 else 0
    feats['hashtags4post'] = hashtags / num_post if num_post != 0 else 0
    feats['publications_period'] = (time / num_post).round() if num_post != 0 else None

    return feats


def get_user_names(L, user_name, from_followers=True, num_accounts=100):
    
    i=0 
    df = pd.DataFrame(columns=['user_name'])

    try:
        profile = instaloader.Profile.from_username(L.context, user_name)
    except Exception:
        print(f'Не удалось подключиться к профилю {user_name}')
        return df

    gen_accounts = profile.get_followers() if from_followers else profile.get_followees()
    
    for foll in tqdm(gen_accounts):
        
        foll_name = foll.username
        df.loc[i, 'user_name'] = foll_name
        i += 1
        
        if i == num_accounts:
            break

    return df