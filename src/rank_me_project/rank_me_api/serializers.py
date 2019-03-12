from rest_framework import serializers
from .models import PictureItem, GradeItem, UserProfile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _

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
            #'is_facebook_account'
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
        if ('password' in validated_data):
            instance.set_password(validated_data['password'])
            instance.save()
            return instance
        else:
            return super().update(instance, validated_data)

    def partial_update(self, instance, validated_data):
        if ('password' in validated_data):
            instance.set_password(validated_data['password'])
            instance.save()
            return instance
        else:
            return super().update(instance, validated_data)

        #validated_data['password'] = set_password(validated_data['password'])
        #validated_data.save()
        #return super(ProfileSerializer, self).partial_update(instance, validated_data)

        #instance.email = validated_data.get('email', instance.email)
        #instance.name = validated_data.get('name', instance.name)
        #instance.password = validated_data.get('password', instance.password)

        #instance.gender = validated_data.get('gender', instance.gender)
        #instance.preference = validated_data.get('preference', instance.preference)
        #instance.given_grades_amount = validated_data.get('given_grades_amount', instance.given_grades_amount)
        #instance.name = validated_data.get('name', instance.name)
        #instance.main_profile_picture = validated_data.get('main_profile_picture', instance.main_profile_picture)

# We need this serialized to override default email template.
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            ###### USE YOUR TEXT FILE ######
            'email_template_name': 'custom_reset_password_email.txt',
            'request': request,
        }
        self.reset_form.save(**opts)

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
        read_only_fields = ['id', 'profile']


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
        read_only_fields = ['id']
