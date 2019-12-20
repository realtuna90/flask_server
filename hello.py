from flask import Flask, escape, request, render_template
import random
import requests
import json

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/myname')
def myname():
    return '권민수다'

# 랜덤으로 점심메뉴를 추천
@app.route('/lunch')
def lunch():
    menus = ['양자강','김밥까페','20층','순남시래기']
    lunch = random.choice(menus)
    return lunch

# 아이돌 백과사전
@app.route('/idol')
def idol():
    idols = {
        'BTS':{
            '지민':25,
            '랩몬스터':23
        },
        'RV':'레드벨벳',
        '핑클':{
            '이효리':'거꾸로해도 이효리',
            '옥주현':'35'
        },
        'SES':['유진','바다','슈']
    }
    return idols

# 동적 라우팅 : 라우트 주소를 동적으로 부여
@app.route('/post/<int:num>')
def post(num):
    posts = ['0번 포스트','1번 포스트','2번 포스트','3번 포스트']
    return posts[num]

# 실습
# 1 -> 1
# 2 -> 8
# 3 -> 27
# str : 문자열로 바꿔주는 함수
@app.route('/cube/<int:num>')
def cube(num):
    result = num ** 3
    return str(result)

# 클라이언트에게 html 파일을 주고싶다
@app.route('/html')
def html():
    return render_template('hello.html')

@app.route('/ping')
def ping():
    return render_template('ping.html')

@app.route('/pong')
def pong():
    age = request.args.get('age')
    # age = request.args['age']
    return render_template('pong.html',age_in_html=age)

# 로또번호를 가져와서 보여주는 서버
# API (application programming interface) : 프로그램과 프로그램간의 접면(상호작용)
@app.route('/lotto_result/<int:round>')
def lotto_result(round):
    url = f'https://www.nlotto.co.kr/common.do?method=getLottoNumber&drwNo={round}'
    result = requests.get(url).json()

    winner = []
    for i in range(1,7):
        winner.append(result.get(f'drwtNo{i}')) # 키값이 잘못돼도 null값을 전달해 에러가 나지 않는다
        # winner.append(result[f'drwtNo{i}']) -> 키값이 잘못됐을 때 서버에러가 난다
    winner.append(result.get('bnusNo'))
    return json.dumps(winner)

app.run(debug=True)