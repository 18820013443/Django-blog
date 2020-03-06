# from django.contrib.auth.models import User
from . import forms
from . import models
from django.contrib import auth
from .models import Ouser
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# 第四个是 auth中用户权限有关的类。auth可以设置每个用户的权限。
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import RegisterForm, LoginForm#, ProfileForm
import re




# Create your views here.
@csrf_exempt
def register(request):
    context = {}
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        next_to = request.POST.get('next', 0)
        if register_form.is_valid():
            register_name = request.POST['username']
            register_password = request.POST['password']
            register_password2 = request.POST['password2']
            register_email = request.POST['email']
            context = {'username': register_name, 'pwd': register_password, 'email': register_email}
            #判断密码是否为纯数字
            if register_password.isdigit():
                context['pwd_error'] = 'nums'
                return render(request, 'account/signup.html', context)
            
            # 判断第一次和第二次输入的密码是否一致
            if register_password != register_password2:
                context['pwd_error'] = 'unequal'
                return render(request, 'account/signup.html', context)

            # 判断用户是否存在
            user = Ouser.objects.filter(username=register_name)
            email = Ouser.objects.filter(email=register_email)
            pwd_length = len(register_password)
            if pwd_length < 8 or pwd_length > 20:
                context['pwd_error'] = 'length'
                return render(request, 'account/signup.html', context)

            user_length = len(register_name)
            if user_length < 5 or user_length > 20:
                context['user_error'] = 'length'
                return render(request, 'account/signup.html', context)

            if user:
                context['user_error']='exit'
                return render(request, 'account/signup.html', context)

            if not re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', register_email):
                context['email_error'] = 'format'
                return render(request, 'account/signup.html', context)

            if email:
                context['email_error'] = 'exit'
                return render(request, 'account/signup.html', context)

            # 添加到数据库（还可以加一些字段的处理）
            user = Ouser.objects.create_user(username=register_name, password=register_password, email=register_email)
            user.save()
            user = auth.authenticate(username=register_name, password=register_password)

             # 添加到session
            request.session['username'] = register_name
            request.session['email'] = register_email
            request.session['uid'] = user.id
            request.session['nick'] = ''

            # 调用auth登录
            auth.login(request, user)
            # 重定向到首页
            if next_to == '':
                next_to = '/index'
            return redirect(next_to)
    else:
        next_to = request.GET.get('next', '/index')
        context = {'isLogin': False}
        context['next_to'] = next_to
    # 将req 、页面 、以及context{}（要传入html文件中的内容包含在字典里）返回
    return render(request, 'account/signup.html', context)


@csrf_exempt
def login(request):
    context = {}
    if request.method == 'POST':
        next_to = request.POST.get('next', '/index')
        remember = request.POST.get('remember',0)
        login_form = LoginForm(request.POST)
        print(login_form)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            context={'username':login_name,'password':login_password}
            user = authenticate(username = login_name, password = login_password)
            if next_to=='':
                next_to='/index'
            if user is not None:
                if user.is_active:
                    request.session['username'] = user.username
                    request.session['email'] = user.email
                    request.session['uid'] = user.id
                    request.session['nick'] = None
                    request.session['tid'] = None
                    response = HttpResponseRedirect(next_to)
                    if remember != 0:
                        response.set_cookie('username', login_name)
                    else:
                        response.set_cookie('username', '', max_age = -1)
                    return response
                else:
                    context['inactive'] = True
                    return render(request, 'account/login.html', context)
            else:
                context['error'] = True
                return render(request, 'account/login.html', context)
        else:
            context['format'] = True
            return render(request, 'account/login.html', context)
    else:
        next_to = request.GET.get('next', '/')
        context['next_to'] = next_to
    return render(request, 'account/login.html', context)


# 登出
def logout_view(request):
    # 清理cookie里保存username
    next_to = request.GET.get('next', '/')
    if next_to == '':
        next_to = '/'
    auth.logout(request)
    return redirect(next_to)