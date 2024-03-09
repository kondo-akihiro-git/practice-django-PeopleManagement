from django.shortcuts import render, redirect
from testapp.forms import UserForm, UserForm_add, LoginForm
from .models import UserInfo
import pykakasi
import requests
from selenium import webdriver
from selenium.webdriver.chrome import service
from django.contrib.auth.views import LogoutView

import django.http
import testapp.models
import testapp.forms
from django.shortcuts import render
import uuid
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login as django_login

from django.contrib import messages

# Create your views here.
import pprint

global currentSlug
currentSlug = ""


def frontpage(request):
    if not request.user.is_authenticated:
        return render(request, "testapp/login.html")

    userinfo = UserInfo.objects.all()
    return render(request, "testapp/frontpage.html", {"userinfo": userinfo})


def user_add(request):
    if not request.user.is_authenticated:
        return render(request, "testapp/login.html")

    userinfo = UserInfo.objects.all()
    if request.method == "POST":
        # /form = UserForm_add(request.POST)
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            print("request.POST.get(picture)")
            print(request.FILES["picture"])
            print("request.POST.get(user_name)")
            print(request.POST.get("user_name"))

            input_info = form.save(commit=False)
            input_info.slug = convertLanguage(request.POST.get("user_name"))
            if request.FILES.get("picture") is not None:
                input_info.picture = request.FILES["picture"]
            input_info.save()
            print("新規登録処理完了")

        return redirect("user_add")
    else:
        form = UserForm_add()
    return render(
        request, "testapp/user_add.html", {"userinfo": userinfo, "form": form}
    )


def user_detail(request, slug):
    print("---reached to user_detail---")

    if not request.user.is_authenticated:
        return render(request, "testapp/login.html")

    userdetail = UserInfo.objects.get(slug=slug)

    global currentSlug
    currentSlug = slug

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            userdetail.user_name = request.POST.get("user_name")
            userdetail.company_name = request.POST.get("company_name")
            userdetail.mail_address = request.POST.get("mail_address")
            userdetail.password = request.POST.get("password")
            userdetail.test_empty = request.POST.get("test_empty")

            if request.FILES.get("picture") is not None:
                userdetail.picture = request.FILES.get("picture")
            userdetail.save()
            print("Update処理完了")

            return redirect("user_detail", slug=userdetail.slug)

        else:
            form = UserForm()
    else:
        form = UserForm()

    return render(
        request, "testapp/user_detail.html", {"userdetail": userdetail, "form": form}
    )


def convertLanguage(str):
    kakasi = pykakasi.kakasi()  # インスタンスの作成
    result = kakasi.convert(str)
    str = "".join([item["hepburn"] for item in result])
    return str


def delete_info(request):
    print("---reached to delete_info---")

    if not request.user.is_authenticated:
        return render(request, "testapp/login.html")

    UserInfo.objects.filter(slug=currentSlug).delete()

    userinfo = UserInfo.objects.all()
    return render(request, "testapp/frontpage.html", {"userinfo": userinfo})


def bookmark(request):
    if not request.user.is_authenticated:
        return render(request, "testapp/login.html")

    slug = request.COOKIES.get("slug", 0)
    check = request.COOKIES.get("check", 0)

    print("def slug=" + slug)
    print("def check=" + check)

    userdetail = UserInfo.objects.get(slug=slug)

    if check == "true":
        userdetail.test_flg = True
        print("true判定")
        userdetail.save()
    elif check == "false":
        print("false判定")
        userdetail.test_flg = False
        userdetail.save()

    userinfo = UserInfo.objects.all()

    return render(request, "testapp/frontpage.html", {"userinfo": userinfo})


def user_fav(request):
    favuser = []
    userinfo = UserInfo.objects.all()
    for info in userinfo:
        if info.test_flg == True:
            favuser.append(info)

    return render(request, "testapp/user_fav.html", {"favuser": favuser})


# ----------ログイン----------


def has_digit(text):
    if re.search("\d", text):
        return True
    return False


def has_alphabet(text):
    if re.search("[a-zA-Z]", text):
        return True
    return False


# def post_new_post(request):
#     if request.method == 'POST':
#         form = testapp.forms.InputForm(request.POST)
#         if form.is_valid():
#             testapp.models.Post.objects.create(name=request.POST['name'], age=request.POST['age'], comment=request.POST['comment'])
#             return django.http.HttpResponseRedirect('/list')
#     else:
#         form = testapp.forms.InputForm()
#     return render(request, 'testapp/post_new_post.html', {'form': form})

# def list(request):
#     posts = testapp.models.Post.objects.all()
#     return render(request, 'testapp/list.html', {'posts': posts})


def login_user(request):
    # messages.info(request, 'まだ企業情報が登録されていません。')
    print(6)
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        print(request.POST.get("username"))

        username = request.POST.get("username")
        password = request.POST.get("password")
        print(5)
        user = authenticate(request, username=username, password=password)
        print(4)
        if user is not None:
            django_login(request, user)
            print(3)
            return django.http.HttpResponseRedirect("/frontpage")
        else:
            login_form.add_error(None, "ユーザー名またはパスワードが異なります。")
            return render(request, "testapp/login.html", {"login_form": login_form})

    else:
        login_form = testapp.forms.LoginForm()
        print(2)
    print(1)
    return render(request, "testapp/login.html", {"login_form": login_form})
    # アカウントとパスワードが合致したら、その人専用の投稿画面に遷移する
    # アカウントとパスワードが合致しなかったら、エラーメッセージ付きのログイン画面に遷移する


def registation_user(request):
    if request.method == "POST":
        registration_form = testapp.forms.RegistrationForm(request.POST)
        password = request.POST["password"]
        if len(password) < 8:
            registration_form.add_error("password", "文字数が8文字未満です。")
        if not has_digit(password):
            registration_form.add_error("password", "数字が含まれていません")
        if not has_alphabet(password):
            registration_form.add_error("password", "アルファベットが含まれていません")
        if registration_form.has_error("password"):
            return render(
                request,
                "testapp/registration.html",
                {"registration_form": registration_form},
            )
        user = User.objects.create_user(
            username=request.POST["username"],
            password=password,
            email=request.POST["email"],
        )

        login_form = LoginForm(request.POST)
        return render(request, "testapp/login.html", {"login_form": login_form})

    else:
        registration_form = testapp.forms.RegistrationForm()

    return render(
        request, "testapp/registration.html", {"registration_form": registration_form}
    )


# ログアウト機能の処理
class Logout(LogoutView):
    template_name = "testapp/logout.html"
