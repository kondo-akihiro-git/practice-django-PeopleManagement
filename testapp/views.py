from django.shortcuts import render

from .models import UserInfo
# Create your views here.

def frontpage(request):
    userinfo = UserInfo.objects.all()
    return render(request, "testapp/frontpage.html", {"userinfo":userinfo})

def user_detail(request, slug):
    userdetail = UserInfo.objects.get(slug=slug)
    return render(request, "testapp/user_detail.html", {"userdetail":userdetail})