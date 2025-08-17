
from django.shortcuts import render
from django.db.models import F,Func,Value,Q,Count,Max,Min,Avg,Sum
from django.db.models.functions import Concat
from store.models import Product,Customer,Collection



def say_hello(request):
    querySet=Customer.objects.annotate(
        order_count=Count('order')
    ).filter(id__gt=50)
    return render(request,'hello.html',{'name':'rakesh','orders':list(querySet)})



