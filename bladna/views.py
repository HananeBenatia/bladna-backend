from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User 
from .serializers import SigninSerializer , LoginSerializer , SetparentsecretSerializer , VerifyparentsecretSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
# Create your views here.  


class user_signin(APIView) :
    def post(self , request) :
        serializer = SigninSerializer(data = request.data)
        if serializer.is_valid():
           serializer.save (raise_exception=True)
           return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response ( serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class user_login(APIView): 
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data  # this is the authenticated user
            user_data = SigninSerializer(user).data  # serialize user info to send back
            token = AccessToken.for_user(user)
            return Response({
                'token': str(token),  # Return just the token
                'user': SigninSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

'''class secret_answer_set(APIView):
     permission_classes = [IsAuthenticated]
     def post(self , request) :
         user = request.user
         given_answer = request.data.get('secret_answer')
         if Parent.objects.filter(user=user).exists() : 
             return Response({"detail" : "secret answer already set"}, status=status.HTTP_400_BAD_REQUEST)
         parent = Parent.objects.create(user=user , secret_answer = given_answer)
         return Response ({"detail" : " secret answer saved "} , status=status.HTTP_201_CREATED)'''

         
'''class secret_answer_verify(APIView) :
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
            return Response ( {"detail" : "wrong answer"} , status=status.HTTP_403_FORBIDDEN)'''
        


class secret_answer_set(APIView):
     permission_classes = [IsAuthenticated]
     def post(self,request): 
         serializer= SetparentsecretSerializer(instance = request.user , data = request.data)
         if serializer.is_valid():
             serializer.save()
             return Response( {"detail" : "parent secret set"} , status=status.HTTP_200_OK )
         return Response({"detail" : "secret answer not set"}, status=status.HTTP_400_BAD_REQUEST)


class secret_answer_verify(APIView):
     permission_classes = [IsAuthenticated]
     def post(self, request):
        serializer = VerifyparentsecretSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            return Response(
                {"detail": "parent secret verified"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "wrong answer"},
            status=status.HTTP_400_BAD_REQUEST
        )
             
