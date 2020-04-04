from django.urls import path
# from bookmark.views import * 대신에 하나씩 불러와서 충돌을 방지한다.
# from bookmark.views import BookmarkLV, BookmarkDV
# 이제 걍 다 불러온다
from bookmark import views

app_name = 'bookmark'

urlpatterns = [
    # route, view 필수 인자 2개, kwargs, name 선택 인자 2개
    path('',views.BookmarkLV.as_view(), name='index'),
    path('<int:pk>/',views.BookmarkDV.as_view(),name='detail'),
    path('add/',views.BookmarkCreateView.as_view(),name='add'),
    path('change/',views.BookmarkChangeLV.as_view(),name='change'),
    path('<int:pk>/update/',views.BookmarkUpdateView.as_view(),name='update'),
    path('<int:pk>/delete/',views.BookmarkDeleteView.as_view(),name='delete'),
]