from django.contrib import admin
from blog.models import Post

# Register your models here.
@admin.register(Post) # 데코레이터를 사용해서 간단해졌다.
class PostAdmin(admin.ModelAdmin):  # 어드민에서 Post클래스가 어떻게 보일까
    list_display = ['id','title','modify_dt', 'tag_list']   # 출력할 것, tag_list 추가
    list_filter = ['modify_dt'] # 필터 사이드바
    search_fields = ['title','content'] # 검색 박스
    prepopulated_fields = {'slug':['title',]}   # slug 필드는 title 필드를 사용해 미리 채워두기

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self,obj):
        return ', '.join(o.name for o in obj.tags.all())