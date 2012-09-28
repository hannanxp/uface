from django.db import models
from django.contrib.auth.models import User

class BillboardUserModuleBox(models.Model):
    user = models.ForeignKey(User, unique=True)
    modname = models.CharField(max_length=200)
    posx = models.FloatField()
    posy = models.FloatField()
