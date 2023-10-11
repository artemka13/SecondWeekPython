from django.shortcuts import render
from urllib import request
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.translation import gettext_lazy as _
from .forms import UserRegistrationForm, ApplicationCreateForm
from django.views import generic
from .models import Application
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy, reverse


class Index(generic.ListView):
    model = Application
    template_name = 'index.html'
    paginate_by = 5

    def get_queryset(self):
        return Application.objects.filter(status='ready')
        
    def index(request):
        application_list = Application.objects.all()
        return render(
        request, 'index.html', {"application_list": application_list})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def password_reset(request):
    return render(
        request,
        'registration/password_reset.html'
    )


class profile(generic.ListView):
    model = Application
    template_name = 'registration/profile.html'
    paginate_by = 5

    def get_queryset(self):
        ordering = self.request.GET.get('orderby')
        if ordering == 'Выполнено':
            ordering = 'ready'
        elif ordering == 'Принято в работу':
            ordering = 'load'
        elif ordering == 'Новая':
            ordering = 'new'
        elif ordering == 'Все':
            ordering = ''
        if ordering == '' or ordering == None:
            if self.request.user.is_staff:
                return Application.objects.filter()
            else:
                return Application.objects.filter(user__exact=self.request.user.id)
        else:
            if self.request.user.is_staff:
                return Application.objects.filter(status=ordering)
            else:
                return Application.objects.filter(user__exact=self.request.user.id, status=ordering)


def login(request):
    return render(
        request,
        'registration/profile.html'
    )


class view_applications(generic.ListView):
    model = Application
    template_name = 'aplications/application_list.html'
    paginate_by = 5

    def get_queryset(self):
        ordering = self.request.GET.get('orderby')
        if ordering == 'Выполнено':
            ordering = 'ready'
        elif ordering == 'Принято в работу':
            ordering = 'load'
        elif ordering == 'Новая':
            ordering = 'new'
        elif ordering == 'Все':
            ordering = ''
        if ordering == '' or ordering == None:
            if self.request.user.is_staff:
                return Application.objects.filter()
            else:
                return Application.objects.filter(user__exact=self.request.user.id)
        else:
            if self.request.user.is_staff:
                return Application.objects.filter(status=ordering)
            else:
                return Application.objects.filter(user__exact=self.request.user.id, status=ordering)


def get_error(request):
    return render(
        request,
        'aplications/error.html'
    )


class profile_main_applications(generic.ListView):
    model = Application
    template_name = 'aplications/application_list.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_of_load'] = Application.objects.filter(status='load').count()
        context['is_main'] = True;
        return context

    def get_queryset(self):
        return Application.objects.filter(status='ready')


class create_application(CreateView):
    model = Application
    template_name = 'aplications/application_form.html'
    fields = ('title', 'desc', 'img')

    def form_valid(self, form):
        fields = form.save(commit=True)
        fields.user = self.request.user
        fields.save()

        return super().form_valid(form)


class detail_application(DetailView):
    model = Application
    template_name = 'aplications/application_detail.html'


class delete_application(DeleteView):
    model = Application
    template_name = 'aplications/application_confirm_delete.html'
    success_url = reverse_lazy('profile_applications')
    success_msg = 'Запись удалена'

    def form_valid(self, form):
        print(self.object.status)
        if self.object.status != 'new':
            return redirect('error')
        else:
            self.object.delete()
            success_url = reverse_lazy('profile_applications')
            success_msg = 'Запись удалена'
            return HttpResponseRedirect(success_url, success_msg)


class update_application(UpdateView):
    model = Application
    fields = ('status', 'ready_design', 'category', 'comment')
    template_name = 'aplications/application_update.html'
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.status == 'ready':
            context['is_ready'] = True
            context['is_new'] = False
            context['is_load'] = False
        
            
        elif self.object.status == 'load':
            context['is_load'] = True
            context['is_new'] = False
            context['is_ready'] = False
        
        elif self.object.status == 'new':
            context['is_new'] = True
            context['is_ready'] = False
            context['is_load'] = False
        else:
            self.object.save()
            success_url = reverse_lazy('profile_applications')
            success_msg = 'Запись обновлена'
            return HttpResponseRedirect(success_url, success_msg)
        return context
    

    def form_valid(self, form):
        print(self.object.status)

        if self.object.status != 'ready':
            return redirect('error_update')

        else:
            self.object.save()
            success_url = reverse_lazy('profile_applications')
            success_msg = 'Запись обновлена'
            return HttpResponseRedirect(success_url, success_msg)
            

def get_error_update(request):
    return render(
        request,
        'aplications/error_update.html'
    )
