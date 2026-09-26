from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Expenses(models.Model):
    title=models.CharField(max_length=100)
    CATEGORY=[
        ('food','Food'),
        ('rent','Rent'),
        ('travel','Travel'),
        ('groceries','Groceries'),
        ('fuel','Fuel'),
        ('shopping','Shopping'),
        ('bills','Bills'),
        ('medical','Medical'),
        ('education','Education'),
        ('entertainment','Entertainment'),
        ('investment','Investment'),
        ('others','Others')
     ]
    category=models.CharField(max_length=100,choices=CATEGORY)
    amount=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)

class employee(models.Model):
    name=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    salary=models.PositiveBigIntegerField()
    location=models.CharField(max_length=100)

    def __str__(self):
        return self.name
