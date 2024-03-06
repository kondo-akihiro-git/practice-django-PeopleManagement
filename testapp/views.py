from django.shortcuts import render, redirect
from testapp.forms import UserForm
from .models import UserInfo
import pykakasi
# Create your views here.

def frontpage(request):
    userinfo = UserInfo.objects.all()
    return render(request, "testapp/frontpage.html", {"userinfo":userinfo})

def user_add(request):
    userinfo = UserInfo.objects.all()
    return render(request, "testapp/user_add.html", {"userinfo":userinfo})

def user_detail(request, slug):
    userdetail = UserInfo.objects.get(slug=slug)

    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():

            #userdetail.user_name = request.POST.get("user_name")
            #userdetail.save() 

            input_info = form.save(commit =False)
            input_info.user_detail = user_detail
            input_info.slug =convertLanguage(request.POST.get("user_name"))
            input_info.save()
            
            
            return redirect("user_detail", slug=userdetail.slug)
        
    else:
        form = UserForm()

    return render(request, "testapp/user_detail.html", {"userdetail":userdetail, "form":form})

def convertLanguage(str):
    kakasi = pykakasi.kakasi() # インスタンスの作成
    result = kakasi.convert(str)
    str = ''.join([item['hepburn'] for item in result])
    return str


