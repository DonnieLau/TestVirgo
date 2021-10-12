from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Myapp.models import *
import json
import requests


# 获取公共参数
def glodict(reuqest):
    userimg = str(reuqest.user.id) + '.png'
    res = {"username": reuqest.user.username, "userimg": userimg}
    return res


# 正交工具页面
def zhengjiao(request):
    return render(request, 'welcome.html',
                  {"whichHTML": "zhengjiao.html", "oid": request.user.id, **glodict(request)})
