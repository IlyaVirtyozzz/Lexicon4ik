from constants import logging, request, json, app
from main import Main_class

logging.basicConfig(level=logging.INFO, filename='/home/AbilityForAlice/mysite/app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/', methods=['POST'])
def main():
    if request.json['request']["command"] != "ping":
        logging.info(request.json['session']["user_id"][:5] + " : " + request.json['request']["command"])
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {}
    }

    one = Main_class(response, request.json)
    one.start()
    response = one.get_response()

    return json.dumps(response)
