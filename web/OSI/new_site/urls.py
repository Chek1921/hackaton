"""OSI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from new_site import views
from new_site import api_views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name = 'index'),
    path('reg/', views.RegView.as_view(), name='reg'),
    path('login/', views.LogView.as_view(), name='login'),
    path('logout/', views.logout_l, name='logout'),
    path('dashboards/', views.dashboards, name='dashboards'),
    path('work/create', views.CreateWorkType.as_view(), name = 'work_create'),
    path('rep1', views.ReportStage1.as_view(), name = 'rep1'),
    path('rep2', views.ReportStage2.as_view(), name = 'rep2'),
    path('rep3', views.ReportStage3.as_view(), name = 'rep3'),
    path('user/list', views.UserList.as_view(), name = 'user_list'),
    path('user/add/<int:user_pk>', views.user_add, name = 'user_add'),
    path('rep/to_me/<int:rep_id>', views.report_to_me, name = 'rep_to_me'),
    path('rep/cmplt/<int:rep_id>', views.report_cmplt, name = 'rep_cmplt'),


    path('api/telegram/message/get', api_views.ReportApiList.as_view()),
    path('api/telegram/rating/', api_views.RatingApi.as_view()),
]   
