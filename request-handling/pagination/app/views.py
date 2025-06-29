from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
import csv
from django.conf import settings
from django.core.paginator import Paginator

def index(request):
    return redirect(reverse('bus_stations'))

def bus_stations(request):
    data = []
    try:
        with open(settings.BUS_STATION_CSV, 'r', encoding='cp1251') as file:
            # Прочитаем первую строку для проверки заголовков
            first_line = file.readline().strip()
            file.seek(0)  # Возвращаемся в начало файла
            
            # Определяем разделитель по наличию запятой в первой строке
            delimiter = ',' if ',' in first_line else ';'
            
            reader = csv.DictReader(file, delimiter=delimiter)
            
            # Определяем правильные ключи для столбцов
            fieldnames = [f.strip() for f in reader.fieldnames]  # Убираем пробелы вокруг названий
            name_key = next((f for f in fieldnames if 'name' in f.lower()), None)
            street_key = next((f for f in fieldnames if 'street' in f.lower()), None)
            district_key = next((f for f in fieldnames if 'district' in f.lower()), None)
            
            if not all([name_key, street_key, district_key]):
                raise ValueError("Не удалось определить необходимые столбцы в CSV файле")
            
            for row in reader:
                data.append({
                    'Name': row.get(name_key, ''),
                    'Street': row.get(street_key, ''),
                    'District': row.get(district_key, ''),
                })
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
        # В случае ошибки возвращаем пустой список
    
    # Пагинация с использованием Paginator
    paginator = Paginator(data, 10)
    page_number = int(request.GET.get('page', 1))
    page = paginator.get_page(page_number)
    
    # Формирование URL для пагинации
    base_url = reverse('bus_stations')
    prev_page_url = None
    next_page_url = None
    
    if page.has_previous():
        prev_page_url = f"{base_url}?{urlencode({'page': page.previous_page_number()})}"
    
    if page.has_next():
        next_page_url = f"{base_url}?{urlencode({'page': page.next_page_number()})}"
    
    return render(request, 'index.html', context={
        'bus_stations': page.object_list,
        'current_page': page.number,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })