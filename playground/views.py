
from django.shortcuts import render
from django.db.models import F,Func,Value,Q,Count,Max,Min,Avg,Sum
from django.db.models.functions import Concat
from store.models import Product,Customer,Collection



# Create your views here.
# view handles the request
# request -> response
def say_hello(request):
    #data insert 
    return render(request,'hello.html',{'name':'rakesh'})
    


