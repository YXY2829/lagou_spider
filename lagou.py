import requests
import pickle
from peewee import *

db = MySQLDatabase('mydb', user='root', passwd='rootroot')

class Lagou(Model):
    businessZones = CharField(null=True)
    companyFullName = CharField()
    companyShortName = CharField(null=True)
    positionName = CharField()
    companyLabelList = CharField(null=True)
    companySize = CharField()
    district = CharField(null=True)
    education = CharField()
    financeStage = CharField(null=True)
    createTime = CharField()
    industryField = CharField(null=True)
    positionAdvantage = CharField(null=True)
    salary = CharField()
    workYear = CharField()

    class Meta:
        database = db

db.connect()
db.create_table(Lagou)

url='http://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
headers={
    'Host':'www.lagou.com',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Referer':'http://www.lagou.com/jobs/list_Python?px=default&city=%E5%8C%97%E4%BA%AC'
}

json_data = []
for i in range(1,31):
    data={'first':False,'pn':i,'kd':'Python'}
    r=requests.post(url,headers=headers,data=data)
    json_data.append(r.json())

with open('data', 'wb') as f:
    pickle.dump(json_data, f)

with open('data', 'rb') as f:
    datas = pickle.load(f)
    for data in datas:
        info = data['content']['positionResult'].get('result')
        for i in info:
            print(i['businessZones'])
            print(i['companyFullName'])
            print(i['companyShortName'])
            print(i['positionName'])
            print(i['companyLabelList'])
            print(i['companySize'])
            print(i['district'])
            print(i['education'])
            print(i['financeStage'])
            print(i['createTime'])
            print(i['industryField'])
            print(i['positionAdvantage'])
            print(i['salary'])
            print(i['workYear'])
            print('-----------------')

            Lagou.create(
                businessZones = ','.join(list(i['businessZones'])) if i['businessZones'] else None,
                companyFullName = i['companyFullName'],
                companyShortName = i['companyShortName'],
                positionName = i['positionName'],
                companyLabelList = ','.join(list(i['companyLabelList'])) if i['companyLabelList'] else None,
                companySize = i['companySize'],
                district = i['district'],
                education = i['education'],
                financeStage = i['financeStage'],
                createTime = i['createTime'],
                industryField = i['industryField'],
                positionAdvantage = i['positionAdvantage'],
                salary = i['salary'],
                workYear = i['workYear'])

db.close()
