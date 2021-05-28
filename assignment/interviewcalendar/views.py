from .models import User
from .serializers import UserSerializer
from rest_framework import generics

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
