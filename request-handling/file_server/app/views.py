import datetime
import os
from django.conf import settings # type: ignore
from django.shortcuts import render, Http404 # type: ignore

def file_list(request, date=None):
    files_path = settings.FILES_PATH
    files = []
    
    for filename in os.listdir(files_path):
        file_path = os.path.join(files_path, filename)
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
            ctime = datetime.datetime.fromtimestamp(stat.st_ctime)
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
            file_info = {
                'name': filename,
                'ctime': ctime,
                'mtime': mtime,
            }
            
            if date is None or date == ctime.date() or date == mtime.date():
                files.append(file_info)
    
    context = {'files': files, 'date': date}
    return render(request, 'index.html', context)

def file_content(request, name):
    files_path = settings.FILES_PATH
    file_path = os.path.join(files_path, name)
    
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("File does not exist")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return render(
        request,
        'file_content.html',
        context={'file_name': name, 'file_content': content}
    )