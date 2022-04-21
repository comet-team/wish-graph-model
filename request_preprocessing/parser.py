import pandas as pd


class Parser:
    MAX_CREATORS = 30
    MAX_PURCHASERS = 30

    def __init__(self, owner):
        self.owner = owner

    def parse_user_nft(self, owner, answer):
        nft_number = answer['total']
        loved_creators = {}
        for i in range(nft_number):
            if not answer['items'][i]['deleted'] and int(answer['items'][i]['supply']) < 30:
                try:
                    creators = answer['items'][i]['creators']
                    item_value = sum((creator['value'] for creator in creators))
                    """
                    owners = answer['items'][i]['owners']
                    for other_owner in owners:
                        if other_owner != owner and other_owner not in self.checked_users and other_owner not in self.waiting_owners_list:
                            self.waiting_owners_list.add(other_owner)
                    """
                    for creator in creators:
                        tmp_data = loved_creators.setdefault(creator['account'], {'number_owned': 0, 'total_value': 0})
                        tmp_data['number_owned'] += 1
                        tmp_data['total_value'] += item_value
                        loved_creators[creator['account']] = tmp_data
                except:
                    continue
        user_connections = pd.concat([pd.DataFrame({'user_id': [owner] * len(loved_creators),
                                                    'creator_id': loved_creators.keys(),
                                                    }), pd.DataFrame(loved_creators.values())], axis=1, join='inner')
        if user_connections.shape[0] > Parser.MAX_CREATORS:
            user_connections = user_connections.sort_values(by='total_value', ignore_index=True).iloc[:Parser.MAX_CREATORS]
        return user_connections

    def parse_creator_purchasers(self, creator, creator_wallet):
        nft_number = creator_wallet['total']
        purchasers = dict()
        for i in range(nft_number):
            if not creator_wallet['items'][i]['deleted'] and int(creator_wallet['items'][i]['supply']) < 30:
                try:
                    owners = creator_wallet['items'][i]['owners']
                    for other_owner in owners:
                        if other_owner != creator:
                            purchasers[other_owner] = purchasers.setdefault(other_owner, 0) + 1
                except:
                    continue
        if len(purchasers) > Parser.MAX_PURCHASERS:
            purchasers = list(map(lambda x: x[0], sorted(purchasers.items(), key = lambda x:x[1], reverse=True)[:Parser.MAX_PURCHASERS]))
        else:
            purchasers = purchasers.keys()
        return purchasers

    def get_level_tree(self, owner, answer, levels=6):
        self.checked_users = set()
        self.creators_checked = set()

        waiting_owners_list = {owner}
        waiting_authors_list = set()

        self.ownership_df = pd.DataFrame([], columns=['user_id', 'creator_id', 'number_owned', 'total_value', 'level'])
        for level in range(levels):
            for user in waiting_owners_list:
                user_ownership = self.parse_user_nft(self, owner, answer)
