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
    modify_dt = models.DateTimeField("MODIFY DATE", auto_now=True)

    from taggit.managers import TaggableManager
    tags = TaggableManager(blank=True)

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
