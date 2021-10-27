import unittest, time, re, json, requests
from Myapp.HTMLRunner import HTMLTestRunner
import sys, os, django

path = "../TestVirgo"
sys.path.append(path)
os.environ.setdefault("DJNGO_SETTINGS_MODULE", "TestVirgo.settings")
django.setup()
from Myapp.models import *


class Test(unittest.TestCase):
    def demo(self, step):
        # 获取所有请求的资源
        api_method = step.api_method
        api_url = step.api_url
        api_host = step.api_host
        api_header = step.api_header
        api_body_method = step.api_body_method
        api_body = step.api_body
        get_path = step.get_path
        get_zz = step.get_zz
        assert_zz = step.assert_zz
        assert_qz = step.assert_qz
        assert_path = step.assert_path
        mock_res = step.mock_res
        if api_header == '':
            api_header = '{}'
        try:
            ts_project_headers = step.public_header.split(',')
        except:
            ts_project_headers = step.public_header

        if mock_res not in ['', None, 'None']:
            res = mock_res
        else:
            # 检查是否需要进行替换占位符
            rlist_url = re.findall(r"##(.+?)##", api_url)
            for i in rlist_url:
                api_url = api_url.replace("##" + i + "##", str(eval(i)))

            rlist_header = re.findall(r"##(.+?)##", api_header)
            for i in rlist_header:
                api_header = api_header.replace("##" + i + "##", repr(str(eval(i))))

            if api_body_method == 'none':
                pass
            elif api_body_method == 'Json':
                rlist_body = re.findall(r"##(.+?)##", api_body)
                for i in rlist_body:
                    api_body = api_body.replace("##" + i + "##", repr(str(eval(i))))
            else:
                rlist_body = re.findall(r"##(.+?)##", api_body)
                for i in rlist_body:
                    api_body = api_body.replace("##" + i + "##", str(eval(i)))

            # 处理header
            try:
                header = json.loads(api_header)  # 处理header
            except:
                header = eval(api_header)

            # 公共请求头
            for i in ts_project_headers:
                if i == '':
                    continue
                project_header = DB_project_header.objects.filter(id=i)[0]
                header[project_header.key] = project_header.value

            # 输出请求
            print('\n【method】：', api_method)
            print('【host】：', api_host)
            print('【url】：', api_url)
            print('【header】：', header)
            print('【body_method】：', api_body_method)
            print('【body】：', api_body)

            # 拼接完整url
            if api_host[-1] == '/' and api_url[0] == '/':
                url = api_host[:-1] + api_url
            elif api_host[-1] != '/' and api_url[0] != '/':
                url = api_host + '/' + api_url
            else:
                url = api_host + api_url

            # 登陆态：
            api_login = step.api_login  # 获取登陆开关
            if api_login == 'yes':  # 需要判断
                try:
                    eval("login_res")
                    print('已调用过')
                except:
                    print('未调用过')
                    from Myapp.views import project_send_login_for_other
                    project_id = DB_cases.objects.filter(id=DB_step.objects.filter(id=step.id)[0].Case_id)[0].project_id
                    global login_res
                    login_res = project_send_login_for_other(project_id)
                print(login_res)
                # url插入
                if '?' not in url:
                    url += '?'
                    if type(login_res) == dict:
                        for i in login_res.keys():
                            url += i + '=' + login_res[i] + '&'
                else:
                    if type(login_res) == dict:
                        for i in login_res.keys():
                            url += '&' + i + '=' + login_res[i]
                # header插入
                if type(login_res) == dict:
                    header.update(login_res)
            else:
                login_res = {}

            if api_body_method == 'none' or api_body_method == 'null':
                if type(login_res) == dict:
                    response = requests.request(api_method.upper(), url, headers=header, data={})
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data={})
            elif api_body_method == 'form-data':
                files = []
                payload = {}
                for i in eval(api_body):
                    payload += ((i[0], i[1]),)
                if type(login_res) == dict:
                    for j in login_res.keys():
                        payload += ((j, login_res[j]),)
                    response = requests.request(api_method.upper(), url, headers=header, data=payload, files=files)
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data=payload, files=files)
            elif api_body_method == 'x-www-form-urlencoded':
                header["Content-Type"] = "application/x-www-form-urlencoded"
                payload = {}
                for i in eval(api_body):
                    payload += ((i[0], i[1]),)
                if type(login_res) == dict:
                    for j in login_res.keys():
                        payload += ((j, login_res[j]),)
                    response = requests.request(api_method.upper(), url, headers=header, data=payload)
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data=payload)
            elif api_body_method == 'GraphQL':
                header['Content-Type'] = 'applicatin/json'
                query = api_body.split('*QQWRV*')[0]
                graphql = api_body.split('*QQWRV*')[1]
                try:
                    eval(graphql)
                except:
                    graphql = '{}'
                payload = '{"query":%s,"variables":%s}' % (query, graphql)
                if type(login_res) == dict:
                    response = requests.request(api_method.upper(), url, headers=header, data=payload)
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data=payload)
            else:
                if api_body_method == 'Text':
                    header["Content-Type"] = "text/plain"
                if api_body_method == 'JavaScript':
                    header["Content-Type"] = "text/plain"
                if api_body_method == 'Json':
                    api_body = json.loads(api_body)
                    for i in login_res.keys():
                        api_body[i] = login_res[i]
                    api_body = json.dumps(api_body)
                    header["Content-Type"] = "application/json"
                if api_body_method == 'Html':
                    header["Content-Type"] = "text/plain"
                if api_body_method == 'Xml':
                    header["Content-Type"] = "text/plain"
                if type(login_res) == dict:
                    response = requests.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'))
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'))
            response.encoding = 'utf-8'
            res = response.text
            # 存储域
            DB_host.objects.update_or_create(host=api_host)

        print('【返回体】：', res)
        # 提取-路径法
        if get_path != '':
            for i in get_path.split('\n'):
                key = i.split('=')[0].rstrip()
                path = i.split('=')[1].lstrip()
                py_path = ""
                for j in path.split('/'):
                    if j != '':
                        if j[0] != '[':
                            py_path += '["%s"]' % j
                        else:
                            py_path += j
                value = eval("%s%s" % (json.loads(res), py_path))
                exec('global %s\n%s = value' % (key, key))
        # 提取-正则法：
        if get_zz != '':
            for i in get_zz.split('\n'):
                key = i.split('=')[0].rstrip()
                zz = i.split('=')[1].lstrip()
                value = re.findall(zz, res)[0]
                exec('global %s\n%s = "%s" ' % (key, key, value))
        # 断言-路径法：
        if assert_path != '':
            for i in assert_path.split('\n'):
                path = i.split('=')[0].rstrip()
                want = eval(i.split('=')[1].lstrip())
                py_path = ""
                for j in path.split('/'):
                    if j != '':
                        if j[0] != '[':
                            py_path += '["%s"]' % j
                        else:
                            py_path += j
                value = eval("%s%s" % (json.loads(res), py_path))
                self.assertEqual(want, value, '值不相等')
        # 断言-正则法：
        if assert_zz != '':
            for i in assert_zz.split('\n'):
                zz = i.split('=')[0].rstrip()
                want = i.split('=')[1].lstrip()
                value = re.findall(zz, res)[0]
                self.assertEqual(want, value, '值不相等')
        # 断言-全文检索：
        if assert_qz != '':
            for i in assert_qz.split('\n'):
                if i not in res:
                    raise AssertionError('字符串不存在：%s' % i)


def make_defself(step):
    def tool(self):
        Test.demo(self, step)

    setattr(tool, "__doc__", u"%s" % step.name)
    return tool


def make_def(steps):
    for fun in dir(Test):
        if 'test_' in fun:
            delattr(Test, fun)
    for i in range(len(steps)):
        setattr(Test, 'test_' + str(steps[i].index).zfill(3), make_defself(steps[i]))


def run(case_id, case_name, steps):
    make_def(steps)
    suit = unittest.makeSuite(Test)
    filename = 'Myapp/templates/reports/%s.html' % case_id
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(fp, title='TestVirgo测试报告：%s' % case_name, description='用例描述')
    runner.run(suit)


if __name__ == '__main__':
    unittest.main()
