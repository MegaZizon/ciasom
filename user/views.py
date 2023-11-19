from django.shortcuts import render,redirect,HttpResponse
from .models import *
from random import *
from .sendmail import send
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    content={}

    if not request.session.get('user_id'):
        return render(request,'index.html',content)
    else:
        user_id=request.session.get('user_id')
        user=User.objects.get(user_id=user_id)
        content = {"user":user}
        return render(request,'choice.html',content)
    
def streamerSet(request):

    if not request.session.get('user_id'):
        return redirect('logout')
    else:
        user_id=request.session.get('user_id')
        user=User.objects.get(user_id=user_id)
        content = {"user":user}
        return render(request,'streamer_main.html',content)
    
def faceUpload(request):
    if not request.session.get('user_id'):
        return redirect('logout')
    else:
        user_id=request.session.get('user_id')
        user=User.objects.get(user_id=user_id)
        content = {"user":user}
        return render(request,'face_up.html',content)

def facelist(request):
    if not request.session.get('user_id'):
        return redirect('logout')
    user_id=request.session.get('user_id')
    model=User_model.objects.filter(user_id=user_id).order_by('-time')
    user=User.objects.get(user_id=user_id)
    content={"model":model}
    content['user']=user
    return render(request,'face_list.html',content)
    
def login(request):
    if request.method == "POST":
        loginId = request.POST['loginId']
        loginPW = request.POST['loginPW']
        content={}
        try:
            user = User.objects.get(user_id = loginId)
            if user.user_password == loginPW:
                id=user.user_id+"님 환영합니다."
                request.session['user_id'] = user.user_id
                return redirect('main')
            else:
                content['error']='비밀번호가 틀립니다.'
                return render(request,'index.html',content)
        except:
            content['error']='아이디를 찾을 수 없습니다.'
            return render(request,'index.html',content)
    else:
        return render(request,'index.html')
    
# def signup(request):
#     content={}
#     if request.session.get('error'):
#         content=request.session.get('error')
#         del request.session['error']
#         if(content=="id"):
#             content={"error":"이미 사용중인 아이디 입니다."}
#         elif(content=="email"):
#             content={"error":"이미 사용중인 이메일 입니다."}
#         elif(content=="nickname"):
#             content={"error":"이미 사용중인 닉네임 입니다."}
#         return render(request,'index.html',content)
    
#     return render(request,'choice.html')



def signup(request):
    if request.method == "POST":
        id = request.POST['signupId']
        email = request.POST['signupEmail']
        pw = request.POST['signupPW']
        nickname = request.POST['signupNickname']
        content={}

        if User.objects.filter(user_id = id).exists():
            content={"error":"이미 사용중인 아이디 입니다."}
            return render(request,'index.html',content)
        if User.objects.filter(user_email = email).exists():
            content={"error":"이미 사용중인 이메일 입니다."}
            return render(request,'index.html',content)
        if User.objects.filter(user_nickname = nickname).exists():
            content={"error":"이미 사용중인 닉네임 입니다."}
            return render(request,'index.html',content)
        
        # try:
        #     img = request.FILES['signupImg']
        #     try:
        #         user = User(user_id=id,user_email=email,user_password=pw,user_nickname=nickname,user_img=img)
        #         user.save()
        #     except:
        #         content['error']='데이터베이스에 등록하던 중 알 수 없는 오류가 발생하였습니다.'
        #         return render(request,'index.html',content)
        # except:
        #     try:
        #         user = User(user_id=id,user_email=email,user_password=pw,user_nickname=nickname)
        #         user.save()
        #     except:
        #         content['error']='데이터베이스에 등록하던 중 알 수 없는 오류가 발생하였습니다.'
        #         return render(request,'index.html',content)
        user = User(user_id=id,user_email=email,user_password=pw,user_nickname=nickname)
        user.save() 

        if 'noEmail' in request.POST:
            user=User.objects.get(user_id = id)
            user.user_validate = 1
            user.save()
            response = redirect('main')
            request.session['user_id'] = user.user_id
            return response

        # code=randint(1000,9999)
        # response = redirect('verify')
        # response.set_cookie('code',code)
        # response.set_cookie('user_id',user.user_id)
        # send_result = send(email,code)
        # if send_result:
        #     return response
        # else:
        #     return HttpResponse("서버에서 이메일 전송실패.")


def verify(request):
    return render(request, 'sendEmail/verifyCode.html')

def verifySubmit(request):
    user_code = request.POST['verifyCode']
    cookie_code = request.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(user_id = request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('main')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        # response.set_cookie('user',user)
        request.session['user_id'] = user.user_id
        return response
    else:
        return redirect('verify')
    
def logout(request):
    try:
        del request.session['user_id']
    except:
        pass
    return redirect('main')

def mypage(request):
    if request.session.get('error'):
        content=request.session.get('error')
        del request.session['error']
        if(content=="id"):
            content={"error":"이미 사용중인 아이디 입니다."}
        elif(content=="email"):
            content={"error":"이미 사용중인 이메일 입니다."}
        elif(content=="nickname"):
            content={"error":"이미 사용중인 닉네임 입니다."}
        user_id=request.session['user_id']
        user=User.objects.get(user_id=user_id)
        content["user"] = user
        return render(request,'mypage.html',content)
    
    if not request.session.get('user_id'):
        return redirect('logout')
    
    user_id=request.session['user_id']
    user=User.objects.get(user_id=user_id)
    content = {"user":user}
    
    return render(request,'mypage.html',content)

def changeInfo(request):
    if not request.session.get('user_id'):
        return redirect('logout')
    
    user_id=request.session.get('user_id')

    if 'changeEmail' in request.POST:
        user=User.objects.get(user_id=user_id)

        if User.objects.filter(user_email = request.POST['changeEmail']).exists():
            request.session['error']="email"
            return redirect('mypage')
        
        user.user_email=request.POST['changeEmail']
        user.save()
        return redirect('mypage')
    elif 'changePW' in request.POST:
        user=User.objects.get(user_id=user_id)
        user.user_password=request.POST['changePW']
        user.save()
        return redirect('mypage')
    elif 'changeNickname' in request.POST:
        user=User.objects.get(user_id=user_id)

        if User.objects.filter(user_nickname = request.POST['changeNickname']).exists():
            request.session['error']="nickname"
            return redirect('mypage')

        user.user_nickname=request.POST['changeNickname']
        user.save()
        return redirect('mypage')
    elif 'changeImg' in request.FILES:
        user=User.objects.get(user_id=user_id)
        user.user_img=request.FILES['changeImg']
        user.save()
        return redirect('mypage')
    elif 'out' in request.POST:
        user=User.objects.get(user_id=user_id)
        user.delete()  
        return redirect('logout')
    
def register(request):
    if not request.session.get('user_id'):
        return redirect('logout')
    user_id=request.session.get('user_id')
    user=User.objects.get(user_id=user_id)
    content = {"user":user}
    
    regist_img=User_register.objects.filter(user_id=user_id).order_by('-time')
    
    if not User_register.objects.filter(user_id = user_id).exists():
        content["noImg"]="noImg"
    page = request.GET.get('page')
    paginator = Paginator(regist_img, 3)
    try:
        page_obj = paginator.page(page)
        content["page_obj"]=page_obj
        content["paginator"]=paginator
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
        content["page_obj"]=page_obj
        content["paginator"]=paginator
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
        content["page_obj"]=page_obj
        content["paginator"]=paginator

    leftIndex = (int(page) - 2)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 2)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages 

    custom_range = range(leftIndex, rightIndex+1)
    content["custom_range"]=custom_range
    model=User_model.objects.filter(user_id=user_id).order_by('-time')
    content["model"]=model

    return render(request, 'register.html',content)

def registImg(request):
    if not request.session.get('user_id'):
        return redirect('logout')
    user_id=request.session.get('user_id')
    if request.method == 'POST':
        received_data = request.POST['modelName']
        if User_model.objects.filter(model_name = received_data).exists():
            return JsonResponse({'message': '이미 사용중인 모델명입니다.'})
        uploaded_files = request.FILES.getlist('image[]')
        # 각 파일을 처리하거나 저장할 수 있습니다.
        for file in uploaded_files:
            # 여기서 파일을 원하는 대로 처리합니다.
            user_instance = User.objects.get(user_id=user_id)
            user = User_register(parent=user_instance,user_id=user_instance.user_id,user_img=file)
            
            user.save()
         
        deepStr=deeplearn(user_id,received_data)
        registImg=User_register.objects.filter(user_id=user_id)
        for regImg in registImg:
            regImg.delete()  
        return JsonResponse({'message': 'Files uploaded successfully.'})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

# def registImg(request):
#     if not request.session.get('user_id'):
#         return redirect('logout')
#     user_id=request.session.get('user_id')
#     print(user_id)
#     if 'userImg' in request.FILES:
#         img = request.FILES['userImg']
#         user_instance = User.objects.get(user_id=user_id)
#         user = User_register(parent=user_instance,user_id=user_instance.user_id,user_img=img)
#         user.save()

#     return redirect('register')

def regDel(request,post_id):
    registImg=User_register.objects.get(id=post_id)
    registImg.delete()  
    return redirect('register')

def modelDel(request,model_id):
    registImg=User_model.objects.get(id=model_id)
    registImg.delete()  
    print(model_id)
    return redirect('facelist')

from django.conf import settings
import os
from os import listdir
from PIL import Image
from numpy import asarray
from numpy import expand_dims
import pickle
import cv2
from keras_facenet import FaceNet
import numpy as np
from io import BytesIO
from base64 import b64decode
from django.core.files import File
from django.http import JsonResponse 
MyFaceNet = FaceNet()
HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'))
def deeplearn(user_id,received_data):
    
    print(received_data)
    user=User_register.objects.filter(user_id = user_id)
    
    #print(user)
    #folder=os.path.join(settings.MEDIA_ROOT,"user_data","user_"+user_id)
    #print(folder)

    database = {}
    for photo in user:

        gbr1 = cv2.imread(photo.user_img.path)
        print(photo.user_img.path)
        print(photo.user_img.url)

        wajah = HaarCascade.detectMultiScale(gbr1,1.1,4)

        if len(wajah)>0:
            x1, y1, width, height = wajah[0]
        else:
            x1, y1, width, height = 1, 1, 10, 10

        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        gbr = Image.fromarray(gbr)                  # konversi dari OpenCV ke PIL
        gbr_array = asarray(gbr)

        face = gbr_array[y1:y2, x1:x2]

        face = Image.fromarray(face)
        face = face.resize((160,160))
        face = asarray(face)


        face = expand_dims(face, axis=0)
        signature = MyFaceNet.embeddings(face)

        database[os.path.splitext(photo.user_img.name)[0]]=signature

    model_file=(os.path.join(settings.MEDIA_ROOT,"user_model",user_id+".pkl"))

    myfile = open(model_file, "wb")
    pickle.dump(database, myfile)
    myfile.close()
    
    with open(model_file, 'rb') as file:
        myfile2 = File(file)
        user_instance = User.objects.get(user_id=user_id)
        user_model=User_model(parent=user_instance,user_id=user_instance.user_id,model_name=received_data)
        user_model.user_model.save(user_id+'.pkl',myfile2)

        # user_instance=LiveRoom.objects.get(host_id="1")
        # liveroom_model=LiveRoom_img(parent=user_instance,host_id=user_instance.host_id)
        # print("3")
        # liveroom_model.video_img.save(user_id+'.pkl2',myfile2)
    user_model.save()
    os.remove(model_file)

    return "sucessed"

