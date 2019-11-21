from constants import db, data, random


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    room_number = db.Column(db.String, unique=False, nullable=False)
    step = db.Column(db.Integer, unique=False, nullable=False)
    points = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return "<User {} {} {} {} {}>".format(self.id, self.user_id, self.step, self.room_number, self.money)


class Line_Vocabulary_words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    line = db.Column(db.String, unique=False, nullable=False)


def add_new_user(user_id):
    user = User(user_id=user_id, step=0, room_number='0')
    db.session.add(user)
    db.session.commit()


def add_new_vocline(user_id):
    voc_list = data['vocabulary_words'][:]
    random.shuffle(voc_list)
    line = ",".join(voc_list)
    one = Line_Vocabulary_words(user_id=user_id, line=line)
    db.session.add(one)
    db.session.commit()


def delete_vocline(user_id):
    one = db.session.query(Line_Vocabulary_words).filter_by(user_id=user_id).first()
    db.session.delete(one)
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
