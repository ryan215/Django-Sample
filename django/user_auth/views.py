#Django Libs
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, Template
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.timezone import utc, now
from django.utils.timezone import utc
from django.conf import settings
from django.contrib.auth.models import check_password
#Python Libs
import json
import string
import random
import datetime
#Rest Framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers
#Serializers
from .serializers import EmailSerializer, CreateUserSerializer, ReturnUserSerializer, LogoutSerializer, PasswordSerializer, ForgotPasswordSerializer, ChangePasswordSerializer, ResetPasswordSerializer, CreateProSerializer
#Models
from notifications import notify
from rest_framework.authtoken.models import Token
from user_app.models import Professional, Address, UniqueLocation, Certification, FeaturedProfessional
from django.contrib.auth import get_user_model
User = get_user_model()



def token_generator(size=5, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    serialized = CreateUserSerializer(data=request.DATA)
    if serialized.is_valid():
        user_data = {field: data for (field, data) in request.DATA.items()}
        pro_referred_by = user_data.pop('referred_by', None)
        temp_address = user_data.pop('primary_address', None)
        tags = user_data.pop('tags', None)
        user_data.pop('password2', None)
        user_data.pop('profession', None)
        user_data.pop('education', None)
        user_data.pop('experience', None)
        user_data.pop('certification_name1', None)
        user_data.pop('certification_number1', None)
        user_data.pop('certification_name2', None)
        user_data.pop('certification_number2', None)
        user_data.pop('phone', None)
        user_data.pop('twitter', None)
        user_data.pop('facebook', None)
        user_data.pop('instagram', None)
        user_data.pop('youtube', None)
        user_data.pop('linkedin', None)
        user_data.pop('plus', None)

        user = User.objects.create_user(
            **user_data
        )
        user.tags.set(*tags)
        user.save()


        if Professional.objects.filter(email = pro_referred_by).exists():
            pro_ref = Professional.objects.get(email = pro_referred_by)
            user.referred_by = pro_ref
            user.referred_by.save()
            user.relationships.add(pro_ref)
            notify.send(user, recipient=pro_ref, verb=u'is following you', target=user)

        for pro in FeaturedProfessional.objects.all():
            pro_ref = pro.professional
            user.relationships.add(pro_ref)
            notify.send(user, recipient=pro_ref, verb=u'is following you', target=user)

        try:
            city = temp_address['city']
            city = str(city)
            city = city.strip()
            state = temp_address['state']
            state = str(state)
            state = state.strip()
            temp_location = city + ', ' + state
            location = UniqueLocation.objects.get_or_create(location = temp_location)
            location[0].counter += 1
            location[0].save()
        except:
            pass

        try:
            user.location = temp_location
            user.lat = temp_address['lat']
            user.lng = temp_address['lng']
        except:
            pass

        try:
            address = Address.objects.get(id = user.primary_address.id)
            address.__dict__.update(**temp_address)
            address.save()
        except:
            pass

        email = user.email
        subject = 'Welcome to Live Ever Fit'
        message = 'Thank you for registering to Live Ever Fit'
        template = get_template('email/generic.html')
        context = Context({})
        output = template.render(context)
        msg = EmailMultiAlternatives(subject, message, 'info@liveeverfit.com', [email])
        msg.attach_alternative(output, "text/html")
        msg.send()

        response = ReturnUserSerializer(instance=user).data
        response['token'] = user.auth_token.key
        response['id'] = user.id
        response['email'] = user.email
        response['img'] = user.img.url
        tier = user.tier
        #depending on tier, depends on user dynamic type
        if tier == 7 or tier == 6:
            response['type'] = 'professional'
        elif tier <= 5 and tier >= 2:
            response['type'] = 'upgraded'
        else:
            response['type'] = 'user'

        user.shopify_create(user_data.get('password'))
        return Response(response, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register_professional(request):
    serialized = CreateProSerializer(data=request.DATA)
    if serialized.is_valid():
        user_data = {field: data for (field, data) in request.DATA.items()}
        email = user_data.pop('email', None)
        certification_name1 = user_data.pop('certification_name1', None)
        certification_number1 = user_data.pop('certification_number1', None)
        certification_name2 = user_data.pop('certification_name2', None)
        certification_number2 = user_data.pop('certification_number2', None)
        user_data.pop('password', None)
        user_data.pop('password2', None)
        user_data.pop('referred_by', None)
        user_data.pop('primary_address', None)


        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            pro = Professional.objects.create_prof(user)
        else:
            return Response({'error': 'Professional could not be created'}, status=status.HTTP_400_BAD_REQUEST)

        pro.__dict__.update(**user_data)
        if certification_name1:
            certification1 = Certification(user = pro, certification_name = certification_name1, certification_number = certification_number1)
            certification1.save()
        if certification_name2:
            certification2 = Certification(user = pro, certification_name = certification_name2, certification_number = certification_number2)
            certification2.save()
        pro.save()


        response = ReturnUserSerializer(instance=user).data
        response['token'] = user.auth_token.key
        response['id'] = user.id
        response['email'] = user.email
        response['img'] = user.img.url
        tier = user.tier
        #depending on tier, depends on user dynamic type
        if tier == 7 or tier == 6:
            response['type'] = 'professional'
        elif tier <= 5 and tier >= 2:
            response['type'] = 'upgraded'
        else:
            response['type'] = 'user'
        return Response(response, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'details':'Logged out'}, status=status.HTTP_200_OK)
    except:
        return Response({'details':'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenSerializer(serializers.Serializer):
    """
    Restfuls AuthTokenSerializer with modifications to use email rather than user
    """
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Unable to login with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password"')


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            return Response({'token': token.key, 'id': id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_auth_token = ObtainAuthToken.as_view()


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.object['user'])
            id = serializer.object['user'].id
            email = serializer.object['user'].email
            img = serializer.object['user'].img.url
            tier = serializer.object['user'].tier
            #depending on tier, depends on user dynamic type
            if tier == 7 or tier == 6:
                type = 'professional'
            elif tier <= 5 and tier >= 2:
                type = 'upgraded'
            else:
                type = 'user'
            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.save()

            return Response({'token': token.key, 'id': id, 'email':email, 'img': img, 'type': type })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_password(request):
    serialized = ChangePasswordSerializer(data = request.DATA)
    if serialized.is_valid():
        data = {field: data for (field, data) in request.DATA.items()}
        token = data['token']
        tokenObj = Token.objects.get(key = token)
        user = tokenObj.user

        if check_password(data['current_password'], user.password):
            user.set_password(data['password'])
            user.save()
            return Response({'details':['Success password changed']}, status=status.HTTP_200_OK)
        else:
            return Response({'current_password':['Wrong current password']}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def forgot_password(request):
    serialized = ForgotPasswordSerializer(data = request.DATA)
    if serialized.is_valid():
        data = {field: data for (field, data) in request.DATA.items()}
        email = data['email']
        user = User.objects.get(email = email)
        temp_password = token_generator(10)
        user.set_password(temp_password)
        user.save()

        if check_password(temp_password, user.password):
            subject = 'Password Reset'
            message = 'Change you password at http://dev.liveeverfit.com/#/reset-password/' + temp_password + '/' + user.email
            send_mail(subject, message, 'info@liveeverfit.com', [email])
            return Response({'details':['Email sent']}, status=status.HTTP_200_OK)
        else:
            return Response({'email':['Email did not send']}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def reset_password(request):
    serialized = ResetPasswordSerializer(data = request.DATA)
    if serialized.is_valid():
        data = {field: data for (field, data) in request.DATA.items()}
        email = data['email']
        user = User.objects.get(email = email)

        if check_password(data['change_password_token'], user.password):
            user.set_password(data['password'])
            user.save()
            return Response({'details':['Success password changed']}, status=status.HTTP_200_OK)
        else:
            return Response({'change_password_token':['Invalid change password token']}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)



