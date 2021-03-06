#!venv/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

users = [
    {
        'login': 'varya',
        'password': 'varya',
        'likes': 2,
        'comments': 3
    },
    {
        'login': 'admin',
        'password': 'admin',
        'likes': 4,
        'comments': 1
    }
]

notices = [
    {
        'id': 1,
        'title': 'Prodam garazh',
        'author': 'varya',
        'likes': [
            {
                'author': 'varya',
                'time': 1530321686
            },
            {
                'author': 'varya',
                'time': 1530321694
            },
            {
                'author': 'varya',
                'time': 1530321613
            },
            {
                'author': 'varya',
                'time': 1530321655
            },
        ],
        'date': 'Sat Jun 30 01:21:26 2018',
        'comments': [
            {
                'author': 'admin',
                'comment': 'how much?',
                'time': 1530321686
            },
            {
                'author': 'aleksey',
                'comment': 'ya pokupayu',
                'time': 1530322346
            },
            {
                'author': 'varya',
                'comment': 'privet vsem',
                'time': 1530322350
            },
            {
                'author': 'varya',
                'comment': 'xochy morozhenko',
                'time': 1530322360
            },
            {
                'author': 'varya',
                'comment': 'kto pokupaet?',
                'time': 1530322370
            }
        ]
    },
    {
        'id': 2,
        'title': 'Xorowii mobilnii Motorola, 200grn',
        'author': 'admin',
        'likes': [],
        'date': 'Sun Jun 24 11:51:11 2018',
        'comments': []
    }
]


@app.route('/notice_board/api/v1.0/signup',
           methods=['POST'])
def singup():
    if 'login' not in request.json \
            or len(request.json['login']) > 20:
        abort(422, 'Invalid login')

    if 'password' not in request.json \
            or 'confirm_password' not in request.json \
            or len(request.json['password']) > 20 \
            or request.json['password'] != request.json['confirm_password']:
        abort(422, 'Invalid password')

    users.append({'login': request.json['login'],
                  'password': request.json['confirm_password']})

    return jsonify({'message': "SignUp Successful"})


@app.errorhandler(422)
def not_found(error):
    return make_response(jsonify([{'error': 'Unprocessable Entity'},
                                  {'message': error.description}]), 422)


@auth.get_password
def get_password(username):
    for user in users:
        if username == user['login']:
            return user['password']
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.route('/notice_board/api/v1.0/notices', methods=['GET'])
@auth.login_required
def get_notices():
    return jsonify({'notices': [make_public_notice(notice) for notice in notices]})


def make_public_notice(notice):
    new_notice = {}
    for field in notice:
        if field == 'id':
            new_notice['uri'] = url_for('get_notice', notice_id=notice['id'], _external=True)
        else:
            new_notice[field] = notice[field]
    return new_notice


@app.route('/notice_board/api/v1.0/notices/<int:notice_id>', methods=['GET'])
@auth.login_required
def get_notice(notice_id):
    notice = [notice
              for notice in notices
              if notice['id'] == notice_id]
    if len(notice) == 0:
        abort(404)
    return jsonify({'notice': [make_public_notice(notice[0])]})


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/notice_board/api/v1.0/add_notice',
           methods=['POST'])
@auth.login_required
def add_notice():
    if 'title' not in request.json \
            or len(request.json['title']) > 50:
        abort(422, 'Invalid title')

    if 'author' not in request.json \
            or len(request.json['author']) > 20:
        abort(422, 'Invalid author')

    format_str = "%a %b %d %H:%M:%S %Y"
    date_time = datetime.datetime.today().strftime(format_str)

    notice = {
        'id': notices[-1]['id'] + 1,
        'title': request.json['title'],
        'author': request.json['author'],
        'likes': [],
        'comments': [],
        'date': date_time
    }
    notices.append(notice)

    return jsonify({'notice': [make_public_notice(notice)]}, 201)


@app.route('/notice_board/api/v1.0/notices/<int:notice_id>/add_comment',
           methods=['POST'])
@auth.login_required
def add_coment(notice_id):
    if 'comment' not in request.json \
            or len(request.json['comment']) > 255:
        abort(422, 'Invalid comment')

    times = []
    author = auth.username()
    for notice in notices:
        for comment in notice['comments']:
            if comment['author'] == author:
                times.append(comment['time'])
    times.sort()

    if len(times) > 4 and (int(datetime.datetime.now().timestamp()) - times[-5] < 3600):
        abort(422, 'Too hot')

    for notice in notices:
        if notice['id'] == notice_id:
            notice['comments'].append({
                'author': author,
                'comment': request.json['comment'],
                'time': int(datetime.datetime.now().timestamp())
            })
            return jsonify({'notice': [make_public_notice(notice)]}, 201)
    return abort(404)


@app.route('/notice_board/api/v1.0/notices/<int:notice_id>/like',
           methods=['POST'])
@auth.login_required
def like(notice_id):
    times = []
    author = auth.username()
    for notice in notices:
        for comment in notice['likes']:
            if comment['author'] == author:
                times.append(comment['time'])
    times.sort()

    if len(times) > 4 and (int(datetime.datetime.now().timestamp()) - times[-5] < 3600):
        abort(422, 'Too hot')

    for notice in notices:
        if notice['id'] == notice_id:
            notice['likes'].append({
                'author': author,
                'time': int(datetime.datetime.now().timestamp())
            })
            return jsonify({'notice': [make_public_notice(notice)]}, 201)
    return abort(404)


if __name__ == '__main__':
    app.run(debug=True)
