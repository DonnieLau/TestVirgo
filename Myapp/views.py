from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Myapp.models import *
import json
import requests


# Create your views here.

# 获取公共参数
def glodict(reuqest):
    userimg = str(reuqest.user.id) + '.png'
    res = {"username": reuqest.user.username, "userimg": userimg}
    return res


# 上传用户头像
@csrf_exempt
def user_upload(request):
    file = request.FILES.get("fileUpload", None)  # 靠name获取上传的文件，如果没有，避免报错，设置成None

    if not file:
        return HttpResponseRedirect('/home/')  # 如果没有则返回到首页

    new_name = str(request.user.id) + '.png'  # 设置好这个新图片的名字
    print(new_name)
    destination = open("Myapp/static/user_img/" + new_name, 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    return HttpResponseRedirect('/home/')  # 返回到首页


# 进入主页
@login_required
def home(request, log_id=''):
    return render(request, 'welcome.html',
                  {"whichHTML": "home_2.html", "oid": request.user.id, "ooid": log_id, **glodict(request)})


# 进入用例页
@login_required
def caselist(request):
    return render(request, 'caselist.html')


# 返回子页面
def child(request, eid, oid, ooid):
    res = child_jason(eid, oid, ooid)
    return render(request, eid, res)


# 数据分发器：控制不同的页面返回不同的数据
def child_jason(eid, oid='', ooid=''):
    res = {}
    if eid == 'home_2.html':
        homerefs = DB_home_href.objects.all()
        projects = DB_project.objects.all()
        homelogs = DB_apis_log.objects.filter(user_id=oid)[::-1]
        if ooid == '':
            res = {"hrefs": homerefs, "projects": projects, "homeloges": homelogs}
        else:
            log = DB_apis_log.objects.filter(id=ooid)[0]
            res = {"hrefs": homerefs, "homeloges": homelogs, "log": log}
    if eid == 'project_list.html':
        projects = DB_project.objects.all()
        res = {"projects": projects}
    if eid == "P_apis.html" or eid == "P_cases.html" or eid == "P_project_set.html":
        project = DB_project.objects.filter(id=oid)[0]
        res = {"project": project}
    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)
        res = {"project": project, "apis": apis}
    if eid == 'P_cases.html':  # 去数据库拿本项目的所有大用例
        project = DB_project.objects.filter(id=oid)[0]
        cases = DB_cases.objects.filter(project_id=oid)
        apis = DB_apis.objects.filter(project_id=oid)
        res = {"project": project, "cases": cases, "apis": apis}

    return res


# 返回登陆页面
def login(request):
    return render(request, 'login.html')


# 开始注册
def register_action(request):
    u_name = request.GET['username']
    u_word = request.GET['password']
    # 开始联通数据库，检验用户和密码
    from django.contrib.auth.models import User
    try:
        user = User.objects.create_user(username=u_name, password=u_word)
        user.save()
        return HttpResponse('注册成功！')
    except:
        return HttpResponse('注册失败！用户名已存在！')


# 开始登陆
def login_action(request):
    u_name = request.GET['username']
    u_word = request.GET['password']
    # 开始联通数据库，检验用户和密码
    user = auth.authenticate(username=u_name, password=u_word)
    if user is not None:
        auth.login(request, user)
        request.session['user'] = u_name
        return HttpResponse('登陆成功')
    else:
        return HttpResponse('登陆失败')


# 退出登陆
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


# 吐槽
def pei(request):
    tucao_text = request.GET['tucao_text']
    DB_tucao.objects.create(user=request.user.username, text=tucao_text)
    return HttpResponse('')


# 帮助文档
def help_action(request):
    return render(request, 'welcome.html', {"whichHTML": "help.html", "oid": "", **glodict(request)})


# 项目列表
def project_action(request):
    return render(request, 'welcome.html', {"whichHTML": "project_list.html", "oid": "", **glodict(request)})


# 删除项目
def project_delete(request):
    id = request.GET['id']
    DB_project.objects.filter(id=id).delete()
    DB_apis.objects.filter(project_id=id).delete()  # 删除项目中接口
    all_case = DB_cases.objects.filter(project_id=id)
    for i in all_case:
        DB_step.objects.filter(case_id=i.id).delete()  # 删除用例中的步骤
        i.delete()  # 删除项目中的用例
    return HttpResponse('')


# 新增项目
def project_add(request):
    project_name = request.GET['project_name']
    DB_project.objects.create(name=project_name, remark="", user=request.user.username, other_user="")
    return HttpResponse('')


# 进入接口库
@login_required
def open_apis(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_apis.html", "oid": project_id, **glodict(request)})


# 进入用例库
@login_required
def open_cases(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_cases.html", "oid": project_id, **glodict(request)})


# 进入项目设置
@login_required
def open_project_set(request, id):
    project_id = id
    return render(request, 'welcome.html', {"whichHTML": "P_project_set.html", "oid": project_id, **glodict(request)})


# 保存项目设置
def save_project_set(request, id):
    project_id = id
    porject_name = request.GET['name']
    porject_remark = request.GET['remark']
    porject_other_user = request.GET['other_user']
    DB_project.objects.filter(id=project_id).update(name=porject_name, remark=porject_remark,
                                                    other_user=porject_other_user)
    return HttpResponse('呜啦啦')


# 新增接口
def project_api_add(request, Pid):
    project_id = Pid
    DB_apis.objects.create(project_id=project_id, api_method='none')
    return HttpResponseRedirect('/apis/%s' % project_id)


# 删除接口
def project_api_delete(request, id):
    project_id = DB_apis.objects.filter(id=id)[0].project_id
    DB_apis.objects.filter(id=id).delete()
    return HttpResponseRedirect('/apis/%s' % project_id)


# 保存接口备注
def save_bz(request):
    api_id = request.GET['api_id']
    bz_value = request.GET['bz_value']
    DB_apis.objects.filter(id=api_id).update(des=bz_value)
    return HttpResponse('')


# 获取接口备注
def get_bz(request):
    api_id = request.GET['api_id']
    bz_value = DB_apis.objects.filter(id=api_id)[0].des
    return HttpResponse(bz_value)


# 保存接口信息
def api_save(request):
    # 获得所有接口信息
    api_id = request.GET['api_id']
    api_name = request.GET['api_name']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    # 返回体子页面时点击保存
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
        if ts_body_method in ['', None]:
            return HttpResponse('faild')
    else:
        ts_api_body = request.GET['ts_api_body']
        api = DB_apis.objects.filter(id=api_id)
        api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)
    # 保存数据
    DB_apis.objects.filter(id=api_id).update(
        name=api_name,
        api_method=ts_method,
        api_url=ts_url,
        api_host=ts_host,
        api_header=ts_header,
        body_method=ts_body_method,
        api_body=ts_api_body
    )
    return HttpResponse('success')


# 获取接口数据
def get_api_data(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    # json格式返回前端
    return HttpResponse(json.dumps(api), content_type='applicatin/json')


# 调试层发送请求
def api_send(request):
    # 获得所有接口信息
    api_id = request.GET['api_id']
    api_name = request.GET['api_name']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    # 返回体子页面时点击send
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
        if ts_body_method in ['', None]:
            return HttpResponse('请先选择好请求体编码格式和请求体，再点击Send按钮发送请求！')
    else:
        ts_api_body = request.GET['ts_api_body']
        api = DB_apis.objects.filter(id=api_id)
        api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)

    # 发送send请求获取返回值
    # 处理header
    try:
        header = json.loads(ts_header)
    except:
        return HttpResponse('请求头不符合json格式！')
    # 处理host+url
    if ts_host[-1] == '/' and ts_url[0] == '/':
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':
        url = ts_host + '/' + ts_url
    else:
        url = ts_host + ts_url
    # 处理method
    if ts_body_method == 'none':
        response = requests.request(ts_method.upper(), url, headers=header, data={})
    elif ts_body_method == 'form-data':
        files = []
        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)
    elif ts_body_method == 'x-www-form-urlencoded':
        header['Content-Type'] = 'application/x-www-form-urlencoded'
        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        response = requests.request(ts_method.upper(), url, headers=header, data=payload)
    else:
        if ts_body_method == 'Text':
            header['Content-Type'] = 'text/plain'
        elif ts_body_method == 'JavaScript':
            header['Content-Type'] = 'text/plain'
        elif ts_body_method == 'Json':
            header['Content-Type'] = 'text/plain'
        elif ts_body_method == 'Html':
            header['Content-Type'] = 'text/plain'
        elif ts_body_method == 'Xml':
            header['Content-Type'] = 'text/plain'
        response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))
    # 返回值返回给前端
    response.encoding = 'utf-8'
    return HttpResponse(response.text)


# 接口复制
def api_copy(request):
    api_id = request.GET['api_id']
    old_api = DB_apis.objects.filter(id=api_id)[0]
    DB_apis.objects.create(project_id=old_api.project_id,
                           name=old_api.name + '_副本',
                           api_method=old_api.api_method,
                           api_url=old_api.api_url,
                           api_header=old_api.api_header,
                           api_login=old_api.api_login,
                           api_host=old_api.api_host,
                           des=old_api.des,
                           body_method=old_api.body_method,
                           api_body=old_api.api_body,
                           result=old_api.result,
                           sign=old_api.sign,
                           file_key=old_api.file_key,
                           file_name=old_api.file_name,
                           public_header=old_api.public_header,
                           last_body_method=old_api.last_body_method,
                           last_api_body=old_api.last_api_body
                           )
    return HttpResponse('')


# 异常测试发送请求
def error_request(request):
    api_id = request.GET['api_id']
    new_body = request.GET['new_body']
    span_text = request.GET['span_text']
    api = DB_apis.objects.filter(id=api_id)[0]
    method = api.api_method
    url = api.api_url
    host = api.api_host
    header = api.api_header
    body_method = api.body_method
    try:
        header = json.loads(header)
    except:
        return HttpResponse('请求头不符合json格式！')

    if host[-1] == '/' and url[0] == '/':
        url = host[:-1] + url
    elif host[-1] != '/' and url[0] != '/':
        url = host + '/' + url
    else:
        url = host + url

    try:
        if body_method == 'none':
            response = requests.request(method.upper(), url, headers=header, data={})
        elif body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload, files=files)
        elif body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload)
        elif body_method == 'Json':
            header['Content-Type'] = 'text/plain'
            response = requests.request(method.upper(), url, headers=header, data=new_body.encode('utf-8'))
        else:
            return HttpResponse('非法的请求体类型')
        # 返回值返回给前端
        response.encoding = 'utf-8'
        res_json = {"response": response, "span_text": span_text}
        return HttpResponse(json.dumps(res_json), content_type='application/json')
    except:
        res_json = {"response": '接口未通!', "span_text": span_text}
        return HttpResponse(json.dumps(res_json), content_type='application/json')


# 首页发送send请求
def api_send_home(request):
    # 提取所有数据
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    ts_api_body = request.GET['ts_api_body']
    # 发送请求获取返回值
    try:
        header = json.loads(ts_header)
    except:
        return HttpResponse('请求头不符合json格式！')

    # 将请求数据写入数据库请求记录中
    DB_apis_log.objects.create(user_id=request.user.id,
                               api_method=ts_method,
                               api_url=ts_url,
                               api_header=ts_header,
                               api_host=ts_host,
                               body_method=ts_body_method,
                               api_body=ts_api_body)

    if ts_host[-1] == '/' and ts_url[0] == '/':
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':
        url = ts_host + '/' + ts_url
    else:
        url = ts_host + ts_url

    try:
        if ts_body_method == 'none':
            response = requests.request(ts_method.upper(), url, headers=header, data={})

        elif ts_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)

        elif ts_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload)

        else:  # 这时肯定是raw的五个子选项：
            if ts_body_method == 'Text':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Json':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Html':
                header['Content-Type'] = 'text/plain'

            if ts_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))

        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))


# 首页获取最新的请求记录
def get_home_log(request):
    user_id = request.user.id
    all_logs = DB_apis_log.objects.filter(user_id=user_id)
    ret = {"all_logs": list(all_logs.values("id", "api_method", "api_url", "api_host"))[::-1]}
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 首页获取完整的单一请求记录
def get_api_log_home(request):
    log_id = request.GET['log_id']
    log = DB_apis_log.objects.filter(id=log_id)
    ret = {"log": list(log.values())[0]}
    print(ret)
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 用例库新增用例
def add_case(request, eid):
    DB_cases.objects.create(project_id=eid, name='')
    return HttpResponseRedirect('/cases/%s/' % eid)


# 用例库删除用例
def del_case(request, eid, oid):
    DB_cases.objects.filter(id=oid).delete()
    DB_step.objects.filter(case_id=oid).delete()
    return HttpResponseRedirect('/cases/%s/' % eid)


# 用例库复制用例
def copy_case(request, eid, oid):
    old_case = DB_cases.objects.filter(id=oid)[0]
    DB_cases.objects.create(project_id=old_case.project_id, name=old_case.name + '_副本')
    return HttpResponseRedirect('/cases/%s/' % eid)


# 获取小用例步骤的列表数据
def get_small(request):
    case_id = request.GET['case_id']
    steps = DB_step.objects.filter(case_id=case_id).order_by('index')
    ret = {"all_steps": list(steps.values("id", "name", "index"))}
    return HttpResponse(json.dumps(ret), content_type='application/json')


# 新增小用例
def add_new_step(request):
    case_id = request.GET['case_id']
    step_len = len(DB_step.objects.filter(case_id=case_id))
    DB_step.objects.create(case_id=case_id, name='新步骤', index=step_len + 1)
    return HttpResponse('')


# 删除小用例
def delete_step(request, eid):
    step = DB_step.objects.filter(id=eid)[0]
    index = step.index
    case_id = step.case_id
    step.delete()
    for i in DB_step.objects.filter(case_id=case_id).filter(index__gt=index):
        i.index -= 1
        i.save()
    return HttpResponse('')


# 获取小步骤
def get_step(request):
    step_id = request.GET['step_id']
    step = DB_step.objects.filter(id=step_id)
    stepList = list(step.values())[0]
    return HttpResponse(json.dumps(stepList), content_type='application/json')