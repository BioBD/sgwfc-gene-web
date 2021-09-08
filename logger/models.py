from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _U


class LogEvents(models.IntegerChoices):
    USER_LOGGED_IN = 1, _U('Usuário fez login')
    USER_LOGGED_OUT = 2, _U('Usuário fez logout')
    USER_CHANGED_PASSWORD = 3, _U('Usuário mudou a senha')
    USER_CREATED = 4, _U('Usuário criado')
    USER_FAILED_LOGIN = 5, _U('Usuário falhou no login')
    USER_ASKED_FOR_PASSWORD_RESET = 6, _U('Usuário pediu redefinição de senha')
    USER_RESET_PASSWORD = 7, _U('Usuário redefiniu senha')


class Log(models.Model):
    log_id = models.AutoField(primary_key=True)
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(auto_now_add=True)
    event = models.IntegerField(choices=LogEvents.choices)
    description = models.CharField(max_length=200, null=True)


class EmailTypes(models.Model):
    email_type = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    template_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'email_types'
