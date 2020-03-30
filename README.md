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