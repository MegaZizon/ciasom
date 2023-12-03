# 📺 Ciasom
실시간 등록된 사용자 외 모자이크 웹 플랫폼 

## 🖥️ 프로젝트 소개
사용자에게 사진을 입력받아 입력받은 사진 외의 사용자가 영상에 출연할 경우 모자이크 처리를 진행함
<br>

##  👨‍👨‍👧‍👧 팀 소개
지준오(백엔드(웹)), 전찬수(AI), 최호성(백엔드(앱)), 백지원(프론트엔드)
<br>

### ⚙️ 개발 환경
- `Python 3.11`
- `Django`
- **Library** :  WebRTC, AioRTC, OpenCV, gunicorn, uvicorn
- **Database** : PostgreSQL
- **Environment** : Docker, Nginx


## ❗ 주요 기능
#### 라이브 스트리밍 기능
#### 라이브 스트리밍 시청 기능
#### 실시간 모자이크 기능
#### 사용자의 사진을 입력받아 학습하여 모델을 생성하는 기능
#### 썸네일 표시 기능
<br>

## 🧬 System Architecture

![image](https://github.com/MegaZizon/ciasom/assets/105596059/0aed6443-ecae-414f-ae54-88ca66bc8280)

---

<details><summary><h4> 자세히 </h4></summary>
  
---

## 🌕 메인로직
  
EC2에서 무료로 제공하는 인스턴스(t2.micro)로는 작동하지 않아 로컬에서 배포하였다.

WSGI는 요청을 받고 응답을 반환하는 동작이 단일 동기 호출 방식이기 때문에 길게 연결되어야 하는 WebRTC 같은 비동기 통신을 이용하려면 ASGI를 사용하여야 한다.

미들웨어(CGI)에 ASGI 미들웨어가 반드시 필요했기 때문에 Uvicorn을 사용하였다. 개발 단계에서는 Django-Channel을 사용하였다.

Uvicorn은 단일 프로세스로 비동기 처리가 가능하지만, 결국 단일 프로세스라는 한계가 있기 때문에 처리량을 더 늘리기 위해서는 멀티 프로세스를 활용해야 한다.

따라서 Gunicorn을 사용하여 Uvicorn이 Gunicorn의 워커(프로세스)로서 동작하게 하였다.

## 🌙 상세로직

---
  <details><summary><h4>CMD에서 워커프로세스 실행 과정 </h4> </summary>
  
---
  
![image](https://github.com/MegaZizon/ciasom/assets/105596059/7bb0fa02-243a-4a24-b043-de5b48264217)

</details>

---

  <details><summary><h4>호스트와 시청자의 연결과정 및 미디어 스트림의 송수신 방식</h4> </summary>
  
---
  
## 🙍‍♂️호스트의 연결 과정

1. 호스트가 방송시작을 누르면 Google Stun Server와 연결하여 자신의 공인 IP 주소 및 포트를 알아내고, 그 정보(SDP)와 자신이 이용할 딥러닝 모델정보 등을 서버에 전송한다.
2. 서버에서 AioRTC가 동작하여 호스트와 연결한다. (RTCPeerConnection)
   서버는 이벤트 트리거를 설정한다.(addtrack)
   이벤트 트리거 : 영상(MediaStreamTrack)이 수신되면 호스트가 사용하는 딥러닝 모델을 적용하여 영상을 변환하고 변환된 영상 스트림 객체를 배열에 저장한다.
3. 연결이 정상적으로 완료되면, 클라이언트는 영상을 전송한다.
4. 서버에서 이벤트가 발생하여 영상이 변환되고 배열에 반영된다. 이는 호스트나 시청자에게 전송된다.

## 👨‍👨‍👦‍👦시청자의 연결 과정

1. 시청자가 방송시작을 누르면 Google Stun Server와 연결하여 자신의 공인 IP 주소 및 포트를 알아내고, 그 정보(SDP)와 자신이 시청할 호스트이름을 서버에 전송한다.
2. 서버에서 AioRTC가 동작하여 시청자와 연결한다. (RTCPeerConnection)
3. 서버에서는 호스트가 방송을 하고있는지 확인하고 방송을 하고있다면 배열에서 호스트이름에 해당하는 영상 스트림 객체를 시청자에게 송신할 준비를 한다.
4. 연결이 정상적으로 완료되면, 서버는 영상을 송신하고 시청자는 영상을 수신받는다.

#### 미디어 트래픽을 중계하는 중앙 서버 방식인 SFU 방식을 응용하여 서버를 구현하였다.

</details>

</details>

---

## 🔗 API 기능 명세서
  
![image](https://github.com/MegaZizon/ciasom/assets/105596059/7f224037-0a0f-408e-b3bc-7ba930d82657)


---

## 🗂️ DB 스키마
  
![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/1a5abe3e-617b-47ef-ae2d-49b1d00c05a7)

---

## 🚩 구현 결과



#### 메인 기능 ( 지정된 사용자 이외 모자이크 기능 )


https://github.com/MegaZizon/SangChuMarket/assets/105596059/28e7eacc-5619-4044-bfd3-290961360d19

<details><summary><h4>시청자로 입장하였을때</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

https://github.com/MegaZizon/SangChuMarket/assets/105596059/803408a6-985b-45f2-9cc4-9579fdef4663

</details>

<details><summary><h4> 전체 모자이크 </h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

https://github.com/MegaZizon/SangChuMarket/assets/105596059/f25346e6-74c5-4aea-a8b6-67b0046b58f3

</details>

<details><summary><h4> 회원가입 및 마이페이지 </h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

https://github.com/MegaZizon/SangChuMarket/assets/105596059/5bce587f-df0e-44ef-b4ff-53714661acee


</details>




</details>

