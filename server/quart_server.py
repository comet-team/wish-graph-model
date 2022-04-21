import asyncio
from quart import Quart, jsonify
from request_handler import *
from model.graph_model import recommendation_model

global parser
global app
global recommendation_model

app = Quart(__name__)


@app.route('/user_recommend/<user_token>', methods=['GET'])
async def get_recommendations(user_token):
    print(f"received request for profile of user {user_token}")
    # answer = await get_nft_by_owner(user_token)
    answer = await recommendation_model.get_level_tree(user_token)
    print(f"sending request for profile of user {user_token}")
    print(answer)
    return answer.to_json()


@app.route('/creator_recommend/<user_token>', methods=['GET'])
async def get_ideas(user_token):
    print(f"received request for profile of creator {user_token}")
    #answer = await get_nft_by_creator(user_token)
    print(f"sending request for profile of creator {user_token}")
    return "Not available"


if __name__ == "__main__":
    port = '8081'
    app.run(port=port, host='0.0.0.0', debug=True, use_reloader=False)
