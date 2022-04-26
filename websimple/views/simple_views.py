# -- coding: utf-8 --

from flask import Flask, Blueprint, render_template, redirect, request
import json
from datetime import datetime
# 블루프린트 객체 생성, 현재 파일은 app.py에 모듈로 추가되어 사용됨.
bp = Blueprint('simple_views', __name__, url_prefix='/')

# $$$$$$$$$$$$$데이터를 보존하기 위해 json 파일로 읽고 쓰는 부분$$$$$$
data_list = []  # 실행하면 json 파일에서 기존 데이터를 가져와 리스트에 넣음.
json_file = "static/data/data.json"
try:
    with open(json_file, "r") as f:
        data_json = json.load(f)
        data_list = data_json["users"]
except:
    print('빈파일입니다.')


def dumptoJson():  # json파일에 수시로 업데이트 저장하는 함수 호출
    data_dic = {"data": data_list}
    with open(json_file, "w") as f:
        json.dump(data_dic, f, indent=4)
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
############ 여기서 부터가 CRUDE를  처리하는 부분 #######################
############ 데이터를 생성하는 부분 ###############


@bp.route('/simplecreate', methods=['GET', 'POST'])  # 입력하는 부분
def simplecreate():
    if request.method == 'POST':  # 폼의 데이터를 가지고 post방식으로 들어옴.
        id = datetime.now().strftime("%y%m%d%H%M%S")  # 시간을 고유id값으로 사용
        name = request.form['name']
        url = request.form['url']   # 태그의 name속성의 값을 사용함.
        content = request.form['content']
        temp = {"id": id, "name": name, "url": url,
                "content": content}  # 딕셔녀리형식{키:값}
        data_list.append(temp)  # 딕셔너리를 리스트 항목으로 추가 [{키:값},{키,값}]
        dumptoJson()  # json파일에 저장 업데이트하는 함수 호출
        return redirect('/simplelist')  # 다른 주소로 이동하는 리디렉션
    else:  # get방식으로 들어오면 입력화면을 보여줌
        return render_template('simple_create.html')

############ 목록을 보여주는 부분  #############


@bp.route('/simplelist')
def simplelist():  # 리스트 전달만함
    return render_template('simple_list.html', datatojson=data_list)

############ 각 항목의 세부내용을 보여주는 부분 ######


@ bp.route('/simpleread/<id>')
def simpleread(id):
    selected = None
    for data in data_list:  # user_list에 있는 항목을 하나씩 user에 저장하며 반복
        if id == data['id']:  # id가 같으면 현재항목을 selected에 저장
            selected = data
            break    # 해당 항목 찾으면 더이상 반복할 필요없으므로 반복문을 빠져 나옴
    return render_template('simple_read.html', selected=selected)

############업데이트 , 삭제와 입력의 조합 ##############


@bp.route('/simpleupdate/<id>', methods=['GET', 'POST'])
def simpleupdate(id):
    selected = None
    idx = None
    for data in data_list:  # user_list에 있는 항목을 하나씩 user에 저장하며 반복
        if id == data['id']:
            selected = data  # 아이디와 일치하는 항목을 selected에 담아 전송
            idx = data_list.index(data)  # 해당리스트 항목의 인덱스 번호 확인
            break
    if request.method == 'POST':  # post 방식으로 왔을때만 수정
        data_list[idx]['name'] = request.form['name']
        data_list[idx]['url'] = request.form['url']
        data_list[idx]['content'] = request.form['content']
        dumptoJson()  # json파일에 저장 업데이트하는 함수 호출
        return redirect('/simplelist')
    else:  # get방식으로 들어오면 페이지로 연결과 내용 보여줌
        return render_template('simple_update.html', selected=selected)

############삭제, 주소로 접근해서 못지우게 POST방식으로만 처리 #########


@bp.route('/simpledelete/<id>', methods=['POST'])
def simpledelete(id):
    if request.method == 'POST':
        for data in data_list:  # user는 딕션너리형식
            if id == data['id']:
                data_list.remove(data)  # 리스트의 항목을 삭제함
                break
        dumptoJson()
    return redirect('/simplelist')
