from django.db import models
from django.contrib.auth.models import User
#
def store(self, filename):
    url = "enb/media/users/%s/%s" % (self.user.username, filename)
    return url

class Dashboard(models.Model):
    topic = models.CharField(max_length=30)
    desc= models.TextField()
    img = models.ImageField(upload_to=store, blank = True ,null=True)
    file = models.FileField(upload_to=store, blank = True ,null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True)
    def __str__(self):
        return self.topic

class Tag(models.Model):
    name= models.CharField(max_length=30,unique=True)
    dash= models.ManyToManyField(Dashboard)
    def __str__(self):
        return self.name