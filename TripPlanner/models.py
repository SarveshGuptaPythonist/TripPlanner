from django.db import models



class distanceModel(models.Model):
    source = models.CharField(max_length=20)
    dest = models.CharField(max_length=20)
    distance = models.CharField(max_length=20)
    
    def __str__(self):
        return self.source + " " + self.dest
    