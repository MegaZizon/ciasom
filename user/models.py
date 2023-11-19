from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.
def user_directory_path(instance, filename):
    return f'user_data/user_{instance.user_id}/{filename}'


def user_model_directory_path(instance, filename):
    return f'user_model/user_{instance.user_id}/{filename}'

def liveroom_img_directory_path(instance, filename):
    return f'liveroom_img/user_{instance.host_id}/{filename}'

class User(models.Model):
    user_id = models.CharField(max_length=20,unique=True,primary_key=True)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=20)
    user_nickname = models.CharField(max_length=20,unique=True)
    user_img = models.FileField(upload_to='user_info/', default='user_info/default_file.jpg')
    user_validate = models.BooleanField(default=False)

class LiveRoom(models.Model):
    host_id = models.CharField(max_length=20,unique=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    head_count = models.IntegerField()
    live_start= models.DateTimeField(default=timezone.now)

class User_register(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20)
    user_img = models.FileField(upload_to=user_directory_path)
    time = models.DateTimeField(default=timezone.now)

class User_model(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20)
    user_model = models.FileField(upload_to=user_model_directory_path)
    time = models.DateTimeField(default=timezone.now)
    model_name = models.CharField(max_length=20,unique=True)

class LiveRoom_img(models.Model):
    parent = models.ForeignKey(LiveRoom, on_delete=models.CASCADE)
    host_id = models.CharField(max_length=20)
    video_img = models.FileField(upload_to=liveroom_img_directory_path)
    time = models.DateTimeField(default=timezone.now)

@receiver(pre_delete, sender=User_register)
def userfile_delete(sender, instance, **kwargs):
    # 파일 시스템에서 파일 삭제
    instance.user_img.delete(False)  # False를 전달하여 파일만 삭제 (데이터베이스 레코드는 삭제하지 않음)

@receiver(pre_delete, sender=User_model)
def usermodel_delete(sender, instance, **kwargs):
    # 파일 시스템에서 파일 삭제
    instance.user_model.delete(False)  # False를 전달하여 파일만 삭제 (데이터베이스 레코드는 삭제하지 않음)

@receiver(pre_delete, sender=LiveRoom_img)
def liveimg_delete(sender, instance, **kwargs):
    # 파일 시스템에서 파일 삭제
    instance.video_img.delete(False)  # False를 전달하여 파일만 삭제 (데이터베이스 레코드는 삭제하지 않음)

# 해당 리시버를 신호와 연결
pre_delete.connect(userfile_delete, sender=User_register)