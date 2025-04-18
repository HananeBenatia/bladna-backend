from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User , Parent
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
    

class secret_answer_set(APIView):
     def post(self , request) :
         user = request.user
         given_answer = request.data.get('secret_answer')
         if Parent.objects.filter(user=user).exists() : 
             return Response({"detail" : "secret answer already set"}, status=status.HTTP_400_BAD_REQUEST)
         parent = Parent.objects.create(user=user , secret_answer = given_answer)
         return Response ({"detail" : " secret answer saved "} , status=status.HTTP_201_CREATED)

         
class secret_answer_verify(APIView) :
    def post(self , request) :
        user = request.user 
        given_answer = request.data.get('secret_answer')
        try : 
            parent = Parent.objects.get(user=user)
        except Parent.DoesNotExist : 
            return Response ( {"detail" : "secrect answer not set"}, status=status.HTTP_404_NOT_FOUND)
        
        if parent.secret_answer.strip().lower() == given_answer.strip().lower() :
          return Response( {"detail" : "access validated"} , status=status.HTTP_200_OK )
        else : 
            return Response ( {"detail" : "wrong answer"} , status=status.HTTP_403_FORBIDDEN)
        