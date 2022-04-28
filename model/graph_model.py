import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform, pdist

class ModelControl:
    def get_owner_recommendations(self, owner, connection_df):
        connection_df['total_value'] = (connection_df['total_value'] - connection_df['total_value'].min()) / connection_df['total_value'].std()
        connection_df = connection_df.pivot(index='user_id', columns='creator_id', values=['total_value'])
        connection_df = connection_df.fillna(value=0)
        table = []
        owner_line = np.array(connection_df.loc[owner, 'total_value'])
        for id in connection_df.index:
            pair = np.array([np.array(connection_df.loc[id, 'total_value']), owner_line])
            table.append(pdist(pair, 'sqeuclidean'))
        table = np.array(table).T
        table = 1 - table / np.sqrt(table.std())
        table = np.squeeze(table)
        recommendation_weights = pd.DataFrame({'creator_id': connection_df.columns.get_level_values('creator_id'), 'rate': np.matmul(table, connection_df.loc[:, "total_value"])})

        recommendation_weights.sort_values(by = 'rate', ignore_index=True, inplace=True)
        return recommendation_weights['creator_id']

global recommendation_model
recommendation_model = ModelControl()
