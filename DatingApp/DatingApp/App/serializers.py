from rest_framework import serializers

from .models import AppUser, Sympathy


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['profile_pic', 'gender', 'first_name', 'last_name', 'email', 'password', 'lat', 'lng']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        app_user = AppUser(**validated_data)
        app_user.set_password(password)
        app_user.save()
        return app_user


class SympathySerializer(serializers.ModelSerializer):
    class Meta:
        model = Sympathy
        fields = ['from_user', 'to_user']
