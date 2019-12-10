from constants import logging, request, json, app
from main import Main_class

logging.basicConfig(level=logging.INFO, filename='/home/AbilityForAlice/mysite/app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/', methods=['POST'])
def main():
    logging.info(request.json['request']["command"])
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {}
    }

    one = Main_class(response, request.json)
    one.start()
    response = one.get_response()
    logging.info(response["response"]["text"])
    return json.dumps(response)
