from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import get_user_by_id
from .serializers import LoginInputSerializer, UserOutputSerializer
from .services import login_user


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, tokens = login_user(**serializer.validated_data)

        return Response(
            {
                'message': 'Login successful',
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'user': UserOutputSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user_by_id(user_id=request.user.id)
        return Response(UserOutputSerializer(user).data)