import pandas as pd


class Prediction(object):
    def __init__(self, predicted_type='mean'):
        self.raw_list = pd.DataFrame()
        self.type = predicted_type

    @property
    def users(self):
        return self.list['user_id'].tolist()

    @property
    def list(self):
        if self.raw_list.empty:
            return pd.DataFrame(columns=['user_id', 'mean_rating'])
        else:
            ratings_grouped = self.raw_list.groupby(['user_id'])['rating']
            if self.type == 'mean':
                agg = ratings_grouped.mean()
            elif self.type == 'max':
                agg = ratings_grouped.max()
            else:
                agg = ratings_grouped.min()
            df = pd.DataFrame({'user_id': agg.index,
                               'mean_rating': agg.values})
            return df

    def extend(self, ratings):
        self.raw_list = self.raw_list.append(ratings)
