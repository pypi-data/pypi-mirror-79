from implicit.als import AlternatingLeastSquares
from tqdm import tqdm
import numpy as np

from rs_tools.utils import encode, to_csc, dict_to_pandas


class Wrapper:
    def fit(
        self,
        df,
        show_progress=True,
        user_col='user_id',
        item_col='item_id',
        rating_col='rating',
    ):
        df, ue, ie = encode(df, user_col, item_col)
        self.ue, self.ie = ue, ie
        item_users = to_csc(df, user_col, item_col, rating_col).T
        self.model.fit(item_users, show_progress)
        df.loc[:, user_col] = ue.inverse_transform(df[user_col])
        df.loc[:, item_col] = ie.inverse_transform(df[item_col])

    def predict(
        self,
        df,
        k,
        filter_already_liked_items=True,
        filter_items=None,
        recalculate_user=False,
        user_col='user_id',
        item_col='item_id',
        rating_col='rating',
    ):
        df.loc[:, user_col] = self.ue.transform(df[user_col])
        df.loc[:, item_col] = self.ie.transform(df[item_col])
        user_items = to_csc(df, user_col, item_col, rating_col)
        res = dict()
        for user in tqdm(range(user_items.shape[0])):
            pred = self.model.recommend(
                user,
                user_items,
                k,
                filter_already_liked_items,
                filter_items,
                recalculate_user,
            )
            res[user] = pred
        df.loc[:, user_col] = self.ue.inverse_transform(df[user_col])
        df.loc[:, item_col] = self.ie.inverse_transform(df[item_col])
        res = dict_to_pandas(res, user_col, 'item+score')
        res.loc[:, item_col] = res.loc[:, 'item+score'].apply(lambda x: x[0])
        res.loc[:, rating_col] = res.loc[:, 'item+score'].apply(lambda x: x[1])
        res.drop('item+score', axis=1, inplace=True)
        return res


class ALS(Wrapper):
    def __init__(
        self,
        factors=100,
        regularization=0.01,
        dtype=np.float32,
        use_native=True,
        use_cg=True,
        use_gpu=False,
        iterations=15,
        calculate_training_loss=False,
        num_threads=0,
    ):
        self.model = AlternatingLeastSquares(
            factors=factors,
            regularization=regularization,
            dtype=dtype,
            use_native=use_native,
            use_cg=use_cg,
            use_gpu=use_gpu,
            iterations=iterations,
            calculate_training_loss=calculate_training_loss,
            num_threads=num_threads,
        )
