Использованный источник: https://labpys.com/how-to-create-crud-api-in-django-rest-framework/

0. Создайте новый проект (выбор Django при создании нового проекта в Pycharm)
1. Выполните команду в директории вашего проекта:
Pip install Django
[ОПЦИОНАЛЬНО] Выполнить следующую команду в директории вашего проекта, если у вас устаревшая версия pip:
python.exe -m pip install --upgrade pip
2. Выполните команду в директории вашего проекта:
Pip install djangorestframework
3. Проверьте код в файле settings.py в папке с названием вашего проекта:

INSTALLED_APPS = [
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.messages',
   'django.contrib.staticfiles',
   'Здесь Название_Вашего_Проекта',
   'rest_framework'
]

4. Теперь создайте файл models.py в этой же папке и поместите туда следующий код:

from django.db import models
 
# Create your models here.
 
 
class authentication(models.Model):    
        username = models.CharField(max_length=100)
        password = models.CharField(max_length=100)
        emailid = models.CharField(max_length=100,default=True)
        is_active = models.IntegerField()
        firstname = models.CharField(max_length=100,default=True)
        lastname = models.CharField(max_length=100,default=True)
        address = models.CharField(max_length=100,default=True)
        contactno = models.CharField(max_length=100,default=True)
        gender = models.CharField(max_length=100,default=True)        
         
        def __str__(self):
            return self.username

5. Выполните команду в директории вашего проекта:
Python manage.py migrate --run-syncdb
6. Создайте файл serializers.py в папке с названием вашего проекта (в той же, где settings.py) и добавите туда код:

from rest_framework import serializers
from .models import authentication
 
 
class serialize(serializers.ModelSerializer):
    class Meta:
        model = authentication
        fields =['id','username','password','emailid']
 
 
class messagserializer(serializers.Serializer):
  Response = serializers.CharField()
  Message = serializers.CharField()

7. Создайте файл views.py в этой же папке и добавьте туда код:

from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.http import HttpResponse,HttpRequest
from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse
from django.contrib import messages 
from django.contrib.auth import authenticate
from .models import authentication
from .serializers import serialize,messagserializer
import json
  
# Create your views here.
 
 
@api_view(['GET',])
def getusers(request):
    if request.method == 'GET':
        getusers = authentication.objects.all()
        serializer = serialize(getusers, many=True)
        request.session['users'] = serializer.data
        return Response(serializer.data)
 
 
@api_view(['GET'])
def getusersid(request):
 
     
    if request.method == 'GET':
        argdata = request.data
        getuserss = authentication.objects.filter(username=argdata['username'] , password=argdata['password'])
        serializer = serialize(getuserss, many=True)
        request.session['users'] =serializer.data
        return Response(serializer.data)
     
    return Response('Failure')
 
 
@api_view(['POST',])
def postusers(request, *args, **kwargs):
    argdata = request.data
    
    if request.method == 'POST':
        argdata = request.data
        isvalid = authentication.objects.filter(username=argdata['username']).exists()
        if isvalid==False:
            postusers = authentication.objects.create(username=argdata['username'],password=argdata['password'],emailid=argdata['emailid'],is_active=1)
            postusers.save()
            getuserss = authentication.objects.filter(username=argdata['username'])
            serializer = serialize(getuserss, many=True) 
            context = {"getdata":serializer.data,"response":"Success"}               
            return Response(context)
        else:
            context = [{"Response":'User Already Registered',"Message":'403'}]
                 
            serializer = messagserializer(context, many=True) 
            return Response(serializer.data)
    
 
 
@api_view(['PUT','GET'])
def Editusers(request, *args, **kwargs):
     
     
    if request.method == 'PUT':
        user_instance =  authentication.objects.get(username=request.data.get('username')) #self.get_object(id,request.data.id)
        if not user_instance:
            return Response({"message":'User Not Registered'},status=status.HTTP_404_NOT_FOUND)
        data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'emailid': request.data.get('emailid'),
            'is_active': request.data.get('is_active')        
        }
        serializer = serialize(instance=user_instance, data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {"getdata":serializer.data,"response":"Success"}               
            return Response(context)
    return Response(serializer._errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def Delete_User(request):
    argdata = request.data
    isvalid = authentication.objects.filter(username=argdata['username']).exists()
          
    if isvalid==True:
        users = get_object_or_404(authentication,username=argdata['username'])
        users.delete()
        context = {"response":"Success"}               
        return Response(context)
    else:
        context = [{"Response":'User Not Registered',"Message":'403'}]
        return Response(context)

8. Создайте файл myurls.py в этой же папке и добавьте туда следующий код:

from django.contrib import admin
from django.urls import path,include
from . import views
  
 
urlpatterns = [    
         
    path('getusers/',views.getusers, name="getusers"),
    path('getusersid/',views.getusersid, name="GetUseById"),
    path('Addusers/',views.postusers, name="postusers"),
    path('Editusers/',views.Editusers, name="Editusers"),
    path('Delete_User/',views.Delete_User, name="Delete_User"),
]

9. Затем очистите файл urls.py (но можете оставить комментарии) и добавьте туда этот код:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Название_Вашего_Прокета.myurls')),
]

10. Можете запустить ваш сервер (в директории вашего проекта):
Python manage.py runserver

11. Чтобы протестировать CRUD, создайте файл requests.http и поместите в него этот код:

### Создать пользователя
POST http://127.0.0.1:8000/Addusers/
Content-Type: application/json

{
"username": "vick@example.com",
"password": "123451221",
"emailid": "2311@example.com",
"is_active": 1
}

### Получить всех пользователей
GET http://127.0.0.1:8000/getusers/

### Получить пользователя по id
GET http://127.0.0.1:8000/getusersid/
Content-Type: application/json

{
"username": "vick@example.com",
"password": "123451221"
}

### Обновить пользователя
PUT http://127.0.0.1:8000/Editusers/
Content-Type: application/json

{
"username": "vick@example.com",
"password": "1234222222",
"emailid": "vick@example.com",
"is_active": 1
}

### Удалить пользователя
DELETE http://127.0.0.1:8000/Delete_User/
Content-Type: application/json

{
"username": "vick@example.com"
}
