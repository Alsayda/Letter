# chat/views.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User,UserContact
from .serializers import UserSerializer , UserContactsSerializer , ContactsSerializer
import bcrypt



def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def login(request):
    return render(request, "chat/login.html")


#define an api for logging in the user 

#define a class that handles the actuall login and sighup. 

# Userlogin should accept a post request and return the user profile in case the login is successfull. 
class UserLogin(APIView):
    def post(self,request):
        email = request.data.get('email',"")
        phone_num = request.data.get('phone_num', "")
        password = request.data.get("password" , "")

        if not (email or phone_num):
            return Response({'error' : 'Please provide atleast email or phone number'} , status=status.HTTP_404_NOT_FOUND)
        if not password:
            return Response({"error": "No password provided"} , status=status.HTTP_400_BAD_REQUEST)

        if email:
            user_profile = User.objects.get(email = email)
        elif phone_num:
            user_profile = User.objects.get(phone_num =phone_num)
        
        if not user_profile:
            return Response({"error":"No User found with the currect credentials"},status=status.HTTP_404_NOT_FOUND)
    
        if bcrypt.checkpw(password.encode('utf-8'), user_profile.password.encode('utf-8')):
            curr_user_serializer = UserSerializer(user_profile)
            return_data = curr_user_serializer.data
            return_data.pop('password')
            return Response(return_data,status=status.HTTP_200_OK)

        return Response({'error':'Incorrect Password'},status=status.HTTP_404_NOT_FOUND)
    
class UserSignup(APIView):
    # This api will help the user in signing up with an account. 
    def post(self,request):
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        phone_num = request.data.get('phone_num', "")
        email = request.data.get('email', "")
        password = request.data.get('password', "")

        if not (first_name,last_name,email,password,phone_num):
            return Response({"error":"You must provide a value for First name, last name, email, phone number and password"},status=status.HTTP_400_BAD_REQUEST)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

        new_user_data = {
            "first_name" : first_name,
            "last_name" : last_name,
            "phone_num" : phone_num,
            "email" : email,
            "password" : hashed_password
        }

        curr_user_serializer = UserSerializer(data=new_user_data)

        if curr_user_serializer.is_valid():
            curr_user_serializer.save()
            new_user_data.pop('password')
            return Response(new_user_data)

        return Response(curr_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
#Define views for the user to connect with their contacts: 
# Views to get all connections for the current User
# Views to add a new connection to the current User 
# Views to delete a connection from the user contact list 

class UserContact(APIView):
    #The endpoint to get all connections for a particular user
    def get(self,request):
        user_id = request.data.get('id',"")

        if not user_id:
            return Response({"error":"A User ID is required to get contact list"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_id = int(user_id)
            user_object = User.objects.get(id=user_id)
        except ValueError:
            return Response({"error":"Invalid User ID, ID Needs to be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error":"Invalid User ID, No such ID exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        contact_list = user_object.get_contact_names_and_id()
        
        return Response(contact_list)
    
    def post(self,request):
        user_id =  request.data.get("id")
        contact_name = request.data.get("contact_name")
        contact_phone_num = request.data.get("contact_phone_num")

        if not (user_id and contact_name and contact_phone_num):
            return Response({"error": "Invalid Data provided"} , status=status.HTTP_400_BAD_REQUEST)
        
        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error":f"Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contact_obj = User.objects.get(phone_num=contact_phone_num)
            contact_id = contact_obj.id
        except User.DoesNotExist:
            return Response({"error":f"User with phone numer {contact_phone_num} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        contact_data = {
            "user" : user_id,
            "contact" : contact_id,
            "contact_name" : contact_name
        }

        contact_obj = ContactsSerializer(data=contact_data)

        if contact_obj.is_valid():
            contact_obj.save()
            return Response({"success": "Contact added successfully"}, status=status.HTTP_201_CREATED)
    
        return Response(contact_obj.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        user_id =  request.data.get("id")
        contact_phone_num = request.data.get("contact_phone_num")

        if not (user_id  and contact_phone_num):
            return Response({"error": "Invalid Data provided"} , status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_obj = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error":f"Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contact_obj = User.objects.get(phone_num=contact_phone_num)
        except User.DoesNotExist:
            return Response({"error":f"User with phone numer {contact_phone_num} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        user_obj.contacts.remove(contact_obj)

        return Response({"success": "Contact deleted successfully"}, status=status.HTTP_200_OK)
        
