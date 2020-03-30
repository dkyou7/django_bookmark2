from django.urls import path
# from bookmark.views import * 대신에 하나씩 불러와서 충돌을 방지한다.
from bookmark.views import BookmarkLV, BookmarkDV

urlpatterns = [
    # route, view 필수 인자 2개, kwargs, name 선택 인자 2개
    path('',BookmarkLV.as_view(), name='index'),
    path('/<int:pk>/',BookmarkDV.as_view(),name='detail'),
]