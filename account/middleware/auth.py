from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from account.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 排除那些不需要登录就能访问的页面
        if request.path_info in ["/login/", "/image/code/"]:
            return
        info_dict = request.session.get("info")
        print("in process_request",info_dict)
        if info_dict:
            if request.path_info in ["/adminUser/","/adminBook/",
                                     "/adminRecord/","/adminAddBook/",
                                     "/bookedit/","/deletebook/","/useredit/",
                                     "/deleteuser/","/usernew/","/usereditpassword/"]:
                user = User.objects.filter(id=info_dict["id"]).first()
                if user.isadmin:
                    info_dict.update({"isadmin":True})
                    request.session["info"]=info_dict
                    return
                else:
                    return redirect("/searchBook/")
            return
        return redirect('/login/')
