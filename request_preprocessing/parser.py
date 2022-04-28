import pandas as pd
import numpy as np
import json

class Parser:
    MAX_CREATORS = 30
    MAX_PURCHASERS = 30

    def parse_user_data(self, owner, user_data):
        user_ids, creator_ids, total_values, dates, supply = [], [], [], [], []
        for line in user_data:
            user_ids += [line["user_id"]]
            creator_ids += [line["creator_id"]]
            total_values += [line["total_value"]]
            dates += [line["date"]]
            supply += [line["supply"]]
        connection_df = pd.DataFrame(
            {"user_id": user_ids,
             "creator_id": creator_ids,
             "total_value": total_values,
             "date": pd.to_datetime(dates),
             "supply": supply}
        )
        connection_df = connection_df.fillna(value=np.nan)
        connection_df.sort_values(by = 'date', inplace=True)
        #if connection_df.shape[0] >= 70 and connection_df['creator_id'].unique() >= 50:
        #    connection_df = connection_df.loc[connection_df.groupby('creator_id')['user_id']]
        return connection_df


global parser
parser = Parser()
