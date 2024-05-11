from django.contrib.auth.hashers import make_password
from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            # 'first_name',
            # 'last_name',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError("password not matched")
        attrs['password'] = make_password(attrs['password'])
        return attrs

    # def to_representation(self, instance):
    #     token_ser = TokenObtainPairSerializer()
    #     refresh = token_ser.get_token(instance)
    #     data = {
    #         "refresh": str(refresh),
    #         "access": str(refresh.access_token)
    #     }
    #     return data


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
