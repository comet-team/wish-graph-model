import pandas as pd

from server.request_handler import get_nft_by_creator
from server.request_handler import get_nft_by_owner


class ModelControl:
    async def get_user(self, owner):
        return await get_nft_by_owner(owner)

    async def get_level_tree(self, owner, levels=3):
        checked_users = {owner}
        creators_checked = set()
        MAX_LEN_USER_LIST = 20
        MAX_LEN_CREATOR_LIST = 20
        waiting_owners_list = {owner}

        ownership_df = pd.DataFrame({'user_id': [], 'creator_id': [], 'number_owned': [], 'total_value': [], 'level': []})
        for level in range(levels):
            print(f"level : {level}, number waiting {len(waiting_owners_list)}")
            next_waiting_creator_list = set()
            for user in waiting_owners_list:
                user_ownership = await get_nft_by_owner(user)
                user_ownership['level'] = [level] * user_ownership.shape[0]
                ownership_df = pd.concat([ownership_df, user_ownership], ignore_index=True)
                next_waiting_creator_list.update(set(ownership_df['creator_id']))
                if len(next_waiting_creator_list) > MAX_LEN_CREATOR_LIST:
                    break
            next_waiting_creator_list.difference_update(creators_checked)
            creators_checked.update(next_waiting_creator_list)
            waiting_owners_list = set()
            print(f"level : {level}, number waiting {len(next_waiting_creator_list)}")
            for creator in next_waiting_creator_list:
                owner_users = set(await get_nft_by_creator(creator))
                waiting_owners_list.update(owner_users)
                if len(waiting_owners_list) > MAX_LEN_USER_LIST:
                    break
            waiting_owners_list.difference_update(checked_users)
            checked_users.update(waiting_owners_list)

        return ownership_df

    async def get_owner_recommendations(self, owner):
        friend_tree = await self.get_level_tree(owner)
        friend_tree['number_owned'] = (friend_tree['number_owned']-friend_tree['number_owned'].min()+1)/friend_tree['number_owned'].std()
        friend_tree['total_value'] = (friend_tree['total_value'] - friend_tree['total_value'].min()+1)/ friend_tree['total_value'].std()
        friend_tree['value'] = friend_tree['total_value']*friend_tree['number_owned']/(1+friend_tree['level'])
        friend_tree = friend_tree.drop(columns = ['number_owned', 'total_value', 'level'])
        friend_tree = friend_tree.groupby('creator_id').sum()
        friend_tree['value'] = (friend_tree['value'] - friend_tree['value'].min())/friend_tree['value'].std()
        friend_tree.sort_values(by='value',inplace = True)
        print(friend_tree.head())
        return friend_tree


global recommendation_model
recommendation_model = ModelControl()
