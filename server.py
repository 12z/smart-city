from flask import Flask, request, jsonify, render_template
import db_connector
import random


app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    request_json = request.get_json()

    new_user = db_connector.User(
        name=request_json['name'],
        login=request_json['login'],
    )

    user = db_connector.add_user(request_json)

    reply = {
        'id': user.id,
        'password': user.password,
    }

    return jsonify(reply)


@app.route('/authorize', methods=['POST'])
def authorize():
    request_json = request.get_json()
    login = request_json['login']
    password = request_json['password']
    user = db_connector.authorize_user(login, password)

    print(user)
    print(user.login)
    return 'ok'


@app.route('/admin')
def admin():
    messages = db_connector.get_messages()
    visitors_list = db_connector.get_visitors()

    return render_template('admin.html',
                           messages=messages,
                           visitors=visitors_list,
                           )


@app.route('/message', methods=['POST'])
def message():
    request_json = request.get_json()
    db_connector.new_message(request_json['user'], request_json['message'])

    return ''


@app.route('/set_gate', methods=['POST'])
def set_gate():

    if request.data:
        request_json = request.get_json()
        action = request_json['action']
        db_connector.set_gate(action)

        return jsonify(request_json)

    else:

        state = db_connector.set_gate()
        return jsonify({
            'action': state,
        })


@app.route('/gate')
def gate():
    return render_template('gate.html')


@app.route('/get_gate')
def get_gate():
    state = db_connector.get_gate()

    links = {
        'down': 'http://sommer-nw.ru/wp-content/uploads/2012/11/ASB_6010.jpg',
        'up': 'http://www.videomodul.ru/uploads/cache/478/300x300-00000000467.jpg',
    }

    return jsonify({'link': links[state]})


@app.route('/add_visitor', methods=['POST'])
def add_visitor():
    request_json = request.get_json()

    db_connector.add_visitor(request_json['name'])

    return ''


@app.route('/visitors')
def visitors():
    visitors_list = db_connector.get_visitors()

    return render_template('visitors.html',
                           visitors=visitors_list)


@app.route('/counters')
def counters():

    one = random.randint(0, 100)
    two = random.randint(0, 100)
    water_pressure = random.randint(397, 403)/100
    gas_measurement = random.randint(490, 510)/10000

    return jsonify({
        'temperature': random.randint(200, 230)/10,
        'water': water_pressure,
        'gas': gas_measurement,
        'electricity': random.randint(500, 2500),
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
