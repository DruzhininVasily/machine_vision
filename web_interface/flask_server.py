from flask import Flask, render_template, request, session, redirect, abort
from flask_sock import Sock
import os
from plc_interaction import PlcClient
from admin_commands import ADMIN_SOCKET_COMMANDS, choice_setpoint, change_setpoint

plc = PlcClient('192.168.0.220', 0, 1)
print('подключено')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gdsacjhdascalkdjbakaldkh'
sock = Sock(app)


# Корневой запрос
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST" and request.form['username'] == 'user':
        session['userLogged'] = request.form['username']
        return redirect(session['userLogged'])
    elif request.method == "POST" and request.form['username'] == 'adфmin' and request.form['psw'] == '12345':
        session['userLogged'] = request.form['username']
        return redirect(session['userLogged'])
    return render_template('index.html')


@app.route("/user", methods=['GET', 'POST'])
def user():
    if 'userLogged' not in session or session['userLogged'] != 'user':
        abort(401)
    return render_template('user.html')


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if 'userLogged' not in session or session['userLogged'] != 'admin':
        abort(401)
    choice = choice_setpoint()
    return render_template('admin.html', select_list=choice[0], ind=choice[1])


@app.errorhandler(401)
def unauthorized(error):
    return render_template('error401.html')


# Вебсоккет для user
@sock.route('/show_photo')
def show_photo(sock):
    while True:
        new_message = sock.receive()
        if new_message == "Дай фото":
            sock.send("static/data/" + os.listdir("C:/PycharmProjects/Machine_vision/web_interface/static/data")[-1])
        elif new_message == "get submit":
            if plc.pallet_is_blocking is True:
                sock.send("request submit")
        elif new_message == "Подтверждено":
            plc.submit_button()


# Вебсоккет для admin
@sock.route('/control')
def control(sock):
    while True:
        new_message = sock.receive()
        try:
            change_setpoint(float(new_message))
        except ValueError:
            ADMIN_SOCKET_COMMANDS[new_message](sock, plc)


if __name__ == "__main__":
    app.run(host='192.168.0.57', port=5000, debug=False)
