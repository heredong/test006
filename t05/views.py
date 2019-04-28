#-*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseNotAllowed
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template
from django.urls import reverse


def index(req):
    # return render(req,'index.html')
    # u_name = req.get_signed_cookie(
    #     'uname',
    #     default=None,
    #     salt=settings.SECRET_KEY
    # )
    u_name = req.session.get('uname')
    is_login = True
    if not u_name:
        u_name="youke"
        is_login=False

    data={
        'uname':u_name,
        'is_login':is_login
    }
    return render(req,'index.html',{'data':data})

def login_view(req):
    if req.method == "GET":
        return render(req,"login.html")
    elif req.method =='POST':

        u_name = req.POST.get("name")
        u_pwd = req.POST.get('pwd')

        if u_pwd!='123':
            return render(req,'login.html',{'error_msg':'zhanghaocuowuhuomimacuowu'})

        response = redirect(reverse('t05:index'))

        # response.set_signed_cookie('uname',u_name,salt=settings.SECRET_KEY)
        req.session['uname']=u_name

        return response

    else:
        return HttpResponseNotAllowed("错误")

def logout_view(req):
    response = redirect(reverse('t05:index'))

    # response.delete_cookie('uname')
    del req.session['uname']
    return response

def register_view(req):
    if req.method=='GET':
        return render(req,'register.html')
    else:
        uname = req.POST.get("uname")
        pwd = req.POST.get('pwd')

        confirm_pwd = req.POST.get('confirm_pwd')
        if not uname or len(uname)<2:
            return render(req,'register.html',{'error_msg':'username is short'})
        if pwd and pwd==confirm_pwd:
            pass
        else:
            return render(
                req,
                'register.html',
                {'error_msg':'passwrod is wrong'}
            )

        if User.objects.filter(username=uname).exists():
            return render(req,'register.html',{'error_msg':'username  multiply'})
        user = User.objects.create_user(
            username=uname,
            password=pwd
        )
        return HttpResponse('create {uname} successfully'.format(uname=user.username))

def login_v2(req):
    if req.method =="GET":
        return render(req,'login_v2.html')
    else:

        uname = req.POST.get('uname')
        pwd  =req.POST.get('pwd')

        if uname and pwd:
            pass
        else:
            return render(req,'login_v2.html',{'error_msg':'error'})

        user = authenticate(username=uname, password=pwd)

        if user:
            login(req, user)

            next = req.GET.get("next")
            if next:
                return redirect(next)
            else:
                return HttpResponse('login sucessfully')
        else:
            return render(
                req,
                'login_v2.html',
                {'error_msg':'error'}
            )
@login_required(login_url='/t05/login_v2')
def home(req):
    user = req.user

    print(user.is_anonymous)
    print(user.username)

    return HttpResponse(user.username)


def logout_v2(req):
    logout(req)
    return HttpResponse('quit successfully')

def send_my_mail(req):
    title = 'sfvsdv'
    message='66666'

    email_from = settings.DEFAULT_FROM_EMAIL

    recivies = [
        "980563921@qq.com"

    ]
    url = 'http://www.baidu.com'

    template = get_template('temp.html')

    html_str = template.render({'url':url})

    print(html_str)

    send_mail(
        title,message,email_from,recivies,html_message=html_str
    )

    return HttpResponse('ok')