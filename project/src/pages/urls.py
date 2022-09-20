from django.urls import path

from .views import homePageView, addView, deleteView, downloadView, addNicknameView, sendView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('download/<int:fileid>', downloadView, name='add'),
    path('delete/', deleteView, name='delete'),
    path('addNickname/', addNicknameView, name='addNickname'),
    # path('filename/', filenameView, name='filename'),
    path('send/', sendView, name='send')
]
