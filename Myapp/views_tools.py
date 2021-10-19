from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Myapp.models import *
from allpairspy import AllPairs
from xlutils import copy
import os
import json
import requests
import xlrd
import xlwt


# 获取公共参数
def glodict(reuqest):
    userimg = str(reuqest.user.id) + '.png'
    res = {"username": reuqest.user.username, "userimg": userimg}
    return res


# 正交工具页面
def zhengjiao(request):
    return render(request, 'welcome.html',
                  {"whichHTML": "zhengjiao.html", "oid": request.user.id, **glodict(request)})


# 正交工具运行
def zhengjiao_play(request):
    end_values = request.GET['end_values'].split(',')
    new_values = [i.split('/') for i in end_values]
    res = []
    for j in AllPairs(new_values):
        res.append(j)
    d = {"res": res}
    return HttpResponse(json.dumps(d), content_type="application/json")


# 正交工具导出
def zhengjiao_excel(request):
    end_keys = request.GET['end_keys'].split(',')
    end_values = request.GET['end_values'].split(',')
    new_values = [i.split('/') for i in end_values]
    res = []
    for j in AllPairs(new_values):
        res.append(j)

    wqrf_book = xlwt.Workbook(encoding='utf-8')
    wqrf_sheet = wqrf_book.add_sheet('正交结果')
    for i in range(len(res)):
        case_index = '用例：' + str(i + 1)
        hb = list(zip(end_keys, res[i]))
        case = ','.join([':'.join(list(i)) for i in hb])
        wqrf_sheet.write(i, 0, case_index)
        wqrf_sheet.write(i, 1, case)
    wqrf_book.save('Myapp/static/tmp_zhengjiao.xls')
    return HttpResponse('')
