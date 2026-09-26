from django.shortcuts import render
from expense.serializer import UserSerializer,ExpenseSerializer
from django.contrib.auth.models import User
from expense.models import Expenses
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.utils import timezone
# Create your views here.
class UserViewSet(ViewSet):
    def create(self,request):
        dser=UserSerializer(data=request.data)
        if dser.is_valid():
            User.objects.create_user(**dser.validated_data)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

class ExpenseViewSet(ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def create(self,request):
        dser=ExpenseSerializer(data=request.data)
        if dser.is_valid():
            dser.save(owner=request.user)
            return Response(data=dser.data,status=status.HTTP_201_CREATED)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)

    def list(self,request,pk=0):
        exp=Expenses.objects.all()
        ser=ExpenseSerializer(exp,many=True)
        return Response(data=ser.data,status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        exp = Expenses.objects.get(id=pk)
        ser = ExpenseSerializer(exp)
        return Response(data=ser.data,status=status.HTTP_200_OK)
    def destroy(self,request,pk=0):
        exp=Expenses.objects.get(id=pk).delete()
        return Response(data={"msg":"Deleted"})
    def update(self,request,pk=0):
        exp=Expenses.objects.get(id=pk)
        dser=ExpenseSerializer(data=request.data,instance=exp)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    def partial_update(self, request, pk=0):
        exp = Expenses.objects.get(id=pk)
        dser = ExpenseSerializer(instance=exp,data=request.data,partial=True)
        if dser.is_valid():
            dser.save()
            return Response(data=dser.data, status=status.HTTP_200_OK)
        return Response( data=dser.errors,status=status.HTTP_400_BAD_REQUEST)


class ExpenseSummaryView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        cur_date=timezone.now()
        cur_month=cur_date.month
        cur_year=cur_date.year
        # print(cur_month,cur_date)
        data=Expenses.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)
        category_summary=data.values('category').annotate(Sum('amount'))
        cat_summary=[summary for summary in category_summary]
        for i in category_summary:
            print(i)
        total_expense=data.values('amount').aggregate(Sum('amount'))
        print(total_expense)
        context={
            "total_expense":total_expense,
            "category_summary":cat_summary
        }
        return Response(data=context)


