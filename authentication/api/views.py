from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, EmailAuthTokenSerializher, SimpleUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class ResgistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token = Token.objects.create(user=saved_account)
            data = {
                'token': token.key,
                'fullname': f'{saved_account.username} {saved_account.last_name}',
                'email': saved_account.email,
                'user_id': saved_account.id
            }
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)


class CustomLoginView(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializher

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account: User = serializer.validated_data['user']
            token: Token = Token.objects.get(user=saved_account)
            data = {
                'token': token.key,
                'fullname': f'{saved_account.username} {saved_account.last_name}',
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)


class EmailCheckView(APIView):
    def get(self, request):

        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'no valid or missing email'}, status=400)

        try:
            user = User.objects.get(email=email)
            user_data = SimpleUserSerializer(user).data
            return Response(user_data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
