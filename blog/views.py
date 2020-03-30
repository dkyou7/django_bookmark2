from django.shortcuts import render

# 클래스형 제네럴 뷰 임포트
from django.views.generic import ListView,DetailView
from django.views.generic.dates import ArchiveIndexView,YearArchiveView,MonthArchiveView
from django.views.generic.dates import DayArchiveView,TodayArchiveView

from blog.models import Post    # 테이블 조회를 위한 임포트

# Create your views here.

#-- ListView
class PostLV(ListView):
    model = Post    # 대상 테이블 정의

    # default : blog/post_list.html
    template_name = 'blog/post_all.html'

    # 템플릿으로 넘겨주는 객체 리스트에 대한 컨텍스트 변수명 지정.
    context_object_name = 'posts'
    paginate_by = 2

#-- DetailView
class PostDV(DetailView):
    model = Post

#-- ArchiveView
# 테이블로부터 객체 리스트를 가져와, 날짜 필드 기준으로 최신 객체 먼저 출력한다.
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'

# 테이블로부터 날짜 필드의 연도를 기준으로 객체 리스트를 가져와 그 객체들이 속한 월을 리스트로 출력.
# 날짜 필드의 연도 파라미터는 URLconf에서 추출해 뷰로 넘겨줍니다.
class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    # 해당 연도에 해당하는 객체의 리스트를 만들어서 템플릿에 넘겨준다.
    # 템플릿 파일에서 object_list 컨텍스트 변수를 사용할 수 있다. default : false
    make_object_list = True
class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'
class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'
class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'

