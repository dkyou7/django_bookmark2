[toc]

# Django_bookmark 2

- 다른 책으로 연습해보는 북마크
- 프로젝트 시작 전 연습하기 좋을 듯.
- 프로젝트 깃에 올릴 시 주의사항
  - 패키지 설치했다면 ? `pip freeze > requirement.txt`로 패키지 등록해놓기
  - 그래야 임포트 시 ` pip install -r requirements.txt`로 같은 가상환경 구축이 가능하다.

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
USE_TZ = False
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

# Django_blog 

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

