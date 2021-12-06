from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404

from .forms import SignUpForm, LogInForm
from .models import Course



@csrf_exempt
def signup_view(request):  # реєстрація
    if request.user.is_authenticated:
        return render(request, 'oncourse/loggedin.html')
    else:
        if request.method == 'POST':
            form = SignUpForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('/oncourse/login')
            else:
                form = SignUpForm()
                return render(request, 'oncourse/signup.html', {'form': form})


@csrf_exempt
def validate_username(request):
    username = request.POST.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('oncourse:index')
    else:
        form = LogInForm()
    return render(request, "oncourse/login.html", {'form': form})


def logout_view(request):
  #  if request.method == 'POST':
        logout(request)
       # return redirect('oncourse:index')
        return render(request, "oncourse/loggedout.html")


class IndexView(ListView):
    template_name = 'oncourse/index.html'
    context_object_name = 'latest_course_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Course.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(DetailView):
    model = Course
    template_name = 'oncourse/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Course.objects.filter(pub_date__lte=timezone.now())


def UsersList(request):
    all = User.objects.all()
    context = {'all': all}
    return render(request, 'oncourse/userslist.html', context)


def view_profile(request):
    args = {'user': request.user}
    return render(request, 'oncourse/profile.html', args)



'''
def join(request):
    content_type = ContentType.objects.get_for_model(Details.course_id)
    permission = Permission.objects.create(
        codename='view_content',
        name='View content',
        content_type=content_type,
    )
    return redirect('oncourse:index')
'''
