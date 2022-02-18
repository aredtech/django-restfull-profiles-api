from rest_framework import serializers
from .models import UserProfile, ProfileFeedItems


class HelloAPISerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {
            "password" : {
                "write_only" : True,
                "style" : {"input_type" : "password"}
            }
        }

    def create(self, validated_data):
        """Create and Return New User"""
        user = UserProfile.objects.create_user(
            email = validated_data["email"],
            name = validated_data["name"],
            password = validated_data["password"]
        )

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileFeedItems
        fields = ['id', 'user_profile', 'status_text', 'created_on']

        extra_kwargs = {
            "user_profile" : {
                "read_only" : True
            }
        }