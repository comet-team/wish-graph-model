import asyncio

import requests

from request_preprocessing.parser import parser


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
    try:
        answer = parser.parse_user_nft(token, answer.json())
        # print(f"Get response successful")
    except:
        print(f"Got bad response")
        answer = []
    return answer


async def get_purchasers_by_creator(token):
    loop = asyncio.get_event_loop()
    get_request = loop.run_in_executor(None, requests.get, 'https://api.rarible.com/protocol/v0.1/ethereum/nft/items/byCreator', {"creator": token})
    answer = await get_request
    try:
        answer = parser.parse_creator_purchasers(token, answer.json())
        # print(f"Get response successful")
    except:
        print(f"Got bad response")
        answer = []
    return answer


async def get_nft_by_creator(token):
    loop = asyncio.get_event_loop()
    get_request = loop.run_in_executor(None, requests.get, 'https://api.rarible.com/protocol/v0.1/ethereum/nft/items/byCreator', {"creator": token, 'size': 5})
    answer = await get_request
    nfts_on_sale = []
    try:
        creators_nfts = parser.parse_creator_nft_on_sale(token, answer.json())
        nfts_on_sale = []
        for nft in creators_nfts:
            nft_info = await get_nft_by_token(nft)
            if len(nft_info) != 0:
                nfts_on_sale.append(nft_info)
        return nfts_on_sale
        # print(f"Get response successful")
    except:
        print(f"Got bad response")
    return nfts_on_sale


async def get_nft_by_token(token):
    loop = asyncio.get_event_loop()
    get_request = loop.run_in_executor(None, requests.get, 'https://api.rarible.org/v0.1/items/ETHEREUM:' + token)
    answer = await get_request
    try:
        answer = parser.parse_nft(answer.json())
    except:
        print(f"Got bad response")
        answer = {}
    return answer
