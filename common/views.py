from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests


# Create your views here.
def main(request):
    return render(request, 'common/main.html')


def login(request):
    return render(request, 'common/login.html')


def info(request):
    # 세션에서 정보 가져오기
    id = request.session.get('id')
    nickname = request.session.get('nickname')
    thumbnail_image = request.session.get('image')

    return render(request, 'common/info.html', {'id': id, 'nickname': nickname, 'thumbnail_image': thumbnail_image})


def getcode(request):
    code = request.GET.get('code')
    # REST API를 이용해 토큰 발급 받아옴 (카카오에게)
    requests.post('https://kauth.kakao.com/oauth/token')
    data = {'grant_type': "authorization_code",
            'client_id': 'aa4f2cb7ffd0e8ced07032bfa9361f57',
            'redirect_uri': 'http://127.0.0.1:8000/oauth/redirect',
            'code': code}
    headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    res = requests.post('https://kauth.kakao.com/oauth/token', data=data, headers=headers)
    token_json = res.json()
    print(token_json)

    # REST API를 이용해 토큰으로 정보를 조회
    access_token = token_json['access_token']

    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    res = requests.get("https://kapi.kakao.com//v2/user/me", headers=headers)
    profile_json = res.json()

    id = profile_json['id']  # ID 뽑아내기
    nickname = profile_json['properties']['nickname']  # 닉네임 뽑아내기
    image = profile_json['properties']['profile_image']  # 이미지 뽑아내기
    print(id)
    print(nickname)
    print(image)

    request.session['id'] = id
    request.session['nickname'] = nickname
    request.session['image'] = image

    return redirect('info')