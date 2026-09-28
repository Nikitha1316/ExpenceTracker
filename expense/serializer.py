from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from expense.models import User,Expenses

class UserSerializer(serializers.Serializer):

    id=serializers.CharField(read_only=True)
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

class ExpenseSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField(read_only=True) # to get the owner as the username 

    # serializer method feild
    # greeting=serializers.serializerMethodFeild()
    owner=serializers.SerializerMethodField()
    class Meta:
        model=Expenses
        fields='__all__'
        read_only_fields=['id','created_at']

    def get_greeting(self,obj):
        return "Hi welcome to expense tracker"
    def get_owner(self,obj):
        return obj.owner.username