import pandas as pd
import numpy as np

class ModelControl:
    def get_owner_recommendations(self, owner, connection_df):
        connection_df['total_value'] = (connection_df['total_value'] - connection_df['total_value'].min()) / connection_df['total_value'].std()
        connection_df = connection_df.pivot(index='user_id', columns='creator_id', values=['total_value'])
        connection_df = connection_df.fillna(value=0)
        table = []
        for id in connection_df.index:
         table.append(np.array(connection_df.loc[id, 'total_value']))
        table = np.array(table)
        line = np.array(connection_df.loc[owner, 'total_value'])
        recommendation_weights = pd.DataFrame({'creator_id': connection_df.columns.get_level_values('creator_id'), 'rate': np.matmul(np.dot(line, table.T), table)})
        recommendation_weights.sort_values(by = 'rate', ignore_index=True, inplace=True)
        return recommendation_weights['creator_id']

global recommendation_model
recommendation_model = ModelControl()
