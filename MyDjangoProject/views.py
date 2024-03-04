from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpRequest
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import authentication
from .Serializers import serialize, messagserializer
import json


# Create your views here.


@api_view(['GET', ])
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
        getuserss = authentication.objects.filter(username=argdata['username'], password=argdata['password'])
        serializer = serialize(getuserss, many=True)
        request.session['users'] = serializer.data
        return Response(serializer.data)

    return Response('Failure')


@api_view(['POST', ])
def postusers(request, *args, **kwargs):
    argdata = request.data

    if request.method == 'POST':
        argdata = request.data
        isvalid = authentication.objects.filter(username=argdata['username']).exists()
        if isvalid == False:
            postusers = authentication.objects.create(username=argdata['username'], password=argdata['password'],
                                                      emailid=argdata['emailid'], is_active=1)
            postusers.save()
            getuserss = authentication.objects.filter(username=argdata['username'])
            serializer = serialize(getuserss, many=True)
            context = {"getdata": serializer.data, "response": "Success"}
            return Response(context)
        else:
            context = [{"Response": 'User Already Registered', "Message": '403'}]

            serializer = messagserializer(context, many=True)
            return Response(serializer.data)


@api_view(['PUT', 'GET'])
def Editusers(request, *args, **kwargs):
    if request.method == 'PUT':
        user_instance = authentication.objects.get(
            username=request.data.get('username'))  # self.get_object(id,request.data.id)
        if not user_instance:
            return Response({"message": 'User Not Registered'}, status=status.HTTP_404_NOT_FOUND)
        data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'emailid': request.data.get('emailid'),
            'is_active': request.data.get('is_active')
        }
        serializer = serialize(instance=user_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {"getdata": serializer.data, "response": "Success"}
            return Response(context)
    return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def Delete_User(request):
    argdata = request.data
    isvalid = authentication.objects.filter(username=argdata['username']).exists()

    if isvalid == True:
        users = get_object_or_404(authentication, username=argdata['username'])
        users.delete()
        context = {"response": "Success"}
        return Response(context)
    else:
        context = [{"Response": 'User Not Registered', "Message": '403'}]
        return Response(context)