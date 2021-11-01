# coding:utf-8
# 本文件存储公共方法
# 请按规则传入和接收
from Myapp.models import *
import re
import ast


# 替换全局变量
def project_datas_replace(project_id: str, s: str) -> str:
    # 根据项目变量去获得生效的变量组。
    try:
        project_data_ids = DB_project.objects.filter(id=project_id)[0].project_datas.split(',')
    except:
        return s

    if project_data_ids == ['']:
        return s

    project_datas = {}
    for i in project_data_ids:
        project_data = ast.literal_eval(list(DB_project_data.objects.filter(id=i).values())[0]['data'])
        project_datas.update(project_data)
    # 用正则找出所有需要替换的变量名称。
    # 处理url/header/data
    list_data = re.findall(r'~(.*?)~', s)
    for i in list_data:
        s = s.replace('~' + i + '~', str(project_datas[i]))

    # 返回结果。
    return s
