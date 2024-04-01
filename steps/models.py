from django.db import models
from django.contrib import admin
from django.db.models import Sum, F

class User(models.Model):
    id_token = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)

    @classmethod
    def exist(cls, request):
        token = request.headers.get('token')
        print(token)
        if not token:
            return false
        try:
            return cls.objects.get(id_token=token)
        except:
            return False

    def __str__(self):
        return self.name


class Steps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.PositiveBigIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def get_dash_data(cls):
        return cls.objects.values('user') \
            .annotate(steps_sum = Sum('steps'), name=F('user__name'), display_name=F('user__display_name')) \
            .order_by('-steps_sum')


    def __str__(self):
        return f"{self.user.name} walked {self.steps} on {self.added_at}"

admin.site.register(User)
admin.site.register(Steps)
