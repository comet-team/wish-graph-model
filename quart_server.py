from quart import Quart, jsonify, request

from model.graph_model import recommendation_model
from request_handler import *

global parser
global app
global recommendation_model

app = Quart(__name__)


@app.route('/user_recommend', methods=['GET'])
async def get_recommendations():
    user_token = request.form.get('user')
    user_data = request.form.get('data')
    try:
        max_recommendations = request.form.get('max_recommendation_number')
    except:
        max_recommendations = 30
    try:
        min_recommendations = request.form.get('min_recommendation_number')
    except:
        min_recommendations = 0
    print(f"received request for profile of user {user_token}")
    user_data = parser.parse_user_data(owner = user_token, user_data=user_data);
    answer = recommendation_model.get_owner_recommendations(user_token, user_data, min_recommendations, max_recommendations)
    print(f"sending request for profile of user {user_token}, number tokens: {len(answer)}")
    return jsonify(answer)


@app.route('/creator_recommend/<user_token>', methods=['GET'])
async def get_ideas(user_token):
    print(f"received request for profile of creator {user_token}")
    # answer = await get_nft_by_creator(user_token)
    print(f"sending request for profile of creator {user_token}")
    return "Not available"


@app.route('/creator_wallet/<user_token>', methods=['GET'])
async def get_creator_wallet(user_token):
    print(f"received request for profile of creator {user_token}")
    answer = await get_nft_by_creator(user_token)
    print(f"sending request for profile of creator {user_token}")
    print(answer)
    return "Ok"


if __name__ == "__main__":
    port = '8082'
    app.run(port=port, host='0.0.0.0', debug=True, use_reloader=False)
