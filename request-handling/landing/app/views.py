from collections import Counter

from django.shortcuts import render # type: ignore

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')
    if from_landing in ['original', 'test']:
        counter_click[from_landing] += 1
    return render(request, 'index.html')

def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ab_test_arg = request.GET.get('ab-test-arg')
    if ab_test_arg == 'test':
        counter_show['test'] += 1
        return render(request, 'landing_alternate.html')
    counter_show['oroginal'] += 1
    return render(request, 'landing.html')

def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    original_conversion = 0.0
    if counter_show['test'] > 0:
        original_conversion = counter_click['original'] / counter_show['test']
    return render(request, 'stats.html', context={
        'test_conversion': 0.5,
        'original_conversion': 0.4,
    })
