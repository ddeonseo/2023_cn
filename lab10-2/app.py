import json
from flask import Blueprint, Flask, render_template, request
import urllib
import requests
import ssl

context = ssl._create_unverified_context()

endpoint = 'https://mynginx12:443/pastebin/api'

app = Flask(__name__)
bp = Blueprint('mybp', __name__,
               static_folder='static',
               static_url_path='/pastebin/static',
               template_folder='templates',
               url_prefix='/pastebin')

@bp.route(f'/', methods=['GET'])
@bp.route(f'/index.html', methods=['GET'])
def get_index():
    count_users = 0
    url = f'{endpoint}/users/'
    with urllib.request.urlopen(url, context=context) as f:
        data = json.loads(f.read())
        count_users = len(data)

    count_pastes = 0
    url = f'{endpoint}/pastes/'
    with urllib.request.urlopen(url, context=context) as f:
        data = json.loads(f.read())
        count_pastes = len(data)

    return render_template('index.html', count_users=count_users, count_pastes=count_pastes)

@bp.route(f'/createuser', methods=['POST', 'GET'])
def post_create_user():
    if request.method == 'POST':
        url = f'{endpoint}/users/'
        data = {'username': request.form['username'],
                'password': request.form['password']}
        headers = {'Content-Type': 'application/json'}

        data_str = json.dumps(data).encode('utf-8')

        req = urllib.request.Request(url=url,
                                     data=data_str,
                                     headers=headers,
                                     method='POST')
        with urllib.request.urlopen(req, context=context) as f:
            pass

    return render_template('createuser.html')


@bp.route(f'/createpaste', methods=['POST','GET'])
def post_create_paste():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url = f'{endpoint}/users/{username}/create_paste?password={password}'
        data = {'title': request.form['title'],
                'content': request.form['content']}
        headers = {'Content-Type': 'application/json'}
        data_str = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url=url,
                                     data=data_str,
                                     headers=headers,
                                     method='POST')
        with urllib.request.urlopen(req, context=context) as f:
            pass
        
    return render_template('createpaste.html')
# def post_create_paste():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         url = f'{endpoint}/users/{username}/create_paste/?password={password}'
#         data = {'title': request.form['title'],
#                 'content': request.form['content']}
#         json_data = json.dumps({'title': request.form['title'],'content': request.form['content']})
#         requests.post(url, data=json_data)  
#     return render_template('createpaste.html')
@bp.route(f'/users/<name>/pastes', methods=['GET'])
def get_users(name=None):
    url = f'{endpoint}/users/{name}/pastes'
    data = None
    # json_data = json.dumps(data)
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, context=context) as f:
        data = json.loads(f.read())
        count_pastes = len(data)
    return render_template('users.html', countpastes=count_pastes,pastes=data, name=name)


app.register_blueprint(bp)
