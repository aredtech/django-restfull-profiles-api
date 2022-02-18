from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from profiles_api import serializers
from .models import UserProfile, ProfileFeedItems
from .permissions import UpdateOwnProfile, UpdateOwnStatus

# Create your views here.
class HelloAPIView(APIView):
    """TEST API VIEW"""
    serializer_class = serializers.HelloAPISerializer

    def get(self, request, format=None):

        an_apiview = [
            'Uses HTTP methods as function (get, post, put, patch, delete)',
            'Is similar to traditional Django View',
            'Gives most control over your application logic',
            'is mapped manually to URLs'
        ]


        return Response({"message":"Hello", "an_apiview": an_apiview})


    def post(self, request, format=None):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"
            return Response({"message":message})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, pk=None):
        """Handle Updating an object"""

        return Response({"method": "PUT"})


    def patch(self, request, pk=None):
        """Handle a partial update of an object"""

        return Response({"method": "PATCH"})

    
    def delete(request, pk=None):
        return Response({"method" : "Delete"})


class HelloViewSet(viewsets.ViewSet):
    """Test API Viewset"""

    serializer_class = serializers.HelloAPISerializer

    def list(self, request):
        """Return a hello message"""

        an_apiviewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({"message":"Hello", "an_apiviewset":an_apiviewset})


    def create(self, request):
        
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"
            return Response({"message":message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle getting and object by its id"""
        return Response({"http_method":"GET"})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({"http_method":"PUT"})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({"http_method":"PATCH"})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({"http_method":"DELETE"})



class UserProfilesViewset(viewsets.ModelViewSet):
    """Handle Creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile, IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "email",)


class UserLoginApiView(ObtainAuthToken):
    """Handles creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



class ProfileFeedItemsView(viewsets.ModelViewSet):


    serializer_class = serializers.ProfileFeedItemSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = ProfileFeedItems.objects.all()
    permission_classes = (UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets User Profile to the logged in User"""
        serializer.save(user_profile = self.request.user)