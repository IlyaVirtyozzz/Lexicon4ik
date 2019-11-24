from constants import logging, request, json
from main import Main_class

logging.basicConfig(level=logging.INFO, filename='/home/IlyaVirtyozzzproject/mysite/app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
    }

    one = Main_class(request.json)
    one.start()
    response['response'] = one.get_response()
    logging.info('Request: %r', response)
    return json.dumps(response)