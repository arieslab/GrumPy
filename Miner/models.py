from django.db import models


class Token(models.Model):
    tokenname = models.CharField('Name', max_length=100)
    token = models.CharField('Token', max_length=100)

    def __str__(self):
        return self.tokenname


class Miner(models.Model):
    minername = models.CharField('Name', max_length=100)  # Miner Name
    repoamount = models.IntegerField('Repo amount')  # Repo amount of listed repo
    minedamount = models.IntegerField('Mined Repo Amount')  # Mined amount
    minerstatus = models.CharField('Status', max_length=100)  # Miner task status
    minertaskid = models.CharField('Task id', max_length=100)  # Asynchronous task id
    tokenassociated = models.ForeignKey(Token, on_delete=models.CASCADE)


    def __str__(self):
        return self.minername
