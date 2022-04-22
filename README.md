# wish-graph-model
block which creates the reccomendations

1. install quart, requests, pandas, also maybe asyncio if it's not included in common libraries
2. run server/quart_server.py
3. right now only get request like "http://localhost:8081/user_recommend/<user_token>" is handled 
4. you will receive json answer like 
```JSON
{
	"value":{
		"0x00a5b85363308c253b2676da418b18e0def166c4":0.0000000479,
      	"0xf50131d7d2b5239fe1e934658fe3f6131532a437":0.0000000479,
      	"0xcb33844b365c53d3462271cee9b719b6fc8ba06a":0.8335986525,
      	"0xf3477a11f998d51df1b667b78fee8c2302d14bb0":1.1670383914,
      	"0x0bf701fed26dd9091eef64a9a2f9972cefc7237a":5.950162985
  	}
}
```