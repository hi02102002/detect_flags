from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .detects import detect_flag


def home(request):
    return render(request, 'index.html')

@csrf_exempt
def detect_flags(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        detected_flag = detect_flag(file_path)

        if detected_flag is None:
            return JsonResponse({'error': 'Could not process the image'}, status=400)
        
        return JsonResponse({'data': detected_flag})
        
        