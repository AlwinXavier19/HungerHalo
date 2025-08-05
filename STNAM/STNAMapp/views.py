from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            res = Response()
            res.set_cookie('access_token', data['access'], httponly=True, secure=True, samesite='Lax')
            res.set_cookie('refresh_token', data['refresh'], httponly=True, secure=True, samesite='Lax')
            res.data = {
                "msg": "Login success",
                "username": data['username'],
                "role": data['role']
            }
            return res
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        res = Response()
        res.delete_cookie('access_token')
        res.delete_cookie('refresh_token')
        res.data = {"msg": "Logged out"}
        return res


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.http import JsonResponse

class RefreshTokenView(APIView):
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get('access_token')

        # Clear expired access token
        response = JsonResponse({})  # initial response

        if access_token:
            from rest_framework_simplejwt.exceptions import InvalidToken, TokenError as AccessTokenError
            from rest_framework_simplejwt.tokens import AccessToken

            try:
                AccessToken(access_token)  # will raise if expired
            except AccessTokenError:
                response.delete_cookie('access_token')

        if not refresh_token:
            response.status_code = 400
            response.content = b'{"error": "No refresh token"}'
            return response

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            new_refresh = str(refresh)  # rotated refresh token

            response = JsonResponse({'access': new_access})
            response.set_cookie('access_token', new_access, httponly=True, secure=True, samesite='Lax')
            response.set_cookie('refresh_token', new_refresh, httponly=True, secure=True, samesite='Lax')
            return response

        except TokenError:
            response.status_code = 403
            response.content = b'{"error": "Invalid or expired refresh token"}'
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response



from rest_framework.permissions import IsAuthenticated

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.role
        })
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "message": f"Welcome to your {user.role} dashboard!",
            "username": user.username,
        }

        if user.role == 'donor':
            data["info"] = "You can donate items."
        elif user.role == 'volunteer':
            data["info"] = "You can manage pickups and deliveries."
        elif user.role == 'receiver':
            data["info"] = "You can request and track donations."
        else:
            data["info"] = "No role found."

        return Response(data)