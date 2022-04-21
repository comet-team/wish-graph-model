from request_preprocessing.parser import parser
from server.server import app

if __name__ == "__main__":
    port = '8080'
    app.run(port=port, host='0.0.0.0', debug=True, use_reloader=False)