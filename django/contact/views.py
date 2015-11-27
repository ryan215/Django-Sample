#Django Libs
from django.core.mail import send_mail
#Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import serializers
#Serializers
from .serializers import ContactSerializer



@api_view(['POST'])
@permission_classes((AllowAny,))
def contact(request):
    serialized = ContactSerializer(data = request.DATA)
    if serialized.is_valid():
        data = {field: data for (field, data) in request.DATA.items()}
        email = data['email']
        subject = 'Contacted Us by ' + data['name']
        message = data['message']
        send_mail(subject, message, email, ['info@liveeverfit.com'])
        return Response({'details':['Success Email']}, status=status.HTTP_200_OK)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)