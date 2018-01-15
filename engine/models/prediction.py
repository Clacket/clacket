import pandas as pd


class Prediction(object):
    def __init__(self):
        self.raw_list = pd.DataFrame()

    @property
    def users(self):
        return self.list['user_id'].tolist()

    @property
    def list(self):
        mean = self.raw_list.groupby(['user_id'])['rating'].mean()
        df = pd.DataFrame({'user_id': mean.index, 'mean_rating': mean.values})
        return df[df['mean_rating'] > 3]

    def extend(self, ratings):
        self.raw_list = self.raw_list.append(ratings)
