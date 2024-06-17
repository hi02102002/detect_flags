from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .detects import detect_objects
from asgiref.sync import sync_to_async

def home(request):
    return render(request, 'index.html')

@csrf_exempt
async def detect_flags(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        try:
         
            detected_flag = await detect_objects(file_path)
            
            if detected_flag is None:
                return JsonResponse({'error': 'Could not process the image'}, status=400)
            
            return JsonResponse({'data': detected_flag})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
        
        