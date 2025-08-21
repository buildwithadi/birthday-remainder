from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

# Create a router and register the ContactViewSet with it.
"""
A router is a tool that automatically generates URL patterns for your ViewSet classes. Instead of manually creating a separate URL path for each of your CRUD (Create, Read, Update, Delete) operations, a router handles all of that for you with a single line of code. 
"""
router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')

# The URL pattern for the API
urlpatterns = [
    path('', include('router.urls')),
]
