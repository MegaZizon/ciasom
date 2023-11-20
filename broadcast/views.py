from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
import uuid
import cv2
import asyncio
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
import json
from av import VideoFrame
from django.http import JsonResponse 
from user.models import LiveRoom
from user.models import User_model
from user.models import User
from user.models import LiveRoom_img
from django.urls import reverse
from django.forms.models import model_to_dict
# Create your views here.

pcs = set()
dicPcV = []
dicPcA = []
tdicPcV = []
tdicPcA = []
dictPc = {}

def onair(request):
    # content={"host_id":host_id}
    
    # model=User_model.objects.filter(user_id = host_id)
    # content["model"]=model
    # return render(request, 'onair.html',content)
    if not request.session.get('user_id'):
        other_app_url = reverse('user:logout')
        return redirect(other_app_url)
    user_id=request.session.get('user_id')
    user=User.objects.get(user_id=user_id)
    content={"host_id":user_id}
    content['user']=user
    
    model=User_model.objects.filter(user_id = user_id)
    content["model"]=model
    print(content)
    return render(request, 'setting.html',content)


def broadcast(request,host_id):
    if not request.session.get('user_id'):
        other_app_url = reverse('user:logout')
        return redirect(other_app_url)
    user_id = request.session.get('user_id')
    user=User.objects.get(user_id=user_id)
    content={}
    content['user']=user
    liveroom = LiveRoom.objects.get(host_id=host_id)
    print(liveroom)
    content['host_id'] = liveroom.host_id
    content['category'] = liveroom.category
    content['head_count'] = liveroom.head_count
    content['title'] = liveroom.title
    return render(request, 'broadcast.html',content)

def searchHost(request,host_id):
    if not request.session.get('user_id'):
        other_app_url = reverse('user:logout')
        return redirect(other_app_url)
    user_id = request.session.get('user_id')
    user=User.objects.get(user_id=user_id)
    content={}
    content['user']=user
    liveroom = LiveRoom.objects.filter(host_id__icontains=host_id)

    broadlist = []

    for lr in liveroom:
        thumbnail = LiveRoom_img.objects.filter(host_id=lr.host_id).order_by('-time').first()
        if thumbnail:
            thumbnail_dict = model_to_dict(thumbnail)  # LiveRoom_img 객체를 딕셔너리로 변환
            thumbnail_dict['title'] = lr.title
            thumbnail_dict['head_count'] = lr.head_count
            thumbnail_dict['category'] = lr.category
            broadlist.append(thumbnail_dict)

    content = {'broadlist': broadlist}
    content['searchHost']=host_id
    print(content)
    return render(request, 'search.html', content)

def searchTitle(request,title):
    if not request.session.get('user_id'):
        other_app_url = reverse('user:logout')
        return redirect(other_app_url)
    user_id = request.session.get('user_id')
    user=User.objects.get(user_id=user_id)
    content={}
    liveroom = LiveRoom.objects.filter(title__icontains=title)

    broadlist = []

    for lr in liveroom:
        thumbnail = LiveRoom_img.objects.filter(host_id=lr.host_id).order_by('-time').first()
        if thumbnail:
            thumbnail_dict = model_to_dict(thumbnail)  # LiveRoom_img 객체를 딕셔너리로 변환
            thumbnail_dict['title'] = lr.title
            thumbnail_dict['head_count'] = lr.head_count
            thumbnail_dict['category'] = lr.category
            broadlist.append(thumbnail_dict)

    content = {'broadlist': broadlist}
    content['searchTitle']=title
    content['user']=user
    print(content)
    return render(request, 'search.html', content)

def broadList(request):
    if not request.session.get('user_id'):
        other_app_url = reverse('user:logout')
        return redirect(other_app_url)
    user_id = request.session.get('user_id')
    user=User.objects.get(user_id=user_id)
    content={}
    liveroom = LiveRoom.objects.all().order_by('-head_count')

    broadlist = []

    for lr in liveroom:
        thumbnail = LiveRoom_img.objects.filter(host_id=lr.host_id).order_by('-time').first()
        if thumbnail:
            thumbnail_dict = model_to_dict(thumbnail)  # LiveRoom_img 객체를 딕셔너리로 변환
            thumbnail_dict['title'] = lr.title
            thumbnail_dict['head_count'] = lr.head_count
            thumbnail_dict['category'] = lr.category
            broadlist.append(thumbnail_dict)

    content = {'broadlist': broadlist}
    content['user']=user
    print(content)
    return render(request, 'viewer_main.html', content)

async def quitbroadcast(request,host_id):
    await delete_live_object(host_id)
    await delete_live_object_array(host_id)

    return JsonResponse({'del':"del"})

def test(request):
    print("dicPcA",dicPcA)
    print("dicPcV",dicPcV)
    print("tdicPcA",tdicPcA)
    print("tdicPcV",tdicPcV)
    print("dictPc",dictPc)

    for i in dictPc:
        temp=dictPc[i]
        print("dictPc :",i," 방에 접속중인 Client LIST:",temp.get_pc())
   
   
    return HttpResponse("테스트.")


async def start(request):
    database={}
    params2 = (request.body).decode("utf-8")
    params = json.loads(params2)
    local_audio=None
    local_video=None
    useModel=await userModel(params["model"])
    if(useModel != None):
        print("in ontrack",useModel.user_model.path)
        myfile = open(useModel.user_model.path,"rb")
        database =  pickle.load(myfile)
        myfile.close()

    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState == "failed" or pc.connectionState == 'disconnected' or pc.connectionState == 'closed':
            if pc.connectionState == "closed":
                #await delete_live_object(params["streamid"])

                if params["streamid"] in dictPc:
                    peerclass = dictPc[params["streamid"]]
                    peer=peerclass.get_pc()
                    
                    print("HOST 연결종료(해제된 연결목록:) :",peer)
                    for i in peer:
                        await i.close()
                    j=0
                    for i in dicPcA:
                        if(i==params["streamid"]):
                            dicPcA.pop(j)
                            dicPcA.pop(j)
                            dicPcV.pop(j)
                            dicPcV.pop(j)
                        j=j+1

                    del dictPc[params["streamid"]]
                    print("HOST 연결종료: ",pc)
            await pc.close()
        elif pc.connectionState == "connected":
            
            try:
                # 오류 무조건 발생하는 부분
                await create_live_object(params["streamid"],params["title"],params["category"],0)
                await asyncio.sleep(1)
                for i in range(len(tdicPcA)):
                    if tdicPcA[i] == params["streamid"]:
                        dicPcA.append(params["streamid"])
                        dicPcA.append(tdicPcA[i+1])
                        dicPcV.append(params["streamid"])
                        dicPcV.append(tdicPcV[i+1])
                        tdicPcA.pop(0)
                        tdicPcA.pop(0)
                        tdicPcV.pop(0)
                        tdicPcV.pop(0)
            except:
                pass

    @pc.on("track")
    def on_track(track):
        if track.kind == "audio":
            pc.addTrack(track)
            local_audio=track
            tdicPcA.append(params["streamid"])
            tdicPcA.append(local_audio)

        if track.kind == "video":

            

            local_video = VideoTransformTrack(
                track,   model=params["model"],database=database,user_id=params["streamid"]
            )
            
            
            pc.addTrack(local_video)
            tdicPcV.append(params["streamid"])
            tdicPcV.append(local_video)
                
    dictPc[params["streamid"]]=PcStorage()

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    print("HOST 연결초기단계 실행중: ",pc)
    

    return JsonResponse({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})



async def watch(request):
    params2 = (request.body).decode("utf-8")
    params = json.loads(params2)
        
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()


    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState == "failed" or pc.connectionState == 'disconnected' or pc.connectionState == 'closed':
            
            if pc.connectionState == "closed":
                await out_live_object(params["streamid"])
                if params["streamid"] in dictPc:
                    peerclass = dictPc[params["streamid"]]
                    peer=peerclass.get_pc()
                    i=0
                    for p in peer:
                        if(p==pc):
                            peerclass.pop_pc(i)
                            print("클래스에서 Client Index제거 disconnect: ",p)
                        i=i+1
                print("disconnected Client: ",pc)
            else:
                await pc.close()
        elif pc.connectionState == "connected":
            try:
                temp=await join_live_object(params["streamid"])
                if(temp):
                    print("방에 입장할 수 없습니다.")
                    await pc.close()
                if params["streamid"] in dictPc:
                    peerclass = dictPc[params["streamid"]]
                    peerclass.append_pc(pc)
                    print("클라이언트 연결됨:Connect",peerclass.get_pc())
            except:
                pass

    
    
    for i in range(len(dicPcA)):
        if(dicPcA[i]==params["streamid"]):
            pc.addTrack(dicPcA[i+1])
            pc.addTrack(dicPcV[i+1])
   
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)


    return JsonResponse({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})


from keras_facenet import FaceNet
from PIL import Image
from numpy import asarray
import numpy as np
import os
import pickle
from numpy import expand_dims
from django.conf import settings
import time
from django.core.files import File
#myfile = open("data.pkl", "rb")
#modelUrl = os.path.join(settings.MEDIA_ROOT, "haarcascade_frontalface_default.xml") 
HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'))
#MyFaceNet = FaceNet()
#database =  pickle.load(myfile)
#######################################################

from . import utils
import mediapipe as mp


class VideoTransformTrack(MediaStreamTrack):

    kind = "video"

    def __init__(self, track, model,database={},user_id="None"):
        super().__init__()  # don't forget this!
        self.track = track
        self.model = model
        self.database = database
        self.MyFaceNet = FaceNet()

        self.last_save_time = time.time()
        self.save_interval = 10  # 10초 간격으로 저장
        self.frame_count = 0
        self.user_id = user_id
        
        mp_face_detection = mp.solutions.face_detection
        self.face_detector=mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5
        )
    async def recv(self):
        frame = await self.track.recv()
        if self.model=="noModel":

            gbr3 = frame.to_ndarray(format="bgr24")

            current_time = time.time()
            if current_time - self.last_save_time >= self.save_interval:
                self.last_save_time = current_time
                self.frame_count += 1
                filename = f"temp_{self.user_id}_{self.frame_count}.jpg"
                save_path = os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id,filename)
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id)):
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id))

                self.save_frame_locally(gbr3, save_path)
                await save_frame_to_model(save_path,self.user_id,self.frame_count)

            new_frame = VideoFrame.from_ndarray(gbr3, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base

            return new_frame

            
        # if self.model!="noModel":
            
            
        #     gbr1 = frame.to_ndarray(format="bgr24")

        #     #wajah 얼굴
        #     #kao 얼굴
        #     wajah = HaarCascade.detectMultiScale(gbr1,1.1,4)

        #     if len(wajah)>0:
        #         x1, y1, width, height = wajah[0]
        #     else:
        #         x1, y1, width, height = 1, 1, 10, 10

        #     x1, y1 = abs(x1), abs(y1)
        #     x2, y2 = x1 + width, y1 + height


        #     gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        #     gbr = Image.fromarray(gbr)                  # konversi dari OpenCV ke PIL
        #     gbr_array = asarray(gbr)

        #     face = gbr_array[y1:y2, x1:x2]

        #     face = Image.fromarray(face)
        #     face = face.resize((160,160))
        #     face = asarray(face)


        #     face = expand_dims(face, axis=0)
        #     signature = self.MyFaceNet.embeddings(face)

        #     min_dist=100
        #     identity=' '
        #     for key, value in self.database.items() :
        #         dist = np.linalg.norm(value-signature)
        #         if dist < min_dist:
        #             min_dist = dist
        #             identity = key

        #     if identity != " ":
        #         mosaic_face = cv2.resize(gbr1[y1:y2, x1:x2], (width // 10, height // 10))
        #         mosaic_face = cv2.resize(mosaic_face, (width, height), interpolation=cv2.INTER_NEAREST)
        #         gbr1[y1:y2, x1:x2] = mosaic_face


        #     # cv2.putText(gbr1,identity, (100,100),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        #     # cv2.rectangle(gbr1,(x1,y1),(x2,y2), (0,255,0), 2)

        #     current_time = time.time()
        #     if current_time - self.last_save_time >= self.save_interval:
        #         self.last_save_time = current_time
        #         self.frame_count += 1
        #         filename = f"temp_{self.user_id}_{self.frame_count}.jpg"
        #         save_path = os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id,filename)
        #         if not os.path.exists(os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id)):
        #             os.makedirs(os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id))

        #         self.save_frame_locally(gbr1, save_path)
        #         await save_frame_to_model(save_path,self.user_id,self.frame_count)

        #     new_frame = VideoFrame.from_ndarray(gbr1, format="bgr24")
        #     new_frame.pts = frame.pts
        #     new_frame.time_base = frame.time_base

        #     return new_frame
        
        elif self.model=="allMosaic":
            fonts = cv2.FONT_HERSHEY_PLAIN
            
            # print('first')

            gbr2 = frame.to_ndarray(format="bgr24")
            rgb_frame = cv2.cvtColor(gbr2, cv2.COLOR_BGR2RGB)


            #results = ((mp.solutions.face_detection).FaceDetection(model_selection=1, min_detection_confidence=0.5)).process(rgb_frame)
            results = self.face_detector.process(rgb_frame)

            frame_height, frame_width, c = gbr2.shape
            if results.detections:
                for face in results.detections:
                    face_react = np.multiply(
                        [
                            face.location_data.relative_bounding_box.xmin,
                            face.location_data.relative_bounding_box.ymin,
                            face.location_data.relative_bounding_box.width,
                            face.location_data.relative_bounding_box.height,
                        ],
                        [frame_width, frame_height, frame_width, frame_height],
                    ).astype(int)
                    # print(face_react)
                    x, y, w, h = face_react
            #         # face_roi = frame[y : y + h, x : x + w]
                    padding = 50
                    fx_min = x - padding
                    fx_max = x + padding + w

                    fy_min = y - padding
                    fy_max = y + padding + h
                    if fx_min <= 0:
                        fx_min = 0
                    if fy_min <= 0:
                        fy_min = 0
                    face_roi = gbr2[fy_min:fy_max, fx_min:fx_max]
                    face_blur_roi = cv2.blur(face_roi, (53, 53))
            #         # print(
            #         #     "face roi shape",
            #         #     face_roi.shape,
            #         #     "face_blurred shape",
            #         #     face_blur_roi.shape,
            #         # )
            #         # frame[y : y + h, x : x + w] = face_blur_roi
                    gbr2[fy_min:fy_max, fx_min:fx_max] = face_blur_roi

                    
            #         print('middle')

                    

            # print('last')

            current_time = time.time()
            if current_time - self.last_save_time >= self.save_interval:
                self.last_save_time = current_time
                self.frame_count += 1
                filename = f"temp_{self.user_id}_{self.frame_count}.jpg"
                save_path = os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id,filename)
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id)):
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id))

                self.save_frame_locally(gbr2, save_path)
                await save_frame_to_model(save_path,self.user_id,self.frame_count)

            new_frame = VideoFrame.from_ndarray(gbr2, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base


            return new_frame
        
        else:
            gbr1 = frame.to_ndarray(format="bgr24")


            wajah = HaarCascade.detectMultiScale(gbr1, 1.1, 4)

            for (x1, y1, width, height) in wajah:
                x1, y1 = abs(x1), abs(y1)
                x2, y2 = x1 + width, y1 + height

                gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
                gbr = Image.fromarray(gbr)
                gbr_array = asarray(gbr)

                face = gbr_array[y1:y2, x1:x2]

                face = Image.fromarray(face)
                face = face.resize((160, 160))
                face = asarray(face)

                face = expand_dims(face, axis=0)
                signature = self.MyFaceNet.embeddings(face)

                min_dist = 100
                identity = ' '
                for key, value in self.database.items():
                    dist = np.linalg.norm(value - signature)
                    if dist < min_dist:
                        min_dist = dist
                        identity = key

                unknownStr = f'user_data/user_{self.user_id}/1'
                unknownStr2 = f'user_data/user_{self.user_id}/2'
                if identity == unknownStr or identity == unknownStr2:  # 등록된 얼굴이 아닌 경우 모자이크 처리
                    # 해당 얼굴 영역을 모자이크하기 위해 이미지를 가져와 모자이크 처리
                    face_censored = gbr1[y1:y2, x1:x2]
                    face_censored = cv2.GaussianBlur(face_censored, (99, 99), 30)  # 가우시안 블러를 사용한 모자이크 처리
                    gbr1[y1:y2, x1:x2] = face_censored  # 모자이크 처리된 영역을 원본 이미지에 적용

            current_time = time.time()
            if current_time - self.last_save_time >= self.save_interval:
                self.last_save_time = current_time
                self.frame_count += 1
                filename = f"temp_{self.user_id}_{self.frame_count}.jpg"
                save_path = os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id,filename)
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id)):
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, "liveroom_img","user_"+self.user_id))

                self.save_frame_locally(gbr1, save_path)
                await save_frame_to_model(save_path,self.user_id,self.frame_count)



            new_frame = VideoFrame.from_ndarray(gbr1, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base

            return new_frame

    def save_frame_locally(self, frame, save_path):
        cv2.imwrite(save_path,frame)
        # print(f"Frame saved locally to {save_path}")
        # user_instance = User.objects.get(user_id=user_id)
        # user_model=User_model(parent=user_instance,user_id=user_instance.user_id,model_name=received_data)
        # user_model.user_model.save(user_id+'.pkl',myfile2)


@sync_to_async
def save_frame_to_model(save_path,host_id,frame_count):
    # Django 모델에 이미지 저장
    live = LiveRoom.objects.get(host_id=host_id)
    print("user_instance",live)
    print("user_instance.user_id",live.host_id)
    with open(save_path, 'rb') as file:
        file = File(file)
        liveroom_model=LiveRoom_img(parent=live,host_id=live.host_id)
        live_file_name=live.host_id+"_"+str(frame_count)+'.jpg'
        print(live_file_name)
        liveroom_model.video_img.save(live_file_name,file)
    liveroom_model.save()
    os.remove(save_path)
    print(f"Frame saved to LiveRoom_img model")


@sync_to_async
def userModel(model):
    try:
        user = User_model.objects.get(model_name = model)
        return user
    except:
        return None
    
@sync_to_async
def get_live_object(host_id):
    try:
        live = LiveRoom.objects.get(host_id=host_id)
        return live
    except:
        return None

@sync_to_async
def create_live_object(host_id, title, category, head_count):
    try:
        delete_live_object(host_id)

        print("LiveRoom 오브젝트 생성됨 HOST ID:",host_id)
        live = LiveRoom(host_id=host_id, title=title, category=category, head_count=head_count)
        live.save()
    except:
        pass


@sync_to_async
def create_live_object(host_id, title, category, head_count):
    try:
        print("LiveRoom 오브젝트 생성됨 HOST ID:",host_id)
        live = LiveRoom(host_id=host_id, title=title, category=category, head_count=head_count)
        live.save()
    except:
        pass

@sync_to_async
def delete_live_object(host_id):
    try:
        print("LiveRoom 오브젝트 제거됨 HOST ID:",host_id)
        live = LiveRoom.objects.get(host_id = host_id)
        live.delete()
    except:
        pass
@sync_to_async
def join_live_object(host_id):
    try:
        print("Client 입장 Room HOST ID:",host_id)
        live = LiveRoom.objects.get(host_id = host_id)
        live.head_count = live.head_count+1
        live.save()
    except:
        return "error"

@sync_to_async
def out_live_object(host_id):
    try:
        print("Client 퇴장 Room HOST ID:",host_id)
        live = LiveRoom.objects.get(host_id = host_id)
        if(live.head_count>0):
            live.head_count = live.head_count-1
        live.save()
    except:
        pass
    
@sync_to_async
def delete_live_object_array(host_id):
    print("LiveRoom 오브젝트 제거됨 모든 클라이언트 연결 해제: HOST ID:",host_id)
    if host_id in dictPc:
        peerclass = dictPc[host_id]
        peerclass.del_all()
        print(peerclass)

def test(request):
    print("dicPcA",dicPcA)
    print("dicPcV",dicPcV)
    print("tdicPcA",tdicPcA)
    print("tdicPcV",tdicPcV)
    print("dictPc",dictPc)

    for i in dictPc:
        temp=dictPc[i]
        print("dictPc :",i," 방에 접속중인 Client LIST:",temp.get_pc())
    
    return HttpResponse("테스트.")


class PcStorage:
    def __init__(self):
        self.pc_array = []  

    def append_pc(self, obj):
        self.pc_array.append(obj)

    def pop_pc(self, index=-1):
        if not self.pc_array:
            print("Array is empty.")
            return None
        if index < -len(self.pc_array) or index >= len(self.pc_array):
            print("Invalid index.")
            return None
        return self.pc_array.pop(index)

    def get_pc(self):
        return self.pc_array
    
    def del_all(self): 
        for i in self.pc_array:
            a=i
            print("goodbye",i)

