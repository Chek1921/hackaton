from .models import Report
from rest_framework import generics
from .serializers import *

class ReportApiList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

# def reportCreate(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#             address = data.get('address')
#             report = data.get('report')
#             userid = data.get('userid')
#             location = Report(address=address, message=report, userId=userid)
#             location.save()
#             return JsonResponse({'success': True})
#         except:
#             return HttpResponseBadRequest('Invalid request data')
#     else:
#         return HttpResponseBadRequest('Invalid request method')

