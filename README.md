# wish-graph-model
Local server which is responsible for making decisions based on ready graph sent in request in json format from main server. 
Right now a primitive analogy of Collaborative Filtering exists. In the future the normal (embedding-idea) model is going to be created and tested. 
1. install quart, pandas, numpy, also maybe asyncio if it's not included in common libraries
2. run quart_server.py
3. right now only get request like "http://localhost:8081/user_recommend" is handled 
4. the request must have a form like 
```JSON
{
  "user": <user_token>, 
  "data": [
        { "user_id" : <token>, 
          "creator_id" : <token>, 
          "total_value": <float>, 
          "date":  <dd.mm.yyyy>, 
          "supply" : <int>
        }
  	]
}
```
5. you will receive json answer like (a list of sorted recommended creator tokens - the first ones are more relevant)
```JSON
	["0x00a5b85363308c253b2676da418b18e0def166c4",
      	"0xf50131d7d2b5239fe1e934658fe3f6131532a437",
      	"0xcb33844b365c53d3462271cee9b719b6fc8ba06a",
      	"0xf3477a11f998d51df1b667b78fee8c2302d14bb0",
      	"0x0bf701fed26dd9091eef64a9a2f9972cefc7237a"
  	]
```