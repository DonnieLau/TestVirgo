// 左侧记录刷新
function log_refresh() {
    // 清空
    var div = document.getElementById('home_log_plan');
    div.innerHTML = '';
    // 生成新的
    $.get('/get_home_log/', {}, function (ret) {
        var res = eval(ret);
        var all_logs = res.all_logs;
        for (var i = 0; i < all_logs.length; i++) {
            var a = document.createElement('a');
            a.class = "log";
            a.href = "/home_log/" + all_logs[i].id + "/";
            a.style = "text-decoration: none"
            var s1 = document.createElement('span');
            s1.style = "font-size: 15px;color: black"
            s1.innerText = all_logs[i].api_method + ' - ';
            var s2 = document.createElement('span');
            s2.innerText = all_logs[i].api_host + all_logs[i].api_url;
            a.appendChild(s1);
            a.appendChild(s2);
            div.appendChild(a);
            div.appendChild(document.createElement('br'));
        }
    })
}

// 首页发送请求
function home_send() {
    // 获取接口的所有数据
    var ts_method = document.getElementById('ts_method').value;
    var ts_url = document.getElementById('ts_url').value;
    var ts_host = document.getElementById('ts_host').value;
    var ts_header = document.getElementById('ts_header').value;
    // 判断顶部的数据是否填充完
    if (ts_method == 'none') {
        alert('请选择请求方式！');
        return
    }
    if (ts_url == '') {
        alert('请输入url！');
        return
    }
    if (ts_host == '') {
        alert('请输入host！');
        return
    }
    if (ts_header == "") {
        alert("请输入header！");
        return
    }
    //判断关键数据是否符合规则
    if (ts_host.slice(0, 7) != 'http://' && ts_host.slice(0, 8) != 'https://' && ts_host.slice(0, 4) != '全局域名') {
        alert('host必须以http://或https://开头！');
        return
    }
    if (ts_header != '') {
        try {
            JSON.parse(ts_header)
        } catch (e) {
            alert('header请求头不符合json规范！');
            return
        }
    }
    var ts_body_method = $('ul#myTab li[class="active"]')[0].innerText;
    console.log(ts_body_method);
    if (ts_body_method == 'none') {
        var ts_api_body = ''
    }
    if (ts_body_method == 'form-data') {
        var ts_api_body = []; //新建这个空列表用来存放后续的数据
        var tbody_ = $("table#mytable tbody")[0]; //获取该表格的内容部分
        var trlist = tbody_.children; //获取下面所有tr，每个tr就是一个键值对实际上
        for (var i = 0; i < trlist.length; i++) {
            var tdarr = trlist[i].children; // 获取tr下的俩个td
            var key = tdarr[0].innerText; // 获取key
            var value = tdarr[1].innerText; // 获取value
            ts_api_body.push([key, value]); // 作为一个数组，存放到这个大数组里。
        }
        ts_api_body = JSON.stringify(ts_api_body);
    }
    if (ts_body_method == 'x-www-form-urlencoded') {
        var ts_api_body = []; //新建这个空列表用来存放后续的数据
        var tbody_ = $("table#mytable2 tbody")[0]; //获取该表格的内容部分
        var trlist = tbody_.children; //获取下面所有tr，每个tr就是一个键值对实际上
        for (var i = 0; i < trlist.length; i++) {
            var tdarr = trlist[i].children; // 获取tr下的俩个td
            var key = tdarr[0].innerText; // 获取key
            var value = tdarr[1].innerText; // 获取value
            ts_api_body.push([key, value]); // 作为一个数组，存放到这个大数组里。
        }
        ts_api_body = JSON.stringify(ts_api_body);
    }
    if (ts_body_method == 'Text') {
        var ts_api_body = document.getElementById('raw_Text').value;
    }
    if (ts_body_method == 'JavaScript') {
        var ts_api_body = document.getElementById('raw_JavaScript').value;
    }
    if (ts_body_method == 'Json') {
        var ts_api_body = document.getElementById('raw_Json').value;
    }
    if (ts_body_method == 'Html') {
        var ts_api_body = document.getElementById('raw_Html').value;
    }
    if (ts_body_method == 'Xml') {
        var ts_api_body = document.getElementById('raw_Xml').value;
    }
    if (ts_body_method == 'GraphQL') {
        var body_plan_G_Q = document.getElementById('body_plan_G_Q').value;
        var body_plan_G_G = document.getElementById('body_plan_G_G').value;
        var ts_api_body = body_plan_G_Q + '*QQWRV*' + body_plan_G_G;
    }
    // 发送请求给后台
    $.get('/api_send_home/', {
        'ts_method': ts_method,
        'ts_url': ts_url,
        'ts_host': ts_host,
        'ts_header': ts_header,
        'ts_body_method': ts_body_method,
        'ts_api_body': ts_api_body
    }, function (ret) {
        log_refresh();
        $("li a[href=#response]").click(); //点击一下返回体按钮
        document.getElementById('ts_response_body').value = ret; //把返回值显示到返回值多行文本框中
    })
}

// 首页保存当前接口信息
function save_api(project_id) {
    // 获取接口的所有数据
    var ts_method = document.getElementById('ts_method').value;
    var ts_url = document.getElementById('ts_url').value;
    var ts_host = document.getElementById('ts_host').value;
    var ts_header = document.getElementById('ts_header').value;
    // 判断顶部的数据是否填充完
    if (ts_method == 'none') {
        alert('请选择请求方式！');
        return
    }
    if (ts_url == '') {
        alert('请输入url！');
        return
    }
    if (ts_host == '') {
        alert('请输入host！');
        return
    }
    //判断关键数据是否符合规则
    if (ts_host.slice(0, 7) != 'http://' && ts_host.slice(0, 8) != 'https://') {
        alert('host必须以http://或https://开头！');
        return
    }
    if (ts_header != '') {
        try {
            JSON.parse(ts_header)
        } catch (e) {
            alert('header请求头不符合json规范！');
            return
        }
    }
    var ts_body_method = $('ul#myTab li[class="active"]')[0].innerText;
    if (ts_body_method == 'none') {
        var ts_api_body = ''
    }
    if (ts_body_method == 'form-data') {
        var ts_api_body = []; //新建这个空列表用来存放后续的数据
        var tbody_ = $("table#mytable tbody")[0]; //获取该表格的内容部分
        var trlist = tbody_.children; //获取下面所有tr，每个tr就是一个键值对实际上
        for (var i = 0; i < trlist.length; i++) {
            var tdarr = trlist[i].children; // 获取tr下的俩个td
            var key = tdarr[0].innerText; // 获取key
            var value = tdarr[1].innerText; // 获取value
            ts_api_body.push([key, value]);// 作为一个数组，存放到这个大数组里。
        }
        ts_api_body = JSON.stringify(ts_api_body);
    }
    if (ts_body_method == 'x-www-form-urlencoded') {
        var ts_api_body = []; //新建这个空列表用来存放后续的数据
        var tbody_ = $("table#mytable2 tbody")[0]; //获取该表格的内容部分
        var trlist = tbody_.children; //获取下面所有tr，每个tr就是一个键值对实际上
        for (var i = 0; i < trlist.length; i++) {
            var tdarr = trlist[i].children; // 获取tr下的俩个td
            var key = tdarr[0].innerText; // 获取key
            var value = tdarr[1].innerText; // 获取value
            ts_api_body.push([key, value]);// 作为一个数组，存放到这个大数组里。
        }
        ts_api_body = JSON.stringify(ts_api_body);
    }
    if (ts_body_method == 'Text') {
        var ts_api_body = document.getElementById('raw_Text').value;
    }
    if (ts_body_method == 'JavaScript') {
        var ts_api_body = document.getElementById('raw_JavaScript').value;
    }
    if (ts_body_method == 'Json') {
        var ts_api_body = document.getElementById('raw_Json').value;
    }
    if (ts_body_method == 'Html') {
        var ts_api_body = document.getElementById('raw_Html').value;
    }
    if (ts_body_method == 'Xml') {
        var ts_api_body = document.getElementById('raw_Xml').value;
    }

    if (ts_body_method == 'GraphQL') {
        var body_plan_G_Q = document.getElementById('body_plan_G_Q').value;
        var body_plan_G_G = document.getElementById('body_plan_G_G').value;
        var ts_api_body = body_plan_G_Q + '*QQWRV*' + body_plan_G_G
    }
    // 发送请求给后台
    $.get('/api_save_home/', {
        'project_id': project_id,
        'ts_method': ts_method,
        'ts_url': ts_url,
        'ts_host': ts_host,
        'ts_header': ts_header,
        'ts_body_method': ts_body_method,
        'ts_api_body': ts_api_body,
    }, function (ret) {
        alert('保存成功！')
    })
}

// 首页查找
function search_home(user_id) {
    var key = document.getElementById('search_input').value;
    // 清空搜索框
    var d = document.getElementById('search_result');
    d.innerHTML = '';
    var sclose = document.createElement('button');
    sclose.id = 'search_close';
    sclose.classList = 'btn btn-danger';
    sclose.style = 'position: absolute;right: 1%;z-index: 999';
    sclose.onclick = function () {
        document.getElementById('search_result').style.display = 'none';
    };
    sclose.innerText = '关闭';
    d.appendChild(sclose);
    if (key == '' || key == ' ') {
        return
    }
    $.get('/search_home/', {
        'key': key,
        'user_id': user_id
    }, function (ret) {
        d.style.display = 'block';
        var results = ret.results;
        for (var i = 0; i < results.length; i++) {
            var a = document.createElement('a');
            a.href = results[i].url;
            a.target = '__blank';
            a.innerText = '【' + results[i].type + '】：' + results[i].text;
            d.appendChild(a);
            d.appendChild(document.createElement('br'))
        }
    })
}