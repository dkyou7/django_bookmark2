from django.contrib import admin
from blog.models import Post

# Register your models here.
@admin.register(Post) # 데코레이터를 사용해서 간단해졌다.
class PostAdmin(admin.ModelAdmin):  # 어드민에서 Post클래스가 어떻게 보일까
    list_display = ['id','title','modify_dt']   # 출력할 것
    list_filter = ['modify_dt'] # 필터 사이드바
    search_fields = ['title','content'] # 검색 박스
    prepopulated_fields = {'slug':['title',]}   # slug 필드는 title 필드를 사용해 미리 채워두기