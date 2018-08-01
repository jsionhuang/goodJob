
from django.shortcuts import render,HttpResponse
from .models import *
from django.core.paginator import Paginator
import json
import urllib

def index(request):
    limit = 5
    joblist = getAllJob()
    paginator = Paginator(joblist,limit)
    #t通过request 变成页码
    page = request.GET.get('page',1)
    loaded = paginator.page(page)
    #进行分页设计值，一共展示11页
    total = int(paginator.num_pages)
    #当前的页数
    now = int(page)
    # 用来装页码的数组
    pagenums = pageBean(now,total,11)

    newjobs = getNewJob()
    newagina = Paginator(newjobs,limit)
    newpage = request.GET.get('newpage',1)
    newloaded = newagina.page(newpage)
    newpagenums = pageBean(int(newpage),int(newagina.num_pages),6)
    try:
        username = request.session['username']
        collectloaded = getcollectByname(username)
    except KeyError:
        collectloaded = []
        pass
    print(collectloaded)
    context = {
        'jobs':loaded,
        'pagenums':pagenums,
        'newjobs':newloaded,
        'newpagenums':newpagenums,
        'collect':collectloaded
    }
    return render(request,'index.html',context)
#传入当前的页码，总页码，和需要分的页数，返回页码的list集合
def fsearch1(request):
    q = request.GET['q']
    if q == '':
        return None
    else:
        #对url的中文进行解析
        key_values = urllib.parse.unquote(q)
        print(key_values)
        #获得返回的匹配数据的list
        result = getTagByPoisitonOrCompany(key_values)
        return HttpResponse(json.dumps(result),content_type='application/json')

def fsearch2(request):
    cy = request.GET['cy']
    if cy == '':
        return None
    else:
        #对url的中文进行解析
        key_values = urllib.parse.unquote(cy)
        #获得返回的匹配数据的list
        result = getTagByCity(key_values)
        return HttpResponse(json.dumps(result),content_type='application/json')

def search(request):
    s_name = request.GET.get('s_name')
    s_city = request.GET.get('s_city')
    print("s_name="+s_name+"s_city="+s_city)
    if (s_name == '')and (s_city == ''):
        return render(request, 'index.html')
    else:
        if s_name == '':
            city = urllib.parse.unquote(s_city)
            joblist = getSearchJob('',city)
            print(city)
        elif s_city == '':
            name = urllib.parse.unquote(s_name)
            joblist = getSearchJob(name,'')
            print(name)
        else:
            name = urllib.parse.unquote(s_name)
            city = urllib.parse.unquote(s_city)
            joblist = getSearchJob(name,city)
            print(city+name)
        limit = 5
        paginator = Paginator(joblist, limit)
        # t通过request 变成页码
        page = request.GET.get('page', 2)
        loaded = paginator.page(page)
        # 进行分页设计值，一共展示11页
        total = int(paginator.num_pages)
        # 当前的页数
        now = int(page)
        # 用来装页码的数组
        pagenums = pageBean(now, total, 11)
        newjobs = getNewJob()
        newagina = Paginator(newjobs, limit)
        page = request.GET.get('newpage', 1)
        newloaded = newagina.page(page)
        newpagenums = pageBean(int(page), int(newagina.num_pages), 6)
        context = {
            'jobs': loaded,
            'pagenums': pagenums,
            'newjobs': newloaded,
            'newpagenums': newpagenums,
            'thejoburl':'s_name='+s_name+'&s_city='+s_city+'&',
        }
        return render(request,'index.html',context)

def classfy(request):
    back_list = []
    return back_list

def emaliExit(request):
    email = request.GET.get('email')
    if emaliIsExit(email):
        status = 'yes'
    else:
        status = 'erro'
    return HttpResponse(status)

def register(request):
    email = request.GET.get('email')
    psd1 = request.GET.get('psd1')
    if adduser(email,psd1):
        status = 'yes'
    else:
        status ='error'
    return HttpResponse(status)

def login(request):
    email = request.GET.get('email')
    psd1 = request.GET.get('psd1')
    if finduser(email,psd1):
        status = 'yes'
        request.session['username']=email
    else:
        status = 'error'
    return HttpResponse(status)

def logout(request):
    del  request.session['username']
    status = 'ok'
    return HttpResponse(status)

def collect(request):
    job_url = request.GET.get('url')
    username = request.session['username']
    if addcollect(username,job_url):
        status = 'yes'
    else:
        status = 'error'
    return HttpResponse(status)
def escollect(request):
    job_url = request.GET.get('url')
    username = request.session['username']
    if delcollectByname(username,job_url):
        status = 'yes'
    else:
        status = 'error'
    return HttpResponse(status)

def personal(request):
    try:
        username = request.session['username']
        collect_list = getperson(username)
        limit = 5
        pntor = Paginator(collect_list,limit)
        pn = request.GET.get('pn',1)
        collectloaded = pntor.page(pn)
        pbeans = pageBean(int(pn),int(pntor.num_pages),7)
    except KeyError:
        collectloaded = []
        pass
    content = {
        'collectlist':collectloaded,
        'pbeans':pbeans
    }
    return render(request,'admin-table.html',content)

def chart(request):
    citys = ['北京','上海','深圳','广州','杭州','武汉','大连','厦门','北京','天津','成都','苏州','南京']
    series_JAVA = []
    for i in citys:
        series_JAVA.append({'name':i,'data':[cityandposition('java',i)],'type':'column'})
    series_PYTHON = []
    for i in citys:
        series_PYTHON.append({'name':i,'data':[cityandposition('python',i)],'type':'column'})
    series_C = []
    for i in citys:
        series_C.append({'name':i,'data':[cityandposition('c',i)],'type':'column'})
    series_post_data = total_nums()
    series_post = [{'name': '开发', 'y': series_post_data['develop']},
                   {'name': '运维', 'y': series_post_data['operation']},
                   {'name': '测试', 'y': series_post_data['test']},
                   {'name': '实施', 'y': series_post_data['implement']},
                   ]
    devolop_data = devolop_nums()
    pie1_data = [{'name': 'java开发', 'y':devolop_data['java'] },
                 {'name': 'python开发', 'y': devolop_data['python']},
                 {'name': 'php开发', 'y': devolop_data['php']},
                 {'name': 'ui设计', 'y': devolop_data['ui']},
                 {'name': '大数据', 'y': devolop_data['bignum']},
                 {'name': '前端', 'y': devolop_data['front']},
                 {'name': 'C++', 'y': devolop_data['c']},]
    # pie2_data = [i for i in one_day_deal_area()]
    pie2_data = []
    area_data = area_num()
    for i in area_data:
        pie2_data.append({'name':i,'y':area_data[i]})
    context = {
        'series_JAVA':series_JAVA,
        'series_PYTHON':series_PYTHON,
        'series_C':series_C,
        'series_post':series_post,
        'pie1_data':pie1_data,
        'pie2_data':pie2_data
    }
    return  render(request,'chart2.html',context)

def news(request):
    return  render(request,'index2.html')



