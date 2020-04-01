[toc]

# 1. Django_bookmark 2

- 다른 책으로 연습해보는 북마크
- 프로젝트 시작 전 연습하기 좋을 듯.
- 프로젝트 깃에 올릴 시 주의사항
  - 패키지 설치했다면 ? `pip freeze > requirement.txt`로 패키지 등록해놓기
  - 그래야 임포트 시 ` pip install -r requirements.txt`로 같은 가상환경 구축이 가능하다.
- 다음과 같은 작은 조각들을 계속 모은다.

```
# 3. 프로젝트 첫 페이지 만들기
## 3.1 어플리케이션 설계
## 3.2 개발 코딩하기 - 뼈대
## 3.3 개발 코딩하기 - 모델
## 3.4 개발 코딩하기 - URLconf
## 3.5 개발 코딩하기 - 뷰
## 3.6 개발 코딩하기 - 템플릿
```

## 1.1 어플리케이션 설계

- 어플리케이션은 이렇게 설계하고 기획해주세요.

### 가. 화면 UI 설계

- 화면 정의서, 문서로 작성하기

### 나. 테이블 설계

- 이렇게 짠다.

| 필드명 | 타입 | 제약 조건          | 설명        |
| ------ | ---- | ------------------ | ----------- |
| Id     | Long | PK, Auto Increment | 기본 키(PK) |

### 다. 로직 설계

- 처리 흐름을 설계한다.
- 예시) URL - View - Template 으로 이루어진다. 

| URL        | View                | Template           |
| ---------- | ------------------- | ------------------ |
| /bookmark/ | BookmarkV.as_view() | Bookmark_list.html |

### 라. URL 설계

- 다. 에서 설계한 흐름 바타대로 URL 패턴, 뷰 이름, 템플릿 파일 이름 및 뷰에서 어떤 제네릭 뷰를 사용할 것인지 등을 결정한다.

| URL 패턴     | 뷰 이름                | 템플릿 파일 이름     |
| ------------ | ---------------------- | -------------------- |
| /bookmark/12 | BookmarkDV(DetailView) | Bookmark_detail.html |

### 마. 작업 순서

1. 뼈대 만들기
2. 앱 생성
3. config - Settings.py 설정
4. 수퍼유저 생성
5. 모델 코딩
6. URL 코딩
7. 뷰 코딩
8. 템플릿 코딩

## 1.2 개발 코딩하기 - 뼈대

1. 뼈대 만들기

```bash
pip install django
django-admin startproject config .
python manage.py migrate
python manage.py createsuperuser
admin
admin@naver.com
1q2w3e4r!@
1q2w3e4r!@
python manage.py runserver
```

2. 앱 생성

```python
python manage.py startapp bookmark
```

3. Config - settings.py 설정

```python
INSTALLED_APPS = [
    ...
    'bookmark',	# 추가
]
```

```python
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        ...
    }
]
```

```python
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

...
# DB에 저장되는 시간이 한국 시간으로 저장된다.
# USE_TZ = False

# 20/03/31기준
USE_TZ = True # 로 설정하게 됬음. 한글 설정 에러가 나기 때문에...ㅠㅠ 아직 해결책 못찾음
```

```python
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]    # 추가

MEDIA_URL = '/media/'   # 추가

MEDIA_ROOT = os.path.join(BASE_DIR,'media') # 추가
```

4. 수퍼유저 생성

```python
python manage.py createsuperuser
```

## 1.3 개발 코딩하기 - 모델

1. Bookmark 모델 코딩

```python
from django.db import models

# Create your models here.
class Bookmark(models.Model):
    title = models.CharField('TITLE',max_length=100,blank=True)
    url = models.URLField('URL',unique=True)
    
    def __str__(self):
        return self.title
```

- 모델 속성
  - 맨 앞 'TITLE' : url 컬럼에 대한 별칭.
  - blank = True : 공백 값을 가질 수 있다.
- DB 가 변경되었으므로 migrate를 해준다

2. Admin 모델 코딩

```python
from django.contrib import admin
from bookmark.models import Bookmark
# Register your models here.

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id','title','url']
```

- 약간 신기했다. 어노테이션 사용해서 모델 코딩하는게 신기했음.

## 1.4 개발 코딩하기 - URLconf

- 프로젝트 URL 과 앱 URL 을 구분하여 파일을 작성하자.

```python
from django.contrib import admin
from django.urls import path, include
# config > urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookmark/',include('bookmark.urls'))
]
```

```python
from django.urls import path
# from bookmark.views import * 대신에 하나씩 불러와서 충돌을 방지한다.
from bookmark.views import BookmarkLV, BookmarkDV
# bookmark > urls.py
urlpatterns = [
    # route, view 필수 인자 2개, kwargs, name 선택 인자 2개
    path('',BookmarkLV.as_view(), name='index'),
    path('bookmark/<int:pk>/',BookmarkDV.as_view(),name='detail'),
]
```

## 1.5 개발 코딩하기 - 뷰

- ListView : Bookmark 테이블에서 여러개의 레코드를 가져오는 로직 필요
- DetailView : Bookmark 테이블에서 한개의 레코드를 가져오는 로직 필요

```python
# 클래스형 제네릭 뷰를 사용하기 위해서
from django.views.generic import  ListView, DetailView
# 테이블 조회를 위해서 모델 클래스를 임포트 한다.
from bookmark.models import Bookmark

# Create your views here.
class BookmarkLV(ListView):
    model = Bookmark

class BookmarkDV(DetailView):
    model = Bookmark
```

## 1.6 개발 코딩하기 - 템플릿

```html
<!-- bookmark/templates/bookmark/bookmark_list.html -->

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <div id="content">
        <h1>Bookmark List</h1>

        <ul>
            {% for bookmark in object_list %}
            <li><a href="{% url 'detail' bookmark.id%}">{{bookmark}}</a></li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
```

```html
<!-- bookmark/templates/bookmark/bookmark_detail.html -->

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Detail</title>
</head>
<body>
    <div id="content">
        <h1>{{object.title}}</h1>

        <ul>
            <li>url : <a href="{{object.url}}">{{object.url}}</a></li>
        </ul>
    </div>
</body>
</html>
```

## 결론

- 간단하게 북마크 시스템을 개발해보는 좋은 계기가 되었다.
- 장고의 전반적인 흐름을 이해하고, 다시한번 되짚어보는 좋은 계기가 되었다.

- 설계부분을 어떻게 진행되는지 흐름을 알 수 있어서 좋았다.

# 2. Django_blog 

- 이걸로 마무리 되는줄 알았는데 블로그 앱도 여기서 같이 개발한다고 한다.
- 앱을 한 프로젝트에서 두개 이상 써본적은 첨이라 조금 기대된다.

## 2.1 어플리케이션 설계

- 1장에서와 마찬가지로 앱설계를 진행한다.

## 2.2 개발 코딩하기 - 뼈대

`python manage.py startapp blog`

```python
INSTALLED_APPS = [
    ...
    'bookmark',
    'blog',
]
```

## 2.3 개발 코딩하기 - 모델

```python
from django.db import models
# URL 패턴을 만들어주는 장고 내장함수.
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    # CharField : 한줄로 입력됨 , verbose_name : 컬럼에대한 별칭을 지정, max_length : 최대 길이 설정
    title = models.CharField(verbose_name="TITLE", max_length=50)

    # SlugField : 제목에 대한 별칭 , unique : 특정 포스트 검색 시 기본키 대신 사용 , allow_unicode : 한글 처리 ,
    # help_text : 해당 컬럼을 설명해주는 문구로 폼 화면에서 나타남.
    slug = models.SlugField("SLUG",unique=True,allow_unicode=True,help_text='one word for title alias.')
    description = models.CharField("DESCRIPTION",max_length=100, blank=True,help_text='simple description text')

    # TextField : 여러줄 입력 가능
    content = models.TextField("CONTENT")

    # auto_now_add : 객체 생성될 떄의 시각을 자동으로 기록
    create_dt = models.DateTimeField("CREATE DATE", auto_now_add=True)

    # auto_now : 객체가 변동될 때의 시각을 자동으로 기록
    modifiy_dt = models.DateTimeField("MODIFY DATE", auto_now=True)

    # 필드 속성 외에 필요한 파라메터가 있으면, Meta 내부 클래스로 정의한다.
    class Meta:
        # 테이블의 단수 별칭
        verbose_name = 'post'
        # 테이블의 복수 별칭
        verbose_name_plural = 'posts'
        # DB에 저장되는 테이블의 이름
        db_table = 'blog_posts'
        # 모델 객체 리스트 출력 시 기준이 되는 것.
        ordering = ['-modify_dt','-create_dt']

    def __str__(self):
        return self.title

    # 이 메소드가 정의된 객체를 지칭하는 URL을 반환.
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=(self.slug,))

    def get_previous(self):
        return self.get_previous_by_modify_dt()

    def get_next(self):
        return self.get_next_by_modify_dt()
```

```python
# blog/admin.py

from django.contrib import admin
from blog.models import Post

# Register your models here.
@admin.register(Post) # 데코레이터를 사용해서 간단해졌다.
class PostAdmin(admin.ModelAdmin):  # 어드민에서 Post클래스가 어떻게 보일까
    list_display = ['id','title','modify_dt']   # 출력할 것
    list_filter = ['modify_dt'] # 필터 사이드바
    search_fields = ['title','content'] # 검색 박스
    prepopulated_fields = {'slug':['title',]}   
    # slug 필드는 title 필드를 사용해 미리 채워두기
```

```bash
$ python manage.py makemigrations blog
$ python manage.py migrate
```

## 2.4 개발 코딩하기 - URLconf

```python
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
    path('archive/<int:year>/<str:month>/<int:day>/',views.PostDAV,name='post_day_archive'),
    # /blog/archive/today/
    path('archive/today/',views.PostTAV.as_view(),name='post_today_archive')
    
]
```

## 2.5. 개발 코딩하기 - 뷰

```python
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
```

## 2.6 개발 코딩하기 - 템플릿

- Git repository 에 다 올려놓았음. 

# 3. 프로젝트 첫 페이지 만들기

## 3.1 어플리케이션 설계

1. UI 설계
2. 테이블 설계
   - 테이블 변경사항 없음
3. URL 설계
   - 루트 URL 을 추가하자
4. 로직 설계
   - 루트에서 각 앱으로 이동하는 네비게이션을 만들자.
5. 작업/코딩 순서
   - 

## 3.2 개발 코딩하기 - 뼈대

- 앱을 신규로 만드는 것이 아니기 때문에 뼈대작업이 필요 없다.

## 3.3 개발 코딩하기 - 모델

- 테이블에 대한 변동사항은 없다.

## 3.4 개발 코딩하기 - URLconf

1. config - urls.py 코딩

```python
from django.contrib import admin
from django.urls import path, include
from config.views import HomeView   # 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookmark/',include('bookmark.urls')),
    path('blog/',include('blog.urls')),
    path('',HomeView.as_view(),name='home'),    # 추가
]
```

## 3.5 개발 코딩하기 - 뷰

- 템플릿 뷰를 임포트해서 사용한다.

```python
from django.views.generic import TemplateView

#-- TemplateView
class HomeView(TemplateView):
    # template_name : 필수 오버라이딩이다.
    # 템플릿 위치 디렉토리는 settings.py의
    # 'DIRS': [os.path.join(BASE_DIR,"templates")] 로 지정되어있다.
    template_name = 'home.html'
```

## 3.6 개발 코딩하기 - 템플릿

- 신기하게 base.html, home.html 로 나누어서 코딩한다.

  - 근본 : base.html
  - 첫 페이지 : home.html

  로 구분한다.

- templates/base.html
  - 부트스트랩 설정
  - 골격 설정
  - 폰트어썸 설정

- templates/home.html
  - {% extends 'base.html' %}
  - {% load static %}
  - {% static 'img/header.jpg' %}

# 4. 기존 앱 개선하기 - Bookmark, Blog
## 4.1 어플리케이션 설계

1. 화면 UI 설계

- home.html 에서 각각의 앱으로 이동할 수 있도록 개선하자.

## 4.2 개발 코딩하기 - 뼈대

없음.

## 4.3 개발 코딩하기 - 모델

없음.

## 4.4 개발 코딩하기 - URLconf

없음.

## 4.5 개발 코딩하기 - 뷰

없음.

## 4.6 개발 코딩하기 - 템플릿

- 각각 상속 템플릿으로 변환 후 연결할 예정이다.

# 5. Blog 앱 확장 - Tag 달기
## 5.1 어플리케이션 설계

1. 화면 설계
   - 태그 관련 두개 화면 신규 추가
   - 기존 상세 화면 수정
2. 테이블 설계
   - 태그 기능을 위한 필드 추가
3. URL 설계
   - 태그 관련 URL 추가
     - 태그 클라우드를 보기 위한 URL
     - 특정 태그가 달려 있는 포스트들의 리스트를 보여주는 URL

## 5.2 개발 코딩하기 - 뼈대

1. 태그잇 오픈소스 활용하기

```bash
pip install django-taggit
pip install django-taggit-templatetags
```

```python
INSTALLED_APPS = [
    ...
    'taggit',   # 추가
    'taggit_templatetags2', # 추가
]
```

```python
...
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

TAGGIT_CASE_INSENSITIVE = True  # 추가

TAGGIT_LIMIT = 50   # 추가
```

## 5.3 개발 코딩하기 - 모델

1. 모델 추가

```python
# blog/models.py

from taggit.managers import TaggableManager
tags = TaggableManager(blank=True)
```

```python
# blog/admin.py

from django.contrib import admin
from blog.models import Post

# Register your models here.
@admin.register(Post) # 데코레이터를 사용
class PostAdmin(admin.ModelAdmin):  # 어드민에서 Post클래스가 어떻게 보일까
    list_display = ['id','title','modify_dt', 'tag_list']   # 출력할 것, tag_list 추가
    list_filter = ['modify_dt'] # 필터 사이드바
    search_fields = ['title','content'] # 검색 박스
    prepopulated_fields = {'slug':['title',]}   # slug 필드는 title 필드를 사용해 미리 채워두기
    # 두 메서드 추가.
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self,obj):
        return ', '.join(o.name for o in obj.tags.all())
```

2. 모델 추가되었으니 DB migrate 가 필요하다.

```bash
python manage.py makemigrations blog
python manage.py migrate
```

## 5.4 개발 코딩하기 - URLconf

```python
# /blog/tag/
path('tag/',views.TagCloudTV.as_view(),name='tag_cloud'),
# /blog/tag/tagname/
path('tag/<str:tag>/',views.TaggedObjectLV.as_view(),name='tagged_object_list'),a
```

## 5.5 개발 코딩하기 - 뷰

```python
class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'
class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags_name=self.kwargs.get('tag'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
```

## 5.6 개발 코딩하기 - 템플릿

- 

# 6. Blog 앱 확장 - 댓글 기능
## 6.1 어플리케이션 설계
## 6.2 개발 코딩하기 - 뼈대
## 6.3 개발 코딩하기 - 모델
## 6.4 개발 코딩하기 - URLconf
## 6.5 개발 코딩하기 - 뷰
## 6.6 개발 코딩하기 - 템플릿

# 7. Blog 앱 확장 - 검색 기능

- Q-객체 활용한 검색 단어가 있는 블로그를 찾고, 그 결과를 보여주는 기능 개발해보기

## 7.1 어플리케이션 설계

1. 화면 설계
   - 블로그 글에 대한 검색기능 구현해보기
   - 검색 폼과 검색 결과를 같은 페이지에 보여줘보자
2. 테이블 설계
   - 없음
3. URL 설계
   - 검색 폼 처리를 위한 URL 넣기

## 7.2 개발 코딩하기 - 뼈대

- 없음

## 7.3 개발 코딩하기 - 모델

- 없음

## 7.4 개발 코딩하기 - URLconf

```python
# blog/urls.py

# /blog/search/
path('search/',views.SearchFormView.as_view(),name='search'),
```

## 7.5 개발 코딩하기 - 뷰

``` python
from django.views.generic import FormView
from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render

#-- FormView
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord) | Q(content_icontains=searchWord)).distict()
        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request,self.template_name,context)
```

## 7.6 개발 코딩하기 - 템플릿

```python
{% extends 'base.html' %}

{% block title %}Post_search.html{% endblock %}

{% block content %}
    <h1>Blog Search</h1>

    <form action="." method="post">{% csrf_token %}
        {{form.as_table}}
        <input type="submit" value="Submit" class="btn btn-primary btn-sm">
    </form>
    {% if object_list %}
        {% for post in object_list %}
            <h2><a href="{{post.get_absolute_url}}">{{post.title}}</a></h2>
            {{post.modify_date|date:"N d, Y"}}
            <p>post.description}}</p>
        {% endfor %}
    {% elif search_term %}
        <b><i>Search Word({{search_term}}) Not Found !</i></b>
    {% endif %}
{% endblock %}
```

- 기능 동작이 안된다.. 일단 계속 진행해보자.

# 8. 실전 프로그램 개발 - Photo 앱
## 8.1 어플리케이션 설계

1. 화면 UI 설계
   - 템플릿 파일명과 화면 요소들이 무엇을 의미하는지, 그리고 어느 모델 피드에 해당하는지 등을 표시함.
2. 테이블 설계
   - 엘범, 포토 테이블 2개.
     - 1:N 관계가 성립된다.
3. URL 설계
   - 엘범, 포토 URL 설계

## 8.2 개발 코딩하기 - 뼈대



## 8.3 개발 코딩하기 - 모델
## 8.4 개발 코딩하기 - URLconf
## 8.5 개발 코딩하기 - 뷰
## 8.6 개발 코딩하기 - 템플릿