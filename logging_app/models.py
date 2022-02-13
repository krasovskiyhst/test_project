from django.db import models


class AccessLogs (models.Model):
    ip = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=False)
    request_method = models.CharField(max_length=200)
    code_status = models.IntegerField(default=0)
    data_transfer = models.IntegerField(default=0)

    def __str__(self):
        return self.ip
