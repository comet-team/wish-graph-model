import asyncio

import requests
from quart import Quart

from request_preprocessing.parser import Parser

global app
app = Quart(__name__)


def parse_nft_items(owner, answer):
    nft_number = answer['total']
    # item { id : {'supply', 'creators', 'value'}
    items = {}
    # owners with shared owning rights on some nfts {id : number of shared nfts}
    partner_owners = {}
    for i in range(nft_number):
        if not answer['items'][i]['deleted']:
            item_id = answer['items'][i]['id']
            creators = answer['items'][i]['creators']
            item_value = sum((creator['value'] for creator in creators))
            supply = answer['items'][i]['supply']
            owners = answer['items'][i]['owners']
            for other_owner in owners:
                if other_owner != owner:
                    partner_owners[other_owner] = partner_owners.setdefault(other_owner, 0) + 1
            items[item_id] = {'supply': supply, 'creators': [creator['account'] for creator in creators], 'value': item_value}
    return items, partner_owners


async def get_nft_by_owner(token):
    loop = asyncio.get_event_loop()
    get_request = loop.run_in_executor(None, requests.get, 'https://api.rarible.com/protocol/v0.1/ethereum/nft/items/byOwner', {"owner": token})
    answer = await get_request
    print(f"Get response successful")
    parser = Parser(token)
    print(parser.parse_user_nft(token, answer.json()))
    return answer


async def get_nft_by_creator(token):
    loop = asyncio.get_event_loop()
    get_request = loop.run_in_executor(None, requests.get, 'https://api.rarible.com/protocol/v0.1/ethereum/nft/items/byCreator', {"creator": token})
    answer = await get_request
    print(f"Get response successful")
    parser = Parser(token)
    print(parser.parse_creator_purchasers(token, answer.json()))
    return answer


@app.route('/user_recommend/<user_token>', methods=['GET'])
async def get_recommendations(user_token):
    print(f"received request for profile of user {user_token}")
    answer = await get_nft_by_owner(user_token)
    print(f"sending request for profile of user {user_token}")
    return "WHAT???"


@app.route('/creator_recommend/<user_token>', methods=['GET'])
async def get_ideas(user_token):
    print(f"received request for profile of user {user_token}")
    answer = await get_nft_by_creator(user_token)
    print(f"sending request for profile of user {user_token}")
    return "WHAT???"

if __name__ == "__main__":
    port = '8081'
    app.run(port=port, host='0.0.0.0', debug=True, use_reloader=False)