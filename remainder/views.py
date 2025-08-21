from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Contact, EmailReminder
from .serializer import ContactSerializer, UserRegistrationSerializer, UserLoginSerializer, EmailRemainderSerializer

"""
This is a viewset for viewing and editing Contact instances.
It provides CRUD operations.

"""
class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user).order_by('name')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# API view for user registration
# Allows new users to create an account
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


# API view for user login
# Return an authenticateion token on successful login.
class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Get or create a new authenticatoin token for the user
        token, created = Token.objects.get_or_create(user = user)

        return Response({
            "token" : token.key,
            "username" : user.username,
            "email" : user.email,
        }, status=status.HTTP_200_OK)
    
class EmailRemainderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmailRemainderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Return a list of all email remainder sent to the currently authenticated user.
    def get_queryset(self):
        return EmailReminder.objects.filter(contact__user=self.request.user).order_by('-sent_at')