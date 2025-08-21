from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from .models import Contact, User, EmailReminder

class ContactSerializer(serializers.Serializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'date_of_birth']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        
        contact = Contact.objects.create(user = user, **validated_data)

        return contact
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.relationship = validated_data.get('relationship', instance.relationship)
        instance.save()
        return instance
    

# User Registration Serializer
class UserRegistrationSerializer(serializers.Serializer):
    
    # Serializer to handle user registration
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    # Creating a new user with a securely hashed password
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user


# User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    # Serializer to handle user login
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    # Authenticate the user based on the provided credentials
    def validate(self, data):
        username = data.get('username') # fetch all the usernames
        password = data.get('password') # fetch all the passwords

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                    return data
                else:
                    raise serializers.ValidationError('User account is disabled')
            else:
                raise serializers.ValidationError('Incorrect credentials')
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'")

# Serializer for the EmailRemainder model
# Used for reading and displaying log information    
class EmailRemainderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailReminder
        fields = ['id', 'contact', 'sent_at']
        read_only_fields = ['id', 'contact', 'sent_at']