from .models import Report, UserRating
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

class ReportApiList(generics.ListCreateAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        queryset = Report.objects.all()
        userId = self.request.query_params.get('userId', None)
        print(userId)
        if userId is not None:
            queryset = queryset.filter(userId=userId)
        return queryset
    
class RatingApi(APIView):
    def post(self, request):
        data = request.data
        print(request.data)
        rating = int(data['rating'])
        reportId = int(data['reportId'])
        user = Report.objects.get(id = reportId).whos
        rating_field = UserRating.objects.get(user = user)
        rating_field.all_rating = rating_field.all_rating+rating
        rating_field.count_raiting = rating_field.count_raiting+1
        print(rating_field.all_rating, rating_field.count_raiting)
        rating_field.save()
        return Response({'title': 'OK'})

    
    
#     def reportCreate(request):
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

