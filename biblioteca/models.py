from django.db import models

class Userr(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=30)

    def __str__(self):
        return self.name