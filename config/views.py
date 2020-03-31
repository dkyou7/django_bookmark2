from django.views.generic import TemplateView

#-- TemplateView
class HomeView(TemplateView):
    # template_name : 필수 오버라이딩이다.
    # 템플릿 위치 디렉토리는 settings.py의
    # 'DIRS': [os.path.join(BASE_DIR,"templates")] 로 지정되어있다.
    template_name = 'home.html'