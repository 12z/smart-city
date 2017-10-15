import random
import string

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean

engine = create_engine('sqlite:///the_db.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    login = Column(String)
    password = Column(String)

    def __repr__(self):
       return "<User(name='%s', fullname='%s', password='%s')>" % (
                            self.name, self.fullname, self.password)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user = Column(String)
    text = Column(String)


class Visitor(Base):
    __tablename__ = 'visitors'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Gate(Base):
    __tablename__ = 'gates'

    id = Column(Integer, primary_key=True)
    state = Column(String)


Base.metadata.create_all(engine)

gate = Gate(state="down")
tmp_session = Session()
tmp_session.add(gate)
tmp_session.commit()


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def authorize_user(login, password):
    session = Session()
    user = session.query(User).filter_by(login=login).first()
    if user.password == password:
        return user


def add_user(req):
    session = Session()

    password = id_generator()
    user = User(name=req['name'], login=req['login'], password=password)
    session.add(user)
    session.commit()
    return user


def get_messages():
    session = Session()
    messages = []
    got_messages = session.query(Message).all()

    for msg in got_messages:
        messages.append({'user': msg.user,
                         'text': msg.text, })

    return messages


def new_message(user, message):
    session = Session()
    message = Message(user=user, text=message)
    session.add(message)
    session.commit()


def get_user(user_id):
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    return user


def get_gate():
    session = Session()
    gate = session.query(Gate).first()
    return gate.state


def set_gate(action=None):
    session = Session()
    gate = session.query(Gate).first()

    if action is None:

        if gate.state == 'up':
            gate.state = 'down'
        elif gate.state == 'down':
            gate.state = 'up'

        session.commit()

    else:
        gate.state = action
        session.commit()

    return gate.state


def add_visitor(name):
    session = Session()

    visitor = Visitor(name=name)
    session.add(visitor)
    session.commit()


def get_visitors():
    session = Session()

    visitors = []

    got_visitors = session.query(Visitor).all()
    for vstr in got_visitors:
        visitors.append({'name': vstr.name})

    return visitors
