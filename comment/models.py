from django.db import models

# Create your models here.


class Comment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50,unique=True)
    date = models.CharField(max_length=20)
    date = models.CharField(max_length=20)
    comment_text = models.TextField(null=True)
    commnet_value = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    type = models.BooleanField(null=True)
