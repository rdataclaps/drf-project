from django.forms import ValidationError
from rest_framework import serializers
from account.models import User
from django.contrib.auth.hashers import make_password
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from account.utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
    #Valiating password and password2 is same while Registration
    def validate(self,data):
        password=data.get('password')
        password2=data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match")
        return data
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']
        

class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        print(user,"=====================")
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({'old_password': 'Incorrect old password'})

        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({'confirm_new_password': 'Passwords do not match'})

        return data

    def save(self):
        user = self.context['request'].user
        print(user,"--------------------------")
        new_password = self.validated_data['new_password']

        user.password = make_password(new_password)
        user.save()

        return user
    
class SendPasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    
    def validate(self,data):
        email=data.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            # print('Encoded',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            # print("PasswordResetToekn",token)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            # print('Password Reset Link',link)
            #Send Email
            body="Click of following link to reset your password: " + link
            dataa={
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email

            }
            # print(dataa)
            try:
                Util.send_email(dataa)
            except Exception as e:
                print(e)

            return data
        else:
            raise ValidationError("You are not a registered User")
        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    class Meta:
        fields=['password','password2']
    def validate(self,data):
        try:
            password=data.get('password')
            password2=data.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password Does not match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError("Token is not valid or expired")
            user.set_password(password)
            user.save()
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError("Token is not valid or expired")

