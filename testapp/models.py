from django.db import models

# Create your models here.


class UserInfo (models.Model):
    # 各フィールド情報を定義
    id = models.AutoField  # 自動採番でidを付与
    company_name = models.CharField(max_length=255, blank=True) 
    user_name = models.CharField(max_length=255, blank=True) 
    mail_address = models.CharField(max_length=255, blank=True) 
    password = models.CharField(max_length=255, blank=True) 
    picture = models.ImageField(upload_to='images/',blank=True, null=True, default='images/default.jpg')
    test_empty = models.CharField(max_length=255, blank=True) 
    test_flg = models.BooleanField(default=False)  # 削除有無
    test_datetime = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    
