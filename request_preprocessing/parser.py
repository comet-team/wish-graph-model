import pandas as pd


class Parser:
    MAX_CREATORS = 30
    MAX_PURCHASERS = 30

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

    def parse_nft(self, nft):
        try:
            #print('id', nft['id'])
            #print('meta', nft['meta']['content'][0]['url'])
            return {'id' : nft['id'], 'url' : nft['meta']['content'][0]['url']}
        except:
            return {}

    def parse_creator_nft_on_sale(self, creator, creator_wallet):
        nft_number = creator_wallet['total']
        available_nfts = []
        for i in range(min(nft_number, 10)):
            try:
                if not creator_wallet['items'][i]['deleted'] and \
                        int(creator_wallet['items'][i]['supply']) > 0:
                    available_nfts.append(creator_wallet['items'][i]['id']) #= creator_wallet['items'][i]['lastUpdatedAt']
            except:
                continue
        return available_nfts


global parser
parser = Parser()
