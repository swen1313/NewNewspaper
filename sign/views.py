from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.views.generic.edit import CreateView
from .forms import RegisterForm
from django.contrib.auth.models import Group





class RegisterView(CreateView):
   model = User
   form_class = RegisterForm
   template_name = 'sign/signup.html'
   success_url = '/'

   def form_valid(self, form):
      user = form.save()
      group = Group.objects.get_or_create(name='common')[0]
      user.groups.add(group)
      user.save()
      return super().form_valid(form)

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
      return context


@login_required
def upgrade_me(request):
   user = request.user
   authors_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       authors_group.user_set.add(user)
   return redirect('/')



class LoginView(FormView):
   model = User
   form_class = LoginForm
   template_name = 'sign/login.html'
   success_url = '/'

   def form_valid(self, form):
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(self.request, username=username, password=password)
      if user is not None:
         login(self.request, user)
      return super().form_valid(form)


class LogoutView(LoginRequiredMixin, TemplateView):
   template_name = 'sign/logout.html'

   def get(self, request, *args, **kwargs):
      logout(request)
      return super().get(request, *args, **kwargs)
