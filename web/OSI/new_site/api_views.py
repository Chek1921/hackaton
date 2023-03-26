from .models import Report, UserRating
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models.functions import TruncDay
from django.db.models import Count


class ReportApiList(generics.ListCreateAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        queryset = Report.objects.all()
        userId = self.request.query_params.get('userId', None)
        print(userId)
        if userId is not None:
            queryset = queryset.filter(userId=userId)
        return queryset

class ReportApi(generics.ListAPIView):
    serializer_class = ReportPerDaySerializer
    model = Report
    queryset = Report.objects.extra(select={'day': 'date( date )'}).values('day') \
               .annotate(available=Count('date'))
    # 
    # def get_queryset(self):
        
    #     print(queryset)
    #     return queryset

class MoneyApi(APIView):
    def get(self, request):
        addresses = Address.objects.all()
        address_list = []
        money_come_list = []
        money_go_list = []
        for address in addresses:
            address_list.append(address.name)
            money_come_list.append(address.money)
            reports = Report.objects.filter(stage_id = 4, address = address.name)
            money_go = 0
            for report in reports:
                if report.cost:
                    money_go = money_go + report.cost
            money_go_list.append(money_go)
        
        return Response({'address_list': address_list, 'money_come_list': money_come_list, 'money_go_list': money_go_list})
    
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

class UserRatingApiList(generics.ListAPIView):
    serializer_class = UserRatingSerializer
    model = UserRating
    queryset = UserRating.objects.all()

    
    
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

