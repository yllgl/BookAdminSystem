from crispy_forms.utils import render_crispy_form
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from account.models import User
from account.myform import UserEditModelForm, NewUserForm, UserPasswordForm


def user_detail(request):
    """ 根据ID获取订单详细 """
    id = request.GET.get("id")
    row_dict = User.objects.filter(id=id)
    if not row_dict.exists():
        return JsonResponse({"status": False, 'error': "数据不存在。"})
    result = {
        "status": True,
        "data": model_to_dict(row_dict.first())
    }
    return JsonResponse(result)


@csrf_exempt
def user_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_object = User.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})
    print(request.POST.dict())
    form = UserEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})
def delete_user(request):
    uid = request.GET.get('id')
    objects = User.objects.filter(id=uid)
    if not objects.exists():
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})

    objects.delete()
    return JsonResponse({"status": True})
def user_new(request):
    form = NewUserForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    ctx = {}
    ctx.update(csrf(request))
    form_html = render_crispy_form(form, context=ctx)
    return JsonResponse({"status": False, 'form_html': form_html})
def user_edit_password(request):
    uid = request.GET.get("uid")
    row_object = User.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})
    print(request.POST.dict())

    form = UserPasswordForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    ctx = {}
    ctx.update(csrf(request))
    form_html = render_crispy_form(form, context=ctx)
    return JsonResponse({"status": False, 'passwordform_html': form_html})
def logout(request):
    request.session.clear()
    return redirect('/login/')