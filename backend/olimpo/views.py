from rest_framework import viewsets, permissions, authentication
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from olimpo.helpers import *
from rest_framework.authentication import TokenAuthentication
from olimpo.serializers import UserSerializer
from olimpo.models import *
from olimpo.serializers import *
from django.http import HttpResponse

# Create your views here.
class UserRegistrationView(APIView):
    # Use the registration serializer with its respective authentication
    serializer_class = UserRegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    # Create a new user and return a JWT
    def post(self, request):
        
        # Validate the request
        serializer = self.serializer_class(data = request.data)
        
        if serializer.is_valid(raise_exception=True):
            
            password = serializer.validated_data.get('password', None)
            confirmPassword = serializer.validated_data.get('confirmPassword', None)

            # Check if passwords match
            if password != confirmPassword:
                raise AuthenticationFailed({'confirmPassword': ['Passwords do not match']})
            
            # Save the user
            new_user = serializer.save()
            if new_user:
                # Generate an access token
                access_token = generate_access_token(new_user)
                data = {'access_token': access_token }
                response = Response(data, status=status.HTTP_201_CREATED)

                # VERY IMPORTANT: Here the authentications cookies are set, otherwise, you are COOKED.
                response.set_cookie(key = 'access_token', value = access_token, httponly=False, secure=True, samesite='None')
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    # Use serializers for the login
    serializer_class = UserLoginSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    
    def post(self, request):
        # Retrieve credentials
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        # Validate credentials
        if not password:
            raise AuthenticationFailed({'password': ['This field is required']})
        elif not email:
            raise AuthenticationFailed({'email': ['This field is required']})
        
        user_instance = authenticate(email = email, password = password)
        if not user_instance:
            raise AuthenticationFailed({'password': ['Invalid credentials']})

        if user_instance.is_active:
            # Generate an access token
            user_access_token = generate_access_token(user_instance)
            response = Response()

            # VERY IMPORTANT: Here the authentications cookies are set, otherwise, you are COOKED.
            response.set_cookie(key='access_token', value=user_access_token, httponly=False, secure=True, samesite='None', )
            response.data = {
                'access_token': user_access_token,
            }

            return response
        return Response({'message': 'Server has been destroyed to pieces. Come back later!'})

class UserLogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token')
        if user_token:
            response = Response()
            response.delete_cookie('access_token')
            response.data = {
                'message': 'User logged out successfully!'
            }
            return response
        response = Response()
        response.data = {
            'message': 'No user logged in'
        }
        return response

class UserProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthorized')
        try:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

            user_model = get_user_model()
            user = user_model.objects.filter(id = payload['user_id']).first()
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)
        
        except jwt.ExpiredSignatureError:
            response = Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie('access_token')
            return response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(activo=True)
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.filter(activo=True)
    serializer_class = ClienteSerializer

    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()

class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.filter(activo=True)
    serializer_class = DispositivoSerializer

    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.filter(activo=True)
    serializer_class = ServicioSerializer

    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()

    
class TipoDispositivoViewSet(viewsets.ModelViewSet):
    queryset = TipoDispositivo.objects.filter(activo=True)
    serializer_class = TipoDispositivoSerializer

    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
    

