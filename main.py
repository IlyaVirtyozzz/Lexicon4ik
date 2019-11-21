from constants import db
from database import User, add_new_user


class Main_class():
    def __init__(self, req):
        classes = []
        self.res = {}
        self.req = req
        self.db = db
        self.user_id = req['session']['user_id']
        self.user = self.db.session.query(User).filter_by(user_id=self.user_id).first()
        self.start()

    def check_answer(self, step):

        logging.info(room.get_buttons())
        logging.info(self.req['request']["command"].strip())
        if 'помощь' in list(map(lambda x: x.lower(), self.req['request']['nlu']["tokens"])) or \
                'умеешь' in list(map(lambda x: x.lower(), self.req['request']['nlu']["tokens"])):
            self.res[
                'text'] = 'Это.'

        elif self.req['request']["command"].strip() in room.get_buttons():
            button = room.find_buttons(self.req['request']["command"].strip())
            if button.get("step")  == 0:
                self.user.step = button["step"]
            if button.get("room") or button.get("step") == '0':
                self.user.room_number = button["room"]
            self.db.session.commit()
        else:
            self.res['text'] = 'Я не понимаю'


    def if_new_session(self):
        if not self.user:
            self.new_user()

        self.user.step = str(0)
        self.db.session.commit()

    def new_user(self):
        add_new_user(self.user_id)
        self.user = self.db.session.query(User).filter_by(user_id=self.user_id).first()

    def start(self):
        if self.req['session']['new']:
            self.if_new_session()
        else:
            if self.user.step == 0:
                self.main_menu()
            elif self.user.step == 1:
                self.in_game()

    def main_menu(self):



    def get_response(self):
        return self.res
