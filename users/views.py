from rest_framework import viewsets, generics
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LogoutSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status


class UserViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated, ]


class RegisterView(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
