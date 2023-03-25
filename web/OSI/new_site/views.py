from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from new_site.forms import RegForm
from django.contrib.auth import login, logout
from django.views.generic.list import ListView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    return render(request, 'new_site/index.html', {'title' : 'Главная'})

def logout_l(request):
    logout(request)
    return redirect('index')

# Sign Up View
class RegView(CreateView):  
    form_class = RegForm
    success_url = reverse_lazy('login')
    template_name = 'new_site/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

class LogView(LoginView):
    redirect_authenticated_user = True
    template_name = "new_site/login.html"
    
    def get_success_url(self):
        return reverse_lazy('index') 
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context
    
class ReportStage1(LoginRequiredMixin,ListView):
    model = Report
    template_name = 'reports/reports_stage1.html'
    paginate_by = 10 
    context_object_name = 'reports'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жалобы'
        context['work_types'] = WorkType.objects.all()
        context['time_factors'] = TimeFactor.objects.all()
        return context
    
    def get_queryset(self):
        reports = Report.objects.filter(stage = Stage.objects.get(id = 1))
        return reports
    
    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.allows == '3':
            form_data = self.request.POST
            report = Report.objects.get(pk = form_data['el_pk'])
            report.time_factor = TimeFactor.objects.get(pk = form_data['time_factor'])
            report.work_type = WorkType.objects.get(pk = form_data['work_type'])
            report.stage = Stage.objects.get(id = 2)
            report.save()
            return redirect('rep1')
        else:
            return redirect('login')
        
class ReportStage2(LoginRequiredMixin,ListView):
    model = Report
    template_name = 'reports/reports_stage2.html'
    paginate_by = 10 
    context_object_name = 'reports'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жалобы'
        context['time_factors'] = TimeFactor.objects.all()
        context.update({
            
        })
        return context
    
    def get_queryset(self):
        reports_1 = Report.objects.filter(time_factor_id = 1, stage_id = 2, work_type_id = self.request.user.work_type_id)
        reports_2 = Report.objects.filter(time_factor_id = 2, work_type_id = self.request.user.work_type_id)
        reports = reports_1 | reports_2
        return reports
    
class ReportStage3(LoginRequiredMixin,ListView):
    model = Report
    template_name = 'reports/reports_stage3.html'
    paginate_by = 10 
    context_object_name = 'reports'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жалобы'
        return context
    
    def get_queryset(self):
        reports = Report.objects.filter(stage = Stage.objects.get(id = 3), whos = self.request.user)
        return reports
    
class UserList(ListView):
    model = CustomUser
    template_name = 'new_site/user_list.html'
    paginate_by = 10 
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return context
    
    def get_queryset(self):
        reports = CustomUser.objects.filter(allows = '1')
        return reports

class CreateWorkType(CreateView):
    model = WorkType
    template_name = 'new_site/new_prof.html'
    fields = ['name']

def user_add(request, user_pk):
    user = CustomUser.objects.get(pk = user_pk)
    user.allows = 2
    user.save()
    return redirect('user_list')
    
def report_to_me(request,rep_id):
    if request.user.allows == '2':
        report = Report.objects.get(id = rep_id)
        report.stage = Stage.objects.get(id = 3)
        report.whos = request.user
        report.save()
        return redirect('rep2')
    else:
        return redirect('index')
    
def report_cmplt(request,rep_id):
    report = Report.objects.get(id = rep_id)
    if request.user.allows == '2' and report.whos == request.user:
        report.stage = Stage.objects.get(id = 4)
        report.save()
        return redirect('rep3')
    else:
        return redirect('index')

