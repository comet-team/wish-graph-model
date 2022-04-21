import pandas as pd
import asyncio

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

        ownership_df = pd.DataFrame({'user_id':[], 'creator_id':[], 'number_owned':[], 'total_value':[], 'level' : []})
        print(ownership_df)
        for level in range(levels):
            print(f"level : {level}, number waiting {len(waiting_owners_list)}")
            next_waiting_creator_list = set()
            for user in waiting_owners_list:
                user_ownership = await get_nft_by_owner(user)
                user_ownership['level'] = [level] * user_ownership.shape[0]
                ownership_df = pd.concat([ownership_df, user_ownership], ignore_index = True)
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


global recommendation_model
recommendation_model = ModelControl()