from django.shortcuts import render, redirect
from testapp.forms import UserForm, UserForm_add
from .models import UserInfo
import pykakasi
import requests

# Create your views here.
import pprint

global currentSlug
currentSlug = ""


def frontpage(request):
    userinfo = UserInfo.objects.all()
    return render(request, "testapp/frontpage.html", {"userinfo": userinfo})


def user_add(request):
    userinfo = UserInfo.objects.all()
    if request.method == "POST":
        form = UserForm_add(request.POST)
        print(form.errors)
        if form.is_valid():
            input_info = form.save(commit=False)
            input_info.slug = convertLanguage(request.POST.get("user_name"))
            input_info.save()
            print("新規登録処理完了")

        return redirect("user_add")
    else:
        form = UserForm_add()
    return render(
        request, "testapp/user_add.html", {"userinfo": userinfo, "form": form}
    )


def user_detail(request, slug):
    print("Update処理開始")
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
    print("delete処理開始")

    UserInfo.objects.filter(slug=currentSlug).delete()

    userinfo = UserInfo.objects.all()
    return render(request, "testapp/frontpage.html", {"userinfo": userinfo})


def bookmark(request):

    # session = requests.Session()
    # responce = session.get('http://localhost:8000')
    # print(session.cookies)
    slug = request.COOKIES.get("slug", 0)
    check = request.COOKIES.get("check", 0)

    userdetail = UserInfo.objects.get(slug=slug)

    print(userdetail.test_flg)

    print(check)

    if check == "true":
        userdetail.test_flg = True
        print(1)
        userdetail.save()
    elif check == "false":
        print(2)
        userdetail.test_flg = False
        userdetail.save()

    print("Finish")

    userinfo = UserInfo.objects.all()
    return render(request, "testapp/frontpage.html", {"userinfo": userinfo})

def user_fav(request):
    userinfo = UserInfo.objects.all()
    return render(request, "testapp/user_fav.html", {"userinfo": userinfo})
