from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login,name='login'),
    path('mypage',views.mypage,name='mypage'),
    path('mypage/changeInfo',views.changeInfo),
    path('register/',views.register,name="register"),
    path('register/delete/<str:post_id>',views.regDel),
    path('register/delete/model/<str:model_id>',views.modelDel),
    path('register/registImg',views.registImg),
    path('logout',views.logout,name='logout'),
    path('signup',views.signup,name='signup'),
    #path('signup/submit',views.signupSubmit),
    path('verify',views.verify,name='verify'),
    path('verify/submit',views.verifySubmit),
    path('deeplearn/<str:user_id>',views.deeplearn),
    path('',views.index,name="main"),
    path('streamerSet',views.streamerSet,name="streamerSet"),
    path('faceUpload',views.faceUpload,name="faceUpload"),
    path('facelist',views.facelist,name="facelist"),
]