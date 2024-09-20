from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Admin_Register(models.Model):
    a_username = models.CharField(max_length=50)
    a_password = models.CharField(max_length=128) 

    def __str__(self):
        return self.a_username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)