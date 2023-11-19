from django.urls import path
from . import views

urlpatterns = [
    path('list',views.broadList),
    path('watch',views.watch),
    path('onair/start',views.start),
    path('onair/set/',views.onair),
    path('broadcast/<str:host_id>',views.broadcast),
    path('onair/end/<str:host_id>',views.quitbroadcast),
    path('search/host/<str:host_id>',views.searchHost),
    path('search/title/<str:title>',views.searchTitle),
    path('test',views.test,name="live_test"),
]