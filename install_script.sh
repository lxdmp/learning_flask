#! /bin/bash
# 若更新不成功,改源
flask/bin/pip install flask
flask/bin/pip install flask-login
flask/bin/pip install flask-openid
flask/bin/pip install flask-mail
flask/bin/pip install flask-sqlalchemy
flask/bin/pip install sqlalchemy-migrate
flask/bin/pip install flask-whooshalchemy
flask/bin/pip install flask-wtf
flask/bin/pip install flask-babel
flask/bin/pip install guess_language
flask/bin/pip install flipflop
flask/bin/pip install coverage
flask/bin/pip install flask-mysql
flask/bin/pip install flask-bootstrap
flask/bin/pip install flask-moment
flask/bin/pip install flask-socketio
flask/bin/pip install gevent # socketio需要
flask/bin/pip install gevent-websocket # socketio需要
flask/bin/pip install flask-apscheduler
flask/bin/pip install futures # in 2.7, no module futures, apscheduelr需要
flask/bin/pip install funcsigs # apscheduler需要
