from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from typing import Any


class SimpleUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id","email","fullname"]

    def get_fullname(self, obj:User)->str:
        return f'{obj.username} {obj.last_name}'.strip()


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('fullname', 'email', 'password', 'repeated_password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {"password": "Passwörter stimmen nicht überein"})
        return data

    def validate_email(self, value:str)->str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                {"error": "Diese Email-Adresse ist bereits vergeben"})
        return value

    def create(self, validated_data: dict[str, Any])->User:
        fullname = validated_data.pop('fullname')
        password = validated_data.pop('password')
        validated_data.pop('repeated_password')

        name_parts = fullname.strip().split()

        username = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        user = User(
            username=username,
            last_name=last_name,
            email=validated_data.get("email")
        )
        user.set_password(password)
        user.save()
        return user


class EmailAuthTokenSerializher(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, payload:dict[str,Any]):
        p_email, p_password = payload.get('email'), payload.get('password')

        try:
            user = User.objects.get(email=p_email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Email oder Passwort ist ungültig")

        user = authenticate(username=user.username, password=p_password)
        if not user:
            raise serializers.ValidationError(
                "Email oder Passwort ist ungültig.")

        payload['user'] = user
        return payload
