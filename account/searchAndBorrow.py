from django import forms
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import *
from .myform import BookModelForm


@csrf_exempt
def searchBook(request):
    if request.method == "GET":
        objects = Book.objects.all()
        query = request.GET.get('q')
        if query:
            objects = Book.objects.filter(
                Q(title__icontains=query) | Q(summary__icontains=query) |
                Q(author__icontains=query) | Q(translator__icontains=query) |
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

        return render(request,"searchBook.html",{"page_obj": page_obj})
    elif request.method == "POST":
        data = request.POST.dict()
        id = data["id"]
        objects = Book.objects.filter(id=id)
        if objects.exists():
            book = objects.first()
            userid = request.session.get("info").get("id")
            user = User.objects.filter(id=userid).first()
            Record.objects.create(userid=user,bookid=book,category=1)
            book.onboard = False
            book.save()
            return JsonResponse({"status":True})
        else:
            return JsonResponse({"status":False,"err":"数据错误"})
@csrf_exempt
def borrowedBook(request):
    if request.method =='GET':
        userid = request.session.get("info").get("id")
        user = User.objects.filter(id=userid).first()
        book_set = Record.objects.filter(userid=user).values('bookid')
        bk_set = book_set.annotate(Mycount=Count('bookid'))
        objects = []
        for item in bk_set:
            if item['Mycount']%2:
                objects.append(Book.objects.get(pk=item["bookid"]))
        return render(request,"borrowedBook.html",{"page_obj":objects})
    elif request.method =='POST':
        data = request.POST.dict()
        id = data["id"]
        objects = Book.objects.filter(id=id)
        if objects.exists():
            book = objects.first()
            book.onboard = True
            book.save()
            userid = request.session.get("info").get("id")
            user = User.objects.filter(id=userid).first()
            Record.objects.create(userid=user, bookid=book, category=0)
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False, "err": "数据错误"})

def borrowedRecord(request):
    userid = request.session.get("info").get("id")
    user = User.objects.filter(id=userid).first()
    book_set = Record.objects.filter(userid=user).all().order_by("-datetime")
    paginator = Paginator(book_set, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,"borrowedRecord.html",{"page_obj":page_obj})
def book_detail(request):
    """ 根据ID获取订单详细 """
    id = request.GET.get("id")
    row_dict = Book.objects.filter(id=id)
    if not row_dict.exists():
        return JsonResponse({"status": False, 'error': "数据不存在。"})
    result = {
        "status": True,
        "data": model_to_dict(row_dict.first())
    }
    return JsonResponse(result)


@csrf_exempt
def book_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_object = Book.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})

    form = BookModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})
def delete_book(request):
    """ 删除订单 """
    uid = request.GET.get('id')
    exists = Book.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})

    Book.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})