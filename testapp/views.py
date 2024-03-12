from django.shortcuts import render, redirect
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.views import LogoutView
import django.http
import pykakasi
import testapp.models
import testapp.forms
from .models import UserInfo
from testapp.forms import UserForm,LoginForm
from django.views import generic
from django.contrib import messages

global currentSlug
currentSlug = ""


def frontpage(request):
    if not request.user.is_authenticated:
        return render(request, "testapp/login.html")
    
    

    userinfo = UserInfo.objects.all()
    paginator = Paginator(userinfo, 3)
    p = request.GET.get('p') 
    articles = paginator.get_page(p) 
    return render(request, "testapp/frontpage.html", {"userinfo": userinfo,"articles": articles})


class ItemListScroll(generic.ListView):
    model = UserInfo
    template_name = 'testapp/item_list_scroll.html'
    paginate_by = 3

    def get_queryset(self):
        return self.model.objects.all()

def user_add(request):
    if not request.user.is_authenticated:
        return render(request, "testapp/login.html")
    userinfo = UserInfo.objects.all()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            input_info = form.save(commit=False)
            input_info.slug = convertLanguage(request.POST.get("user_name"))
            if request.FILES.get("picture") is not None:
                input_info.picture = request.FILES["picture"]
            input_info.save()
            messages.success(request, 'ユーザー追加完了！')
        return redirect("user_add")
    else:
        form = UserForm()
    return render(
        request, "testapp/user_add.html", {"userinfo": userinfo, "form": form}
    )


def user_detail(request, slug):
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
    if not request.user.is_authenticated:
        return render(request, "testapp/login.html")
    UserInfo.objects.filter(slug=currentSlug).delete()
    userinfo = UserInfo.objects.all()
    articles = getArticles(request)
    return render(request, "testapp/frontpage.html", {"userinfo": userinfo,"articles": articles})

def bookmark(request):
    if not request.user.is_authenticated:
        return render(request, "testapp/login.html")
    slug = request.COOKIES.get("slug", 0)
    check = request.COOKIES.get("check", 0)
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
    articles = getArticles(request)
    currentPage = request.COOKIES.get("page", 0)
    if currentPage == "frontpage":
        return render(request, "testapp/"+currentPage+".html", {"userinfo": userinfo,"articles": articles})
    elif currentPage == "user_fav":
        return django.http.HttpResponseRedirect("/user_fav")

def getArticles(request):
    userinfo = UserInfo.objects.all()
    paginator = Paginator(userinfo, 3)
    p = request.GET.get('p') 
    articles = paginator.get_page(p) 
    return articles


def user_fav(request):
    favuser = []
    userinfo = UserInfo.objects.all()
    for info in userinfo:
        if info.test_flg == True:
            favuser.append(info)
    return render(request, "testapp/user_fav.html", {"favuser": favuser})

def has_digit(text):
    if re.search("\d", text):
        return True
    return False

def has_alphabet(text):
    if re.search("[a-zA-Z]", text):
        return True
    return False

def login_user(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)



            return django.http.HttpResponseRedirect("/frontpage")
        else:
            login_form.add_error(None, "ユーザー名またはパスワードが異なります。")
            return render(request, "testapp/login.html", {"login_form": login_form})
    else:
        login_form = testapp.forms.LoginForm()
    return render(request, "testapp/login.html", {"login_form": login_form})


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
            registration_form.add_error("password", "パスワードが適切ではありません")
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
        return django.http.HttpResponseRedirect("/")
    else:
        registration_form = testapp.forms.RegistrationForm()
    return render(
        request, "testapp/registration.html", {"registration_form": registration_form}
    )

# ログアウト機能の処理
class Logout(LogoutView):
    template_name = "testapp/logout.html"