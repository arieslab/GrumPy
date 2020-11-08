from django.db import models


class Token(models.Model):
    tokenname = models.CharField('Name', max_length=100)
    token = models.CharField('Token', max_length=100)

    def __str__(self):
        return self.tokenname
