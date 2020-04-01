from django.urls import path, re_path
# 뷰 클래스가 많을 때는 이렇게 뷰 모듈 자체를 임포트한다.
from blog import views


app_name = 'blog'

urlpatterns = [
    # route, view 필수 인자 2개, kwargs, name 선택 인자 2개

    # /blog/
    path('',views.PostLV.as_view(), name='index'),
    # /blog/post/
    path('post/',views.PostLV.as_view(),name='post_list'),
    # /blog/post/django-example/
    # 한글 포함 슬러그 처리를 위해.
    re_path(r'^post/(?P<slug>[-\w]+)/$',views.PostDV.as_view(),name='post_detail'),
    # /blog/archive/
    path('archive/',views.PostAV.as_view(),name='post_archive'),
    # /blog/archive/2020/
    path('archive/<int:year>/',views.PostYAV.as_view(),name='post_year_archive'),
    # /blog/archive/2020/nov/
    path('archive/<int:year>/<str:month>/',views.PostMAV.as_view(),name='post_month_archive'),
    # /blog/archive/2020/nov/10/
    path('archive/<int:year>/<str:month>/<int:day>/',views.PostDAV.as_view(),name='post_day_archive'),
    # /blog/archive/today/
    path('archive/today/',views.PostTAV.as_view(),name='post_today_archive'),
    # /blog/tag/
    path('tag/',views.TagCloudTV.as_view(),name='tag_cloud'),
    # /blog/tag/tagname/
    path('tag/<str:tag>/',views.TaggedObjectLV.as_view(),name='tagged_object_list'),
    # /blog/search/
    path('search/',views.SearchFormView.as_view(),name='search'),
]