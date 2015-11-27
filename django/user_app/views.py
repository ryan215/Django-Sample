from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import generics

from .filters import UserFilter, GenderFilterBackend, ProfessionFilterBackend, LocationFilterBackend, AcceptingFilterBackend, TagFilterBackend
from .filters import OwnerFilterBackend, QueueFilterBackend
from .serializers import SettingsSerializer, PasswordSerializer, GroupSerializer, ProfessionalListSerializer, LocationSerializer, ClientListSerializer
from .serializers import PaymentSerializer, ModifyMembershipSerializer, CreditcardSerializer, SettingsProfessionalSerializer, ProfileSerializer, UserLikeSerializer
from .serializers import FollowUserSerializer, BlockUserSerializer, ConnectUserSerializer, GroupTagSerializer, StaticTagSerializer, UserListSerializer
from .permissions import IsAdminOrSelf, IsOwnerOrReadOnly, AuthenticatedReadOnly
from .models import Professional, UniqueLocation, StaticTags


class UserListView(generics.ListAPIView):
    paginate_by = 50
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = UserListSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('first_name', 'last_name')


class UserViewSet(generics.RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = (IsAdminOrSelf,)
    serializer_class = SettingsSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)


    def post_save(self, obj, created=False):
        if type(obj.tags) is list:
            # If tags were provided in the request
            user = User.objects.get(pk=obj.pk)
            user.tags.set(*obj.tags)


class ProfileView(generics.RetrieveAPIView):
    model = User
    permission_classes = (AuthenticatedReadOnly,)
    serializer_class = ProfileSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)

class GroupViewSet(viewsets.ModelViewSet):
    model = Group
    permission_classes = (IsAdminUser,)
    serializer_class = GroupSerializer


class LocationViewSet(viewsets.ModelViewSet):
    model = UniqueLocation
    permission_classes = (IsAuthenticated,)
    serializer_class = LocationSerializer


class ProfessionalListView(generics.ListAPIView):
    paginate_by = 50
    model = Professional
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfessionalListSerializer
    filter_backends = (GenderFilterBackend,ProfessionFilterBackend,LocationFilterBackend,AcceptingFilterBackend, TagFilterBackend, QueueFilterBackend)


    def get_queryset(self):
        return Professional.objects.filter(profession__in=['Nutritionist','Trainer','Instructor',]).order_by('-recently_viewed')


class ProfessionalObjView(generics.RetrieveUpdateDestroyAPIView):
    model = Professional
    serializer_class = SettingsProfessionalSerializer
    permission_classes = (IsAdminOrSelf,)
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)

    def post_save(self, obj, created=False):
        if type(obj.tags) is list:
            # If tags were provided in the request
            user = User.objects.get(pk=obj.pk)
            user.tags.set(*obj.tags)


class CreditcardView(generics.RetrieveAPIView):
    model = User
    permission_classes= (IsAdminOrSelf,)
    serializer_class = CreditcardSerializer
    #filter_backends =


class ClientListView(generics.ListAPIView):
    paginate_by = 50
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = ClientListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'first_name', 'last_name')


class ModifyMembershipView(generics.RetrieveAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = ModifyMembershipSerializer


class PaymentView(generics.RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = (IsAdminOrSelf,)
    serializer_class = PaymentSerializer


class UserLikeView(generics.UpdateAPIView, generics.DestroyAPIView):
    model = User
    permission_classes = (IsAdminOrSelf,)
    serializer_class = UserLikeSerializer


class FollowUserView(generics.UpdateAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowUserSerializer


class BlockUserView(generics.UpdateAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = BlockUserSerializer


class ConnectUserView(generics.UpdateAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = ConnectUserSerializer


class FanaticsListView(generics.ListAPIView):
    paginate_by = 500
    model = User
    permission_classes = (IsAdminOrSelf,)
    # has exact output as client, need to restructure
    # and unify/standardize this serializer
    serializer_class = ClientListSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('first_name', 'last_name',)

    def get_queryset(self):
        return self.request.user.relationships.following()


class GroupTagView(generics.ListAPIView):
    paginate_by = 500
    model = User
    permission_classes = (IsAdminOrSelf,)
    # has exact output as client, need to restructure
    # and unify/standardize this serializer
    serializer_class = GroupTagSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)

    def get_queryset(self):
        type = self.kwargs.get('type', None)
        if type:
            return User.objects.filter(tags__name=type).order_by('?')
        else:
            return []


class StaticTagViewSet(generics.ListAPIView):
    paginate_by = 50
    model = StaticTags
    permission_classes = (AllowAny,)
    serializer_class = StaticTagSerializer

