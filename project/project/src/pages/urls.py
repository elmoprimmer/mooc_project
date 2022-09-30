from django.urls import path

from .views import homePageView, addView, deleteView, downloadView, addNicknameView, sendView
# from .views import change_password
from django.conf.urls import url

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('download/<int:fileid>', downloadView, name='add'),
    path('delete/', deleteView, name='delete'),
    path('addNickname/', addNicknameView, name='addNickname'),
    path('send/', sendView, name='send'),
    # path('changepassword', change_password, name='change_password')
]
