"""PostTestDir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from Myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),  # 进入主页
    re_path(r'user_upload/$', user_upload),  # 上传头像
    re_path(r"^child/(?P<eid>.+)/(?P<oid>.*)/(?P<ooid>.*)/$", child),  # 返回子页面
    path('login/', login),  # 进入登陆界面
    path('accounts/login/', login),  # 非登陆状态自动跳转登陆页面
    path('logout/', logout),  # 退出登陆
    path('register_action/', register_action),  # 注册行为
    path('login_action/', login_action),  # 登陆行为
    path('pei/', pei),  # 专业吐槽
    path('help/', help_action),  # 进入到帮助文档
    path('project_list/', project_action),  # 进入到项目列表
    path('project_delete/', project_delete),  # 删除项目
    path('project_add/', project_add),  # 新增项目
    re_path(r'apis/(?P<id>.*)/$', open_apis),  # 进入接口库
    re_path(r'cases/(?P<id>.*)/$', open_cases),  # 进入用例库

    re_path(r'project_set/(?P<id>.*)/$', open_project_set),  # 进入项目设置
    re_path(r'project_set_save/(?P<id>.*)/$', save_project_set),  # 保存项目设置
    re_path(r'project_api_add/(?P<Pid>.*)/$', project_api_add),  # 新增接口
    re_path(r'project_api_del/(?P<id>.*)/$', project_api_delete),  # 删除接口

    path('save_bz/', save_bz),  # 保存接口备注
    path('get_bz/', get_bz),  # 获取接口备注
    path('api_save/', api_save),  # 保存接口信息
    path('get_api_data/', get_api_data),  # 获取接口数据
    path('api_send/', api_send),  # 调试层发送send请求
    path('api_copy/', api_copy),  # 复制接口
    path('error_request/', error_request),  # 异常测试

    path('api_send_home/', api_send_home),  # 首页发送send请求
    path('get_home_log/', get_home_log),  # 获取最新的请求记录
    path('get_api_log_home/', get_api_log_home),  # 首页获取完整的单一请求记录

    re_path(r'home_log/(?P<log_id>.*)/$', home),  # 再次进入首页，这次带着请求记录

    re_path(r'add_case/(?P<eid>.*)/$', add_case),  # 用例库新增用例
    re_path(r'del_case/(?P<eid>.*)/(?P<oid>.*)/$', del_case),  # 用例库删除用例
    re_path(r'copy_case/(?P<eid>.*)/(?P<oid>.*)/$', copy_case),  # 用例库复制用例
    re_path(r'get_small/$', get_small),  # 获取小用例步骤的列表数据
    re_path(r'add_new_step/$', add_new_step),  # 新增小用例
    re_path(r'delete_step/(?P<eid>.*)/$', delete_step),  # 删除小用例
    re_path(r'get_step/$', get_step),  # 获取小步骤
    re_path(r'save_step/$', save_step),  # 保存小步骤

    re_path(r'step_get_api/$', step_get_api),  # 步骤详情页面获取接口数据
    re_path(r'run_case/$', run_case),  # 运行大用例
    re_path(r'look_report/(?P<eid>.*)/$', look_report),  # 查看大用例报告
]
