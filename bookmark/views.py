from django.shortcuts import render
# 클래스형 제네릭 뷰를 사용하기 위해서
from django.views.generic import  ListView, DetailView
# 테이블 조회를 위해서 모델 클래스를 임포트 한다.
from bookmark.models import Bookmark

# Create your views here.
class BookmarkLV(ListView):
    model = Bookmark

class BookmarkDV(DetailView):
    model = Bookmark