from multiprocessing import AuthenticationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#Generating Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        '''By using this api we will be able to create a new user for that we need to give the email,name, tc(True or False) fields and 
        than it will create a new user and provide access_token and refresh_token'''
        serializer=UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        token=get_tokens_for_user(user)
        return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        '''This api will login the user if account is already created for that we need to give the correct email and password.
          If email or password anything is wrong than it will give the error. And this api also give the access_token and refresh_token'''
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.data.get('email')
        password=serializer.data.get('password')
        print(password)
        user=authenticate(email=email,password=password)
        print(email)
        
        if user is not None:
            user_serializer=UserProfileSerializer(user)

            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Success',},status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        '''This api will provide the user profile by the access_token.'''
        print(request.user)
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        '''By using this api we will be able to change the password if we know the current password, for that we need to give the old_password,new_password,confirm_new_password'''
        serializer=UserChangePasswordSerializer(data=request.data,context={'request':request})
        print(request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Password Change Successfully'},status=status.HTTP_200_OK)
    

class SendPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        '''This api is responsible to send the email. Where uid and token is provided to reset the password if we forgot the previos password.'''
        serializer=SendPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"msg":"Password Reset Link Send. Please Check Your Mail"},status=status.HTTP_200_OK)
    

class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        '''By using this api we will be able to change the password if we forgot the previous password because we got the uid and token in email by providing the 
        uid and token the password will reset.'''
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({"msg":"Password Reset Successfilly"},status=status.HTTP_200_OK)




    


    
