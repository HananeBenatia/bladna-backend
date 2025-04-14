from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import SigninSerializer , LoginSerializer
# Create your views here.  


class user_signin(APIView) :
    def post(self , request) :
        serializer = SigninSerializer(data = request.data)
        if serializer.is_valid():
           serializer.save ()
           return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response ( serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class user_login(APIView): 
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data  # this is the authenticated user
            user_data = SigninSerializer(user).data  # serialize user info to send back
            return Response({'user': user_data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
