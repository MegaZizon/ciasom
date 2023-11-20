# Ciasom
실시간 등록된 사용자 외 모자이크 웹 플랫폼 

## 🖥️ 프로젝트 소개
사용자에게 사진을 입력받아 입력받은 사진 외의 사용자가 영상에 출연할 경우 모자이크 처리를 진행함
<br>

##  팀 소개
지준오(백엔드), 전찬수(AI), 최호성(백엔드), 백지원(프론트엔드)
<br>

### ⚙️ 개발 환경
- `Python 3.11`
- `Django`
- **Library** :  WebRTC, AioRTC
- **Database** : SQLite3

## 📌 주요 기능
#### 라이브 스트리밍 기능
#### 라이브 스트리밍 시청 기능
#### 실시간 모자이크 기능
#### 사용자의 사진을 입력받아 학습하여 모델을 생성하는 기능
#### 썸네일 표시 기능
<br>

## 🗝️ API 기능 명세서

<html xmlns:m="http://schemas.microsoft.com/office/2004/12/omml"
xmlns="http://www.w3.org/TR/REC-html40">

<head>

<meta name=ProgId content=PowerPoint.Slide>
<meta name=Generator content="Microsoft PowerPoint 15">
<style>
<!--tr
	{mso-height-source:auto;}
col
	{mso-width-source:auto;}
td
	{padding-top:1.0px;
	padding-right:1.0px;
	padding-left:1.0px;
	mso-ignore:padding;
	color:windowtext;
	font-size:18.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:Arial;
	mso-generic-font-family:auto;
	mso-font-charset:0;
	text-align:general;
	vertical-align:bottom;
	border:none;
	mso-background-source:auto;
	mso-pattern:auto;}
.oa1
	{border-top:2.0pt solid black;
	border-right:none;
	border-bottom:2.0pt solid black;
	border-left:none;
	background:black;
	mso-pattern:auto none;
	text-align:center;
	vertical-align:top;
	padding-bottom:2.18pt;
	padding-left:4.37pt;
	padding-top:2.18pt;
	padding-right:4.37pt;}
.oa2
	{border-top:2.0pt solid black;
	border-right:none;
	border-bottom:none;
	border-left:none;
	background:#E7E7E7;
	mso-pattern:auto none;
	vertical-align:top;
	padding-bottom:2.18pt;
	padding-left:4.37pt;
	padding-top:2.18pt;
	padding-right:4.37pt;}
.oa3
	{vertical-align:top;
	padding-bottom:3.6pt;
	padding-left:7.2pt;
	padding-top:3.6pt;
	padding-right:7.2pt;}
.oa4
	{background:white;
	mso-pattern:auto none;
	vertical-align:top;
	padding-bottom:2.18pt;
	padding-left:4.37pt;
	padding-top:2.18pt;
	padding-right:4.37pt;}
.oa5
	{background:#E7E7E7;
	mso-pattern:auto none;
	vertical-align:top;
	padding-bottom:2.18pt;
	padding-left:4.37pt;
	padding-top:2.18pt;
	padding-right:4.37pt;}
.oa6
	{background:#F2F2F2;
	mso-pattern:auto none;
	vertical-align:top;
	padding-bottom:2.18pt;
	padding-left:4.37pt;
	padding-top:2.18pt;
	padding-right:4.37pt;}
.oa7
	{background:#D9D9D9;
	mso-pattern:auto none;
	vertical-align:top;
	padding-bottom:2.18pt;
	padding-left:4.37pt;
	padding-top:2.18pt;
	padding-right:4.37pt;}
.oa8
	{mso-pattern:auto none;
	vertical-align:top;
	padding-bottom:3.6pt;
	padding-left:7.2pt;
	padding-top:3.6pt;
	padding-right:7.2pt;}
.oa9
	{border-top:none;
	border-right:none;
	border-bottom:2.0pt solid black;
	border-left:none;
	background:white;
	mso-pattern:auto none;
	vertical-align:top;
	padding-bottom:2.18pt;
	padding-left:4.37pt;
	padding-top:2.18pt;
	padding-right:4.37pt;}
-->
</style>
</head>

<body>
<!--StartFragment-->


화면 | URL | 메소드 | 세부기능 | 설명
-- | -- | -- | -- | --
메인 페이지 | / | GET | - | 메인페이지 뷰
/login | POST | 로그인 | 아이디/비밀번호   일치 확인 후 로그인,   틀릴경우 알림
/signup | POST | 회원가입 | 아이디/이메일/닉네임 중복확인 기능 구현
마이 페이지 | /mypage | GET | 마이페이지 | 마이페이지 뷰
/mypage/changeInfo | POST | 마이페이지 정보 수정 | POST 값에   따라 회원정보(닉네임/이메일/비밀번호) 수정
모델 등록 페이지 | /faceupload | GET | 모델 등록 페이지 | 모델 등록 페이지 뷰
/faceupload/deeplearn | POST | 모델 등록 | 입력받은 사진을 토대로 모델 학습하여 pkl 파일 생성 기능
모델 등록 리스트 페이지 | /facelist | GET | - | 등록된 모델 리스트 페이지 뷰
/facelist/model/{model_id} | POST | 모델 삭제 | 모델 삭제 기능
스트리머 메뉴 페이지 | /streamerset | GET | - | 스트리머 메뉴 페이지 뷰
방송 세팅 페이지 | /onair/set | GET | - | 방송 세팅 페이지 뷰
/onair/start | POST | 방송 시작 | WebRTC 로   서버와 PeerConnection 및    오디오/비디오   스트리밍 전송 기능   10초마다 썸네일을 생성하여 방송 리스트에 보여지도록 하는 로직 구현
/onair/end | POST | 방송 종료 | 방송 종료 기능
방송 리스트 페이지 | /list | GET | - | 방송 리스트 페이지 뷰
방송 시청 페이지 | /broadcast | GET | 방송 시청 | 방송 시청 페이지 뷰
/broadcast/{host_id} | POST | 방송 시청 시작 | 서버와 PeerConnection 한 뒤 host_id의   비디오/오디오 스트림을 WebRTC로 수신 기능   시청자가 입장하면 시청자 수가 증가하도록 하는 로직 구현
스트리머 검색 페이지 | /search/host/{host_id} | POST | 스트리머 닉네임 검색 | 입력받은 문자열을 포함하는 스트리머 닉네임 검색 기능
방송제목 검색 페이지 | /search/title/{title} | POST | 방송 제목 검색 | 입력받은 문자열을 포함하는 방송 제목 검색 기능



<!--EndFragment-->
</body>

</html>

<details><summary><h4>판매자와 구매자의 중간지점 찾기</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->
```
        function getAddr(lat,lng){
            let geocoder = new kakao.maps.services.Geocoder();

            let coord = new kakao.maps.LatLng(lat, lng);
            let callback = function(result, status) {
                if (status === kakao.maps.services.Status.OK) {
                    addname2=result[0].address.address_name;
                }
            }
            geocoder.coord2Address(coord.getLng(), coord.getLat(), callback);
        }
  
        var geocoder = new kakao.maps.services.Geocoder();
        var callback = function(result, status) {
            if (status === kakao.maps.services.Status.OK) {
                console.log(result);
                addx1=result[0].address.x;
                addy1=result[0].address.y;
                addx1=parseFloat(addx1);
                addy1=parseFloat(addy1);
                addx3=addx1+addx2;
                addy3=addy1+addy2;
                addx4 = addx3/2;
                addy4 = addy3/2;
                lat = addy4;
                lng = addx4;
        
                options = { //지도를 생성할 때 필요한 기본 옵션
                    center: new kakao.maps.LatLng(addy4, addx4), //지도의 중심좌표.
                    level: 4 //지도의 레벨(확대, 축소 정도)
                };
                const container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
                let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
                var marker = new kakao.maps.Marker({ 
                    // 지도 중심좌표에 마커를 생성합니다 
                    position: map.getCenter() 
                }); 
                // 지도에 마커를 표시합니다
                marker.setMap(map);
                getAddr(lat,lng);
            }
        };

```
</details>
<details><summary><h4>1:1 대화 기능</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

1. <message.jsp에 관하여(메세지보내는 창)>메시지를 보낼 때 msg 테이블에 reciverID에 받는사람 senderID에 보낸사람을 입력하여 msg table에 into 하도록 하였습니다.
   과거 대화내역 출력 부분은 select * from msg where (받는사람 = 나 and 보낸사람 = 상대) or (받는사람 = 상대 and 보낸사람 = 나) 인 경우를 리스트에 담아서 가져오게하였습니다.
   가져온 뒤 reciverID가 나면 대화의 왼쪽, senderID가 나면 대화의 오른쪽에 표시되도록 하였습니다.


2. <message_main.jsp에 관하여(메세지함 창)>메세지 함에서 개개인별 대화내역의 마지막 내용을 리스트를 가져온 방법은 자신의 닉네임이 받는사람 이거나 보낸사람이면(select * from msg where (senderId= 자신닉네임) or (reciverId= 자신닉네임)  리스트에 담아서 가지고왔습니다.
   그 뒤 한 상대당 1개의 리스트(채팅방)만 보여지게 하기 위해 중복된 값을 제거하여(msgList3 메소드에서 반복문과 ArrayList<String>의 contain 메소드를 이용) 대화함에 출력하였습니다.


3. 메세지 알림기능은 is Read가 0이고 받는사람이 자신이라면 알림이 표시되도록 하였고(msgToMe 메소드) 알림을 확인할경우 isRead를 1로 update 하도록 하였습니다(msgRead 메소드)


<a href="https://github.com/MegaZizon/SangChuMarket/blob/main/src/main/webapp/message/message.jsp">message.jsp</a>


<a href="https://github.com/MegaZizon/SangChuMarket/blob/main/src/main/webapp/message/message_main.jsp">message_main.jsp</a>


<a href="https://github.com/MegaZizon/SangChuMarket/blob/main/src/main/java/msg/MsgDAO.java">MsgDAO.java</a>

</details>

</details>
<details><summary><h4> 데이터베이스 구성</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

TABLE USER


![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/4eaa899e-808a-4f7c-b8ac-3c4ed7857624)

TABLE Image


![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/96e74297-a60f-4b3e-924f-3d2ec16e4984)

TABLE Msg


![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/a17cc4e8-6b2b-4764-9059-1ab6669f5d0a)


</details>


<details><summary><h4>MVC 모델 1</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/955710bc-b54b-49da-8dc0-8ce25f9b12ac)


상추마켓은 MVC모델 1 구조를 사용하였습니다. View 와 Controller 모두 JSP가 담당하며 Model은 JavaBeans에서 담당합니다. 
구조가 단순하여 익히고 적용하기가 쉽기 때문에 이 구조를 사용하였습니다.
하지만 사용하면서 출력을 위한 뷰 코드와 로직처리를 위한 자바 코드 등이 뒤섞여 나중에는 유지보수가 매우 어려워지는 것을 느꼈습니다. 
</details>

</details>

## 🚩 구현 결과



#### 메인 페이지


![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/7a484bd3-a125-4685-8ee9-ad183203a237)


<details><summary><h4>로그인 팝업창</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/6a2e72cf-6387-4553-8546-491e2ebb469f)

</details>

<details><summary><h4>회원가입 팝업창</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/aab684ce-f219-4a25-ae99-1b8e8d1ceea0)


</details>

<details><summary><h4>검색 페이지</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/66290e9d-d1dc-45a4-9a65-07422677421b)


</details>

<details><summary><h4>판매글 등록 페이지</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/a7cf49bc-0ba3-407d-b4ba-7c6b7cb4b2a0)


</details>

<details><summary><h4>판매자 상세정보 페이지</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/ac490a7d-1784-4585-af1c-43d8d5955b8c)
![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/c80466e9-c3e0-4b4f-8630-075434985461)
![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/49a7ea1f-5cd9-4f4f-a81e-1a10adf6831c)
![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/9ad55d46-4121-45da-9366-559427da32ac)




</details>

<details><summary><h4>1:1 대화</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/b1a24d66-cddf-44a1-9d76-0e4ed2e95b4d)


</details>

<details><summary><h4>중간지점 찾기 클릭</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/5d35e499-ad56-473a-bee0-49eec2eac468)



</details>

<details><summary><h4>판매자 상세정보 페이지</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/f9d2e029-df85-48f7-9658-e983d61ae93c)


</details>

<details><summary><h4>회원정보 페이지</h4> </summary>

<!-- summary 아래 한칸 공백 두어야함 -->

![image](https://github.com/MegaZizon/SangChuMarket/assets/105596059/e7a3982b-f7c1-45a2-9880-cedc41b4bc58)



</details>

