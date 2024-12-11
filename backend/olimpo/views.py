from rest_framework import viewsets, permissions, authentication
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

from django.http import HttpResponse, FileResponse
import io
import logging

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

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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
            response.set_cookie(key='access_token', value=user_access_token, httponly=False, secure=True, samesite='None')
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
        response = Response()
        if user_token:
            response.set_cookie(key='access_token', value="", httponly=False, secure=True, samesite='None')
            response.data = {
                'message': 'User logged out successfully!'
            }
        else:
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
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.activo:
                return Response({'error': 'Ya existe un usuario con ese correo electrónico'}, status=400)
            else:
                user.activo = True
                user.nombres = request.data.get('nombres')
                user.apellidos = request.data.get('apellidos')
                user.cedula = request.data.get('cedula')
                user.telefono = request.data.get('telefono')
                user.is_superuser = bool(request.data.get('is_superuser'))
                user.save()
                serializer = self.get_serializer(user)
                return Response(serializer.data)
        return super().create(request, *args, **kwargs)

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

    
class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.filter(activo=True)
    serializer_class = MarcaSerializer


class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.filter(activo=True)
    serializer_class = ModeloSerializer


class TipoDispositivoViewSet(viewsets.ModelViewSet):
    queryset = TipoDispositivo.objects.filter(activo=True)
    serializer_class = TipoDispositivoSerializer

    def destroy(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
    

def service_to_pdf(request, id):

    # Create bytestream buffer
    buf = io.BytesIO()
    # Create a BaseDocTemplate
    doc = BaseDocTemplate(buf, pagesize=letter)
    # Create a frame
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    
    # Create a PageTemplate
    template = PageTemplate(id='test', frames=frame)

    
    # Add PageTemplate to the BaseDocTemplate
    doc.addPageTemplates([template])
    servicio = ServicioSerializer(instance=Servicio.objects.get(id=id)).data

    tecnico = UserSerializer(instance=User.objects.get(id=servicio['tecnico'])).data
    bullet_style = ParagraphStyle(
        name='Bullet',
        fontSize=10,
        leading=12,
        leftIndent=10,
        bulletFontName='Helvetica',
        bulletFontSize=10,
        bulletColor=colors.black,
        textColor=colors.black,
        bulletType='bullet',
        alignment=TA_LEFT,
    )
        
    headers = ['N', 'Marca', 'Modelo', 'Serial', 'Imeis', 'Reparaciones', 'Costo']

    data = [headers]

    for n, item in enumerate(servicio['dispositivos'], 1):
        marca = MarcaSerializer(instance=Marca.objects.get(id=item['dispositivo']['marca'])).data
        modelo = ModeloSerializer(instance=Modelo.objects.get(id=item['dispositivo']['modelo'])).data
        reparaciones_list = ['• ' + str(r['nombre']) for r in item['reparaciones']]
        reparaciones_paragraph = Paragraph('<br/>'.join(reparaciones_list), bullet_style)
        row = [
            n,
            Paragraph(str(marca['nombre'])),
            Paragraph(str(modelo['nombre'])),
            Paragraph(str(item['dispositivo']['serial'])),
            Paragraph(str(', '.join(item['dispositivo']['imeis']['data']) if item['dispositivo']['imeis']['data'] != ["",""] else "No")),
            reparaciones_paragraph,
            Paragraph(str(item['costo']) + "$"),
        ]
        data.append(row)

    styles = getSampleStyleSheet()
    title_style = styles['Title']  

    title = Paragraph("OLIMPO SYSTEMS", title_style)
    fecha_entrega = Paragraph("Fecha de entrada: " + str(servicio['fecha_entrega']), styles['Normal'])
    fecha_salida = Paragraph("Fecha de salida: " + str(servicio['fecha_salida']), styles['Normal'])
    cliente = Paragraph("Cliente: " + str(servicio['cliente']['nombres'] + " " + str(servicio['cliente']['apellidos'])), styles['Normal'])
    tecnico = Paragraph("Tecnico: " + str(tecnico['nombres'] + " " + tecnico['apellidos']), styles['Normal'])
    observaciones = Paragraph("Observaciones: " + str(servicio['observaciones']), styles['Normal'])
    cedula = Paragraph("Cedula: " + str(servicio['cedula']), styles['Normal'])
    costo_total = Paragraph("Total: " + str(servicio['costo_total']), styles['Normal'])
    status = Paragraph("Status: " + str(servicio['status']), styles['Normal'])
    fecha_actual = Paragraph("Fecha de emision: " + str(datetime.date(datetime.now())), styles['Normal'])
    col_widths = [16*mm, 20*mm, 20*mm, 28*mm, 20*mm, 48*mm, 16*mm]
    table = Table(data, colWidths=col_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  
        ('FONTSIZE', (0, 0), (-1, -1), 8),  
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
        ('TOPPADDING', (0, 1), (-1, -1), 6),  
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),  
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),  
        ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),  
        ('SPLITLONGWORDS', (0, 1), (-1, -1), True),  # Allow text to wrap to the next line
        ('KEEPWITHNEXT', (0, 1), (-1, -1), True),  
    ])
    table.setStyle(style)

    spacer2x = Spacer(1, 15*mm)
    spacer1x = Spacer(1, 7*mm)
    
    story = [title, fecha_entrega, fecha_salida, status, tecnico, cliente, cedula, observaciones, spacer2x, table, spacer1x, costo_total, spacer1x, fecha_actual]
    doc.build(story)
    buf.seek(0)

    
    return FileResponse(buf, as_attachment=True, filename=f'servicio-{servicio["cliente"]["cedula"]}-{servicio["fecha_entrega"]}.pdf')