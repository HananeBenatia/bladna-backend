from rest_framework import serializers
from .models import User , Progress 

from django.contrib.auth import authenticate 

class SigninSerializer (serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = ['full_name' , 'age' ,'username' ,'password']
        extra_kwargs = {'password' : {'write_only' : True } }
    def create (self , validated_data): 
        user = User.objects.create_user( full_name = validated_data['full_name'] , age = validated_data['age']  , username = validated_data['username'] , password = validated_data['password'] )
        return user 
    

class LoginSerializer ( serializers.Serializer ) :
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data) :
        user = authenticate(**data)
        if user and user.is_active :
            return user
        raise serializers.ValidationError("incorrect username or password ") 
    

class SetparentsecretSerializer ( serializers.ModelSerializer ) :
    class Meta : 
         model = User
         fields = ['parent_secret']
         extra_kwargs = {'parent_secret' : {'write_only' : True } }
         def set(self,instance,validated_data):
             instance.parent_secretr= validated_data.get('parent_secret',instance.parent_secret)
             instance.save()
             return instance



class VerifyparentsecretSerializer ( serializers.Serializer ) :
    parent_secret= serializers.CharField(max_length=100)
    def validate(self, attrs):
        user = self.context['request'].user
        if user.parent_secret != attrs['parent_secret']:
            raise serializers.ValidationError("Incorrect answer")
        return attrs        
    

class ProgressSerializer (serializers.ModelSerializer) :
    class Meta :
        model = Progress
        fields = ['region' , 'score' , 'play_date']


class CoinsaddSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = User
        fields = ['score']