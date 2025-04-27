from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import APIView , api_view , permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from .models import User  , Progress
from .serializers import SigninSerializer , LoginSerializer , SetparentsecretSerializer , VerifyparentsecretSerializer , ProgressSerializer 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from datetime import date
import logging
from django.http import JsonResponse
import json
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

logger = logging.getLogger(__name__)

class SaveprogressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            today = date.today()
            region = request.data.get('region')
            score = request.data.get('score')

            if not region or score is None:
                return Response({"error": "Region and score are required."}, status=status.HTTP_400_BAD_REQUEST)

            existing_progress = Progress.objects.filter(user=request.user, play_date=today).first()
            
            if existing_progress:
                existing_progress.delete()

            progress = Progress.objects.create(
                user=request.user,
                play_date=today,
                region=region,
                score=score
            )

            serializer = ProgressSerializer(progress)
            return Response(
                {"message": "Last progress of the day saved", "progress": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error("Error in SaveprogressView: %s", str(e), exc_info=True)
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_today_progress(request):
    try:
        today = date.today()
        progress = Progress.objects.filter(user=request.user, play_date=today).first()
        
        if progress:
            serializer = ProgressSerializer(progress)
            return Response(serializer.data)
        return Response(
            {"message": "No progress saved for today"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )         
    
@csrf_exempt
def reset_password (request) :
    if request.method != 'POST' :
        return JsonResponse ({'error' : 'Only POST method is allowed .'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try :
        data = json.loads (request.body)
        username = data.get ('username')
        newpassword = data.get ('newpassword')
        confirmpassword = data.get ('confirmpassword')
        if not username or not newpassword or not confirmpassword :
            return JsonResponse ({'error' : 'All fields are required .'}, status=status.HTTP_400_BAD_REQUEST)
        if newpassword !=confirmpassword :
            return JsonResponse ({'error' : 'The passwords do not match .'}, status=status.HTTP_400_BAD_REQUEST)
        try : 
            user = User.objects.get (username=username)
        except User.DoesNotExist :
            return JsonResponse ({'error' : 'User not found.'}, status=status.HTTP_404_NOT_FOUND )
        user.password = newpassword
        user.save()
        return JsonResponse ({'error' : 'Reset password done successfully.'}, status=status.HTTP_200_OK )
    except json.JSONDecodeError :
        return JsonResponse ({'error' : 'Invalid json.'}, status=status.HTTP_400_BAD_REQUEST )


