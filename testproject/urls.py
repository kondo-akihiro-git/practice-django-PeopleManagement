"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

役割：ルーター

"""
from django.contrib import admin
from django.urls import path
from testapp.views import frontpage, user_detail, user_add, delete_info, bookmark, user_fav, login_user, registation_user, Logout,ItemListScroll
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path("", login_user, name = "login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('item_list_scroll/', ItemListScroll.as_view(), name="item_list_scroll"),
    path("registration/", registation_user, name = "registration"),
    path("frontpage/", frontpage, name = "frontpage"),
    path('user_add/', user_add, name = "user_add"),
    path('delete_info/', delete_info, name = "delete_info"),
    path('bookmark/', bookmark, name = "bookmark"),
    path('user_fav/', user_fav, name = "user_fav"),
    path("<slug:slug>/", user_detail, name = "user_detail")
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
