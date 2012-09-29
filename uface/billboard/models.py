from django.db import models
from django.contrib.auth.models import User

class BillboardUserModuleBox(models.Model):
    user = models.ForeignKey(User, unique=False)
    modname = models.CharField(max_length=200)
    posx = models.FloatField()
    posy = models.FloatField()
    def __unicode__(self):
        return self.user.username + "-" + self.modname
