from django.http import FileResponse,HttpResponse
import os

def download_csv(request):
    file_path = 'final_api_test.csv'
    
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        return response
    else:
        return HttpResponse('File not found.')
