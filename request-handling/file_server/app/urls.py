from django.urls import path, register_converter # type: ignore
import datetime
from . import views
# Определите и зарегистрируйте конвертер для определения даты в урлах и наоборот урла по датам
class DateConverter:
    regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value):
        return datetime.datetime.strftime(value, '%Y-%m-%d').date()
    
    def to_url(self, value):
        return value.strftime('%Y-%m-%d')
    
register_converter(DateConverter, 'date')

urlpatterns = [
    # Определите схему урлов с привязкой к отображениям .views.file_list и .views.file_content
    path('', views.file_list, name='file_list'),
    path('<date:date>/', views.file_list, name='file_list'),    # задайте необязательный параметр "date"
                                                                # для детальной информации смотрите HTML-шаблоны в директории templates
    path('<str:name>', views.file_content, name='file_content'),
]