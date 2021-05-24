from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'date_of_birth', 'address']


class LogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

    # class Meta:
    #     fields = ['refresh']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(User.objects.all())])
    password = serializers.CharField(
        max_length=60, min_length=6, write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(
        max_length=60, min_length=6, write_only=True, required=True)
    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    date_of_birth = serializers.DateField()
    address = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2',
                  'name', 'phone', 'date_of_birth', 'address']

    def validate(self, attrs):
        user = User.objects.filter(
            email=attrs['email'], username=attrs['email']).first()

        if user:
            raise serializers.ValidationError({'email': 'Email is invalid'})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password field didn't match"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            name=validated_data.get('name', None),
            phone=validated_data.get('phone', None),
            address=validated_data.get('address', None),
            date_of_birth=validated_data.get('date_of_birth', None),
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
