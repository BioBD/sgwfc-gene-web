from django.contrib.auth import views
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from sgwf_gene.auth.forms import CreateUserForm
from sgwf_gene.mailer import alert_staff, send_email
from logger.functions import log_event
from logger.models import LogEvents

from django.db.models import Q


class PasswordChangeView(views.PasswordChangeView):
    def post(self, request):
        response = super().post(request)

        if response.status_code == 302:
            send_email(request.user.email, 4, {
                'user': request.user
            })

        log_event(request, LogEvents.USER_CHANGED_PASSWORD)

        return response


class UserLoginView(views.LoginView):
    def post(self, request):
        response = super().post(request)

        username = request.POST['username'].strip()
        if response.status_code == 302:
            log_event(request, LogEvents.USER_LOGGED_IN, description=username)
        else:
            user = None
            try:
                user = User.objects.get(Q(username=username) | Q(email=username))
            except User.DoesNotExist:
                pass

            log_event(request, LogEvents.USER_FAILED_LOGIN, user=user, description=username)

        return response

    def get_success_url(self):
        return reverse('home')


def createUserView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                is_active=False,
                is_staff=False,
                is_superuser=False,

                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],  # function automatically hashes
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.save()

            alert_staff(0, {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username']
            })

            log_event(request, LogEvents.USER_CREATED, user=user, description=f'{user.first_name} {user.last_name} ({user.email})')

            return HttpResponseRedirect(reverse('user_created'))

    else:
        form = CreateUserForm()

    context = {
        'form': form
    }

    return render(request, 'registration/create_user.html', context)


def userCreatedView(request):
    return render(request, 'registration/user_created.html')
