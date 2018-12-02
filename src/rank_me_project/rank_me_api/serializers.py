from rest_framework import serializers
from .models import PictureItem, GradeItem, UserProfile

class ProfileSerializer(serializers.ModelSerializer):
    """A serializer for our Profile objects."""

    class Meta:
        model   = UserProfile
        fields  = (
            'id',
            'email',
            'name',
            'password',
            'age',
            'gender',
            'preference',
            'given_grades_amount',
            'main_profile_picture'
            )
        extra_kwargs = {'password': {'write_only': True}}

    # We want to override the 'create' function in order to encrypt the password.
    def create(self, validated_data):
        """Create and return a new user."""
        user = UserProfile(
            email    = validated_data['email'],
            name     = validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        self.password = set_password(self.password)
        return super(ProfileSerializer, self).update(instance, validated_data)
        #instance.email = validated_data.get('email', instance.email)
        #instance.name = validated_data.get('name', instance.name)
        #instance.password = validated_data.get('password', instance.password)
        #instance.age = validated_data.get('age', instance.age)
        #instance.gender = validated_data.get('gender', instance.gender)
        #instance.preference = validated_data.get('preference', instance.preference)
        #instance.given_grades_amount = validated_data.get('given_grades_amount', instance.given_grades_amount)
        #instance.name = validated_data.get('name', instance.name)
        #instance.main_profile_picture = validated_data.get('main_profile_picture', instance.main_profile_picture)
        instance.save()
        return instance


class PictureItemSerializer(serializers.ModelSerializer):
    class Meta:
        model   = PictureItem
        fields  = [
            'id',
            'profile', # Indicates the user (picture's owner).
            'comment',
            'picture',
            'timestamp',
        ]
        read_only_fields = ['id', 'profile', 'timestamp']


class GradeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model   = GradeItem
        fields  = [
            'id',
            'picture',
            'comment',
            'grading_profile',
            'grade',
            'timestamp',
        ]
        read_only_fields = ['id', 'grading_profile', 'timestamp']
