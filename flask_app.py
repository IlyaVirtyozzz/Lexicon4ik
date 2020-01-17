from constants import logging, request, json, app
from main import Main_class

logging.basicConfig(level=logging.INFO, filename='/home/AbilityForAlice/mysite/app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {}
    }

    one = Main_class(response, request.json)
    one.start()
    response = one.get_response()
    if request.json['request'].get("command"):
        if request.json['request']["command"] != "ping":
            logging.info(
                str(response['session']["user_id"][:5]) + " : " + str(request.json['request']["command"]) + "||||" +
                str(response['response']['text']))
    else:
        if request.json['request'].get("payload"):
            logging.info(
                str(response['session']["user_id"][:5]) + " : " + str(
                    request.json['request']["payload"]["text"]) + "||||" +
                str(response['response']['text']))
        else:
            logging.info(
                str(response['session']["user_id"][:5]) + " : " + "||||" +
                str(response['response']['text']))

    return json.dumps(response)
