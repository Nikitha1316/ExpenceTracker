from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from expense.models import User,Expenses

class UserSerializer(serializers.Serializer):

    id=serializers.CharField(read_only=True)
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expenses
        fields='__all__'
        read_only_fields=['id','created_at','owner']