from django.db import models
from mongoengine import connect
from mongoengine import Document
from mongoengine import StringField,ListField
import pymongo
import random
import re
import time
connect('goodJob',host='127.0.0.1',port=27017)
client = pymongo.MongoClient('localhost',27017)
job_db = client['goodJob']
job_tab = job_db['51job_test2']
user_tab = job_db['user']
collect_tab = job_db['collect']
category_tab = job_db['category']
news_tab = job_db['news']
class Job:
    def __init__(self,type,salary,company,location,demand,position):
        self.type = type
        self.salary = salary
        self.company = company
        self.location = location
        self.demand = demand
        self.position = position
class User():
    def __init__(self,email,password):
        self.email = email
        self.password = password
class Collect():
    def __init__(self,username,job,time):
        self.username = username
        self.job = job
        self.time = time

class City(Document):
    city_name = StringField()
    city_link = StringField()
    meta = {'collection':'job_city'}

class News():
    def __init__(self,image,title,time,detail):
        self.image = image
        self.title = title
        self.time = time
        self.detail = detail
#分页的辅助
def pageBean(nowpage,totalpage,pagenum):
    pagenum_list = []
    #中间页码数
    avrgnum = int((pagenum+1)/2)
    #当总页数不超过 需要分页的页数时
    if totalpage <= pagenum:
        for i in range(1, nowpage + 1):
            pagenum_list.append(i)
        for i in range(nowpage + 1, totalpage + 1):
            pagenum_list.append(i)
    #当总页数超过需要分页的页数时候
    else:
        # 如果当前页数小于等于需要分页的中间值的时候
        if nowpage <= avrgnum:
            for i in range(1, nowpage + 1):
                pagenum_list.append(i)
            for i in range(nowpage + 1, 11 + 1):
                pagenum_list.append(i)
        elif nowpage >= totalpage - avrgnum:
            for i in range(totalpage - pagenum-1, nowpage):
                pagenum_list.append(i)
            for i in range(nowpage, totalpage + 1):
                pagenum_list.append(i)
        else:
            for i in range(nowpage - avrgnum, nowpage + 1):
                pagenum_list.append(i)
            for i in range(nowpage + 1, nowpage + avrgnum+1):
                pagenum_list.append(i)
    return pagenum_list


#搜索的只能提示1
def getTagByPoisitonOrCompany(key):
    tag_list = []
    back_list = []
    for i in tabToJob(job_tab.find().limit(300)):
        if key in i.position['name'] :
            #print(i.position['name'])
            tag_list.append(i.position['name'])
        if key in i.company['name']:
            #print(i.company['name'])
            tag_list.append(i.company['name'])
        # 如果匹配的数据小于6，则全部展示，大于6则随机抽六个
    if len(tag_list)<=6:
        back_list = tag_list
    else:
        for i in range(0,6):

            key = random.randint(0,len(tag_list)-1)
            if tag_list[key] in back_list:
                key = random.randint(0, len(tag_list) - 1)
            else:
                back_list.append(tag_list[key])
            print(key)
    return back_list

#搜索的只能提示2
def getTagByCity(key):
    tag_list = []
    back_list = []
    for i in City.objects:
        if key in i.city_name:
            tag_list.append(i.city_name)
    if len(tag_list)<=4:
        back_list = tag_list
    else:
        for i in range(0,4):

            key = random.randint(0,len(tag_list)-1)
            if tag_list[key] in back_list:
                key = random.randint(0, len(tag_list) - 1)
            else:
                back_list.append(tag_list[key])
            print(key)
    return back_list

#将job的数据库转化成对象
def tabToJob(tab_list=[]):
    job_list = []
    for i in tab_list:
        type = i['type']
        salary = i['salary']
        company = i['company']
        location = i['location']
        demand = i['demand']
        position = i['position']
        job = Job(type, salary, company, location, demand, position)
        job_list.append(job)
    return job_list


#首页返回全部数据，这里为了速度限制了100条
def getAllJob():
    backlist = tabToJob(job_tab.find().limit(2000))
    return backlist

#搜索功能返回数据
def getSearchJob(name,city):
    # 只查和城市有关的
    if name == '':
        tab_list = job_tab.find({'location.province':re.compile(city)})
    # 只查和职业,公司有关的
    elif city == '':
        tab_list = job_tab.find({"$or":[{'company.name': re.compile(name)},{'position.name': re.compile(name)}]})
    # 两者同时都有
    else:
        tab_list = job_tab.find({"$and":[{'location.province':re.compile(city)},{"$or":[{'company.name': re.compile(name)},{'position.name': re.compile(name)}]}]})

    back_list = tabToJob(tab_list)
    return back_list

#z最新工作
def getNewJob():
    job_list = tabToJob(job_tab.find())
    back_list = []
    for i in job_list:
        back_list.append(i)
    back_list.sort(key = lambda x:x.position['time'])
    return back_list[-100:]

#查看用户是否存在
def emaliIsExit(email):
    if user_tab.find_one({'email': email}) == None:
        return True
    else:
        return False
#添加一个用户
def adduser(email,psd):
    if user_tab.find_one({'email':email})==None:
        user_tab.insert_one({'email':email,'psd':psd})
        return True
    else:
        return False

#查找是否存在用户
def finduser(email,psd):
    if user_tab.find_one({'email':email,'psd':psd})==None:
        return True
    else:
        return False

#添加搜藏
def addcollect(username,job_url):
    job = job_tab.find_one({'position.url':job_url})
    collect = collect_tab.find_one({'job':job})
    if collect==None:
        print('插入')
        collect_tab.insert_one({'username':username,'job':job,'time':time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    else:
        print('已在')
        return False

 # 通过名字删除搜藏
def delcollectByname(username,job_url):
    if job_url in getcollectByname(username):
        collect_tab.remove({'username': username,'job.position.url':job_url})
        return True
    else:
        return False
#查找收藏
def colltabToclass(collects_tab):
    collects = []
    for i in collects_tab:
        collect = Collect(i['username'],i['job'],i['time'])
        collects.append(collect)
    return collects
#由名字获得收藏的工作的url
def getcollectByname(username):
    collectlist = colltabToclass(collect_tab.find({'username':username}))
    loaded = []
    for i in collectlist:
        loaded.append(i.job['position']['url'])
    return loaded
#获得收藏
def getperson(username):
    return colltabToclass(collect_tab.find({'username':username}))

def total_nums():
    develop = job_tab.find({'position.name': re.compile('(?i)开发')}).count()
    test = job_tab.find({'position.name': re.compile('(?i)测试')}).count()
    operation = job_tab.find({'position.name': re.compile('(?i)运维')}).count()
    implement = job_tab.find({'position.name': re.compile('(?i)实施')}).count()
    return {'develop':develop,'test':test,'operation':operation,'implement':implement}

def devolop_nums():
    java = job_tab.find({'position.name': re.compile('(?i)java')}).count()
    python = job_tab.find({'position.name': re.compile('(?i)python')}).count()
    php = job_tab.find({'position.name': re.compile('(?i)php')}).count()
    c = job_tab.find({'position.name': re.compile('(?i)c')}).count()
    ui = job_tab.find({'position.name': re.compile('(?i)ui')}).count()
    bignum = job_tab.find({'position.name': re.compile('(?i)大数据')}).count()
    front = job_tab.find({'position.name': re.compile('(?i)前端')}).count()

    return {'java':java,'python':python,'php':php,'ui':ui,'bignum':bignum,'front':front,'c':c}
def area_num():
    beijing = job_tab.find({'location.province': re.compile('(?i)北京')}).count()
    shanghai = job_tab.find({'location.province': re.compile('(?i)上海')}).count()
    shenzhen = job_tab.find({'location.province': re.compile('(?i)深圳')}).count()
    guangzhou = job_tab.find({'location.province': re.compile('(?i)广州')}).count()
    hangzhou = job_tab.find({'location.province': re.compile('(?i)杭州')}).count()
    nanjing = job_tab.find({'location.province': re.compile('(?i)南京')}).count()
    dalian = job_tab.find({'location.province': re.compile('(?i)大连')}).count()
    wuhan = job_tab.find({'location.province': re.compile('(?i)武汉')}).count()
    chengdu = job_tab.find({'location.province': re.compile('(?i)成都')}).count()
    xiamen = job_tab.find({'location.province': re.compile('(?i)厦门')}).count()
    fuzhou = job_tab.find({'location.province': re.compile('(?i)福州')}).count()
    suzhou = job_tab.find({'location.province': re.compile('(?i)苏州')}).count()
    others = job_tab.find({'location.province': re.compile('(?i)其他')}).count()
    return {'beijing':beijing,
            'shanghai':shanghai,
            'shenzhen':shenzhen,
            'guangzhou':guangzhou,
            'hangzhou':hangzhou,
            'nanjing':nanjing,
            'dalian':dalian,
            'wuhan':wuhan,
            'chengdu':chengdu,
            'xiamen':xiamen,
            'fuzhou':fuzhou,
            'suzhou':suzhou,
            'others':others,}
'''
for i in job_tab.find({'position.name': re.compile('(?i)python')}):
    print(i['position'])
print(job_tab.find({'position.name': re.compile('(?i)实施')}).count())
'''
def cityandposition(name,city):
    num = job_tab.find({'$and':[{'position.name': re.compile('(?i)'+name)},{'location.province': re.compile('(?i)'+city)}]}).count()
    return num

#添加新闻
def addnews(image,title,time,detail):
    news_tab.insert_one()











