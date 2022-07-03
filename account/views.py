import json
import string
from copy import deepcopy
from math import ceil
import random

import requests
from django.db.models import Q
from django.forms import  ModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator

from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from . import models
from .models import Book, User, Record
from .myform import UserEditModelForm, NewUserForm, UserPasswordForm


def mydefaultContext(request):
    nav = [{"title": "查找图书", "link": "/searchBook"},
           {"title": "管理已借图书", "link": "/borrowedBook"},
           {"title": "借阅记录", "link": "/borrowedRecord"},
           {"title": "管理员操作", "isdropdown": True,"isadmin":True,
            "drop_menu": [{"title": "管理图书", "link": "/adminBook"},
                          {"title": "管理用户", "link": "/adminUser"},
                          {"title": "管理用户借阅记录", "link": "/adminRecord"},
                          {"title": "添加图书", "link": "/adminAddBook"}]},
           ]
    global_default_dict = {"nav_items": nav}
    for i, item in enumerate(global_default_dict["nav_items"]):
        isok = False
        if item.get("isdropdown", False):
            for menu in item["drop_menu"]:
                if menu["link"].strip("/") in request.path:
                    global_default_dict["nav_items"][i].update({"active": "active"})
                    isok = True
                    break
            if isok:
                break
        else:
            if item["link"].strip("/") in request.path:
                global_default_dict["nav_items"][i].update({"active": "active"})
                break
    return global_default_dict


# Create your views here.

def index(request):
    return render(request,"empty.html")




def adminBook(request):

    objects = Book.objects.all()
    query = request.GET.get('q')
    if query:
        objects = Book.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query) |
            Q(author__icontains=query) | Q(translator__icontains=query)|
            Q(isbn__icontains=query) | Q(chinaclass__icontains=query) |
            Q(publisher__icontains=query)
        ).distinct()
    paginator = Paginator(objects, 10)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    form = BookModelForm()
    return render(request,"adminBook.html",{"page_obj":page_obj,"form":form})

def adminUser(request):
    objects = User.objects.all()
    query = request.GET.get('q')
    if query:
        objects = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).distinct()
    paginator = Paginator(objects, 10)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    form = UserEditModelForm()
    newform = NewUserForm()
    passwordform = UserPasswordForm()
    return render(request,"adminUser.html",{"page_obj":page_obj,"form":form,"formNew":newform,"formPassword":passwordform})

def adminRecord(request):
    objects = Record.objects.all().order_by("-datetime")
    return render(request,"adminRecord.html",{"data":objects})
@method_decorator(csrf_exempt, name='dispatch')
class adminAddBook(View):
    def __init__(self):
        super(adminAddBook, self).__init__()
        self.catogory_id = [{"id":"1635131814758ref","category":"A 马克思主义、列宁主义、毛泽东思想、邓小平理论"},{"id":"16351318147816lp","category":"B 哲学、宗教"},{"id":"1635131814788f6s","category":"C 社会科学总论"},{"id":"1635131814796thh","category":"D 政治、法律"},{"id":"1635131814802dcw","category":"E 军事"},{"id":"1635131814808y6q","category":"F 经济"},{"id":"1635131814812hyi","category":"G 文化、科学、教育、体育"},{"id":"1635131814827g70","category":"H 语言、文字"},{"id":"1635131814832sf7","category":"I 文学"},{"id":"1635131814838m23","category":"J 艺术"},{"id":"1635131814847ktm","category":"K 历史、地理"},{"id":"","category":"L"},
                            {"id":"1635131814852zyj","category":"N 自然科学总论"},{"id":"","category":"M"},{"id":"16351318148563v0","category":"O 数理科学和化学"},{"id":"1635131814861131","category":"P 天文学、地球科学"},{"id":"1635131814867cl4","category":"Q 生物科学"},{"id":"1635131814872ms6","category":"R 医药、卫生"},{"id":"16351318148772ku","category":"S 农业科学"},{"id":"1635131814883jkl","category":"T 工业技术"},{"id":"16351318148897fb","category":"U 交通运输"},{"id":"1635131814894n29","category":"V 航空、航天"},
                            {"id":"","category":"W"},{"id":"16351318149018c9","category":"X 环境科学、安全科学"},{"id":"","category":"Y"},{"id":"1635131814908pc6","category":"Z 综合性图书"}]
        self.url = "http://api.ibook.tech/book/api/search/books?from={}&size=10&keyword={}&categoryId={}&withTotal=1"
        self.access_token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIxNjU1NDYyMzg2MTc1MHJqIiwiYXBwSWQiOiJ3eDdlMTYwNmE1MzE3MmZjMWUiLCJvcGVuSWQiOiJvcVd3NjQtUFM3T3pUWlZGeUxxWEhoTTU5dUtnIiwiZXhwIjoxNjU1ODIyNDAxfQ.KAeMKHnYAxd8icUGrFq2RZ9QiUPbQRSMvbdAWcx6Bns"
        self.header = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
                  "content-type":"application/x-www-form-urlencoded","referer":"https://servicewechat.com/wx7e1606a53172fc1e/37/page-frame.html",
                       "accept-encoding": "gzip, deflate, br","host":"api.ibook.tech",
                       "access-token":self.access_token}
        self.detail_url = "http://api.ibook.tech/book/api/book/detail?bookId={}"
        print("initialize adminAddBook(View)")

    def get(self,request):
        request.session.setdefault("addbook_q","")
        request.session.setdefault("addbook_total", 0)
        request.session.setdefault("addbook_objects", [])
        request.session.setdefault("addbook_catogory", "")
        request.session.setdefault("addbook_page", 0)
        default_dict = {"options":models.Book.category_choices}
        query = request.GET.get('q',"")
        catogory = request.GET.get('category', "")
        print(dict(request.session))
        if catogory!="":
            catogory = int(catogory)
        if query==request.session.get("addbook_q") and catogory==request.session.get("addbook_catogory"):
            pages = ceil(request.session["addbook_total"]/10)
            page = int(request.GET.get('page',1))
            page = min(pages,page)
            page = max(1,page)
            print("page:",page)
            print("session_page:",request.session.get("addbook_page"))
            print(page<=request.session.get("addbook_page"))
            if page<=request.session.get("addbook_page"):
                start = min(max((page - 1) * 10, 0), len(request.session["addbook_objects"]) - 10)
                end = min(start + 10, len(request.session["addbook_objects"]))
                default_dict.update({"page_obj":request.session["addbook_objects"][start:end],"total":request.session["addbook_total"]})
                print("in page<=sesison.page:default_dict",default_dict)
                return render(request,"adminAddBook.html",default_dict)
            else:
                if request.session["addbook_page"]+1==page:
                    pass
                else:
                    default_dict.update({"errcode": True, "err": "禁止跳页操作"})
                    return render(request,"adminAddBook.html",default_dict)
            response = requests.get(self.url.format((page-1)*10, query, self.catogory_id[catogory]["id"] if catogory else ""), headers=self.header)
            data = response.content.decode("utf-8")
            final_data = json.loads(data)
            if final_data["errcode"] != 0:
                print(final_data)
                default_dict.update({"errcode":True,"err":final_data})
                return render(request,"adminAddBook.html",default_dict)
            final_data = final_data["data"]
            request.session["addbook_total"] = final_data["total"]
            books = final_data["books"]
            objects = []
            for item in books:
                response = requests.get(self.detail_url.format(item["id"]),
                                        headers=self.header)
                data = response.content.decode("utf-8")
                final_data = json.loads(data)
                if final_data["errcode"] != 0:
                    default_dict.update({"errcode": True, "err": final_data})
                    return default_dict
                else:
                    obj = final_data["data"]
                    obj["imgdir"]=obj["img"]
                    if not self.notexist(obj):
                        obj["isexist"] = True
                    obj["id"] = item["id"]
                    objects.append(obj)
            request.session["addbook_page"] = page
            request.session["addbook_objects"].extend(objects)
            start = min(max((page - 1) * 10, 0), len(request.session["addbook_objects"]) - 10)
            end = min(start + 10, len(request.session["addbook_objects"]))
            default_dict.update({"page_obj":request.session["addbook_objects"][start:end],"total":request.session["addbook_total"]})
            print("ready return")
            print("default_dict",default_dict)
            return render(request,"adminAddBook.html",default_dict)
        else:
            page = 1
            request.session["addbook_q"] = query
            request.session["addbook_catogory"] = catogory
            response = requests.get(self.url.format((page - 1) * 10, query, self.catogory_id[catogory]["id"] if catogory!="" else ""),
                                    headers=self.header)
            data = response.content.decode("utf-8")
            final_data = json.loads(data)
            if final_data["errcode"] != 0:
                print(final_data)
                default_dict.update({"errcode": final_data["errcode"]})
                return render(request,"adminAddBook.html",default_dict)
            final_data = final_data["data"]
            request.session["addbook_total"] = final_data["total"]
            books = final_data["books"]
            objects = []
            for item in books:
                response = requests.get(self.detail_url.format(item["id"]),
                                        headers=self.header)
                data = response.content.decode("utf-8")
                final_data = json.loads(data)
                if final_data["errcode"] != 0:
                    print(final_data)
                else:
                    obj = final_data["data"]
                    obj["imgdir"] = obj["img"]
                    if not self.notexist(obj):
                        obj["isexist"] = True
                    obj["id"] = item["id"]
                    objects.append(obj)
            request.session["addbook_objects"] = objects
            request.session["addbook_page"] = 1
            start = min(max((page - 1) * 10, 0), len(request.session["addbook_objects"]) - 10)
            end = min(start + 10, len(request.session["addbook_objects"]))
            default_dict.update({"page_obj": request.session["addbook_objects"][start:end],"total":request.session["addbook_total"]})
            return render(request,"adminAddBook.html",default_dict)
    def notexist(self,data,method='get'):
        if method=="post":
            data["onboard"] = True
        data["imgdir"] = data.setdefault("img", "")
        title = data.setdefault("title", "")
        author = data.setdefault("author", "")
        imgdir = data.setdefault("img", "")
        translator = data.setdefault("translator", "")
        isbn = data.setdefault("isbn", "")
        chinaclass = data.setdefault("chinaclass", "L其他")
        binding = data.setdefault("binding", "")
        language = data.setdefault("language", "")
        publisherAddress = data.setdefault("publisherAddress", "")
        price = data.setdefault("price", "")
        publisher = data.setdefault("publisher", "")
        isbn10 = data.setdefault("isbn10", "")
        page = data.setdefault("page", "")
        category = data.setdefault("category", "")
        if chinaclass:
            search_category = ord(chinaclass[0]) - ord('A')
            if method=="post":
                data["category"] = search_category
        pubdate = data.get("pubdate", "")
        objects = models.Book.objects.filter((Q(title__icontains=title) | Q(title__isnull=True)) &
                                             (Q(imgdir__icontains=imgdir) | Q(imgdir__isnull=True)) &
                                             (Q(translator__icontains=translator) | Q(translator__isnull=True)) &
                                             (Q(isbn__icontains=isbn) | Q(isbn__isnull=True)) &
                                             (Q(chinaclass__icontains=chinaclass) | Q(chinaclass__isnull=True)) &
                                             (Q(binding__icontains=binding) | Q(binding__isnull=True)) &
                                             (Q(language__icontains=language) | Q(language__isnull=True)) &
                                             (Q(publisherAddress__icontains=publisherAddress) | Q(
                                                 publisherAddress__isnull=True)) &
                                             (Q(price__icontains=price) | Q(price__isnull=True)) &
                                             (Q(publisher__icontains=publisher) | Q(publisher__isnull=True)) &
                                             (Q(isbn10__icontains=isbn10) | Q(isbn10__isnull=True)) &
                                             (Q(page__icontains=page) | Q(page__isnull=True)) &
                                             (Q(pubdate__icontains=pubdate) | Q(pubdate__isnull=True)) &
                                             (Q(category__icontains=search_category) | Q(category__isnull=True)) &
                                             (Q(author__icontains=author) | Q(author__isnull=True)))

        if objects.exists():
            return None
        return data
    def post(self,request):
        tmp = request.POST.dict()
        print("in addBook post")
        print(tmp)
        data = json.loads(tmp["data"])
        page = tmp["page"]
        tmp = self.notexist(data,'post')
        if not tmp:
            newlist = request.session["addbook_objects"]
            page = int(page)
            start = min(max((page - 1) * 10, 0), len(newlist) - 10)
            end = min(start + 10, len(newlist))
            for i, obj in enumerate(newlist[start:end]):
                if not self.notexist(obj):
                    obj["isexist"] = True
                newlist[start + i] = obj
            request.session["addbook_objects"]= newlist
            return JsonResponse({"status": False, "error": "数据库已存在"})
        else:
            print(tmp)
            form = BookModelForm(data=tmp)
            if form.is_valid():
                form.save()
                newlist = request.session["addbook_objects"]
                page = int(page)
                start = min(max((page-1)*10,0),len(newlist)-10)
                end = min(start+10,len(newlist))
                for i,obj in enumerate(newlist[start:end]):
                    if not self.notexist(obj):
                        obj["isexist"]=True
                    newlist[start+i]=obj
                request.session["addbook_objects"]= newlist
                return JsonResponse({"status": True})
            else:
                return JsonResponse({"status": False, "error": "数据无效"})
class BookModelForm(ModelForm):
    class Meta:
        model = models.Book
        exclude = []

