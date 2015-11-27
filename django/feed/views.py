from datetime import timedelta
from django.utils.timezone import utc, now
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action, link
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics, mixins
from django.contrib.auth import get_user_model
User = get_user_model()
from notifications import notify

from feed.permissions import IsOwnerOrReadOnly, ProfessionalOnly
from feed.serializers import EntrySerializer, TextEntrySerializer, PhotoEntrySerializer, VideoEntrySerializer, EventEntrySerializer
from feed.serializers import BlogEntrySerializer, CommentSerializer, FlaggedSerializer, EntryLikeSerializer, ListEntrySerializer
from feed.serializers import SharedEntrySerializer, RelationshipTypeAheadSerializer, EntryObjSerializer
from feed.models import TextEntry, PhotoEntry, VideoEntry, BlogEntry, SharedEntry, Entry, Comment, Flagged
from schedule.models.events import Event
from user_app.models import Professional


class EntryListView(generics.ListAPIView):
    paginate_by = 10
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('-created',)

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if pk:
            try:
                user = User.objects.get(pk=pk)
                if self.request.user in user.relationships.blocking() or self.request.user in user.relationships.blockers():
                    raise # raise exception to return empty
                return Entry.objects.filter(user=pk).select_subclasses()
            except:
                #User id doesn't exist, return empty array
                return Entry.objects.none()
        else:
            #RETURNS LIST OF USERS THAT USER IS FOLLOWING
            following = self.request.user.relationships.following()
            blocking = self.request.user.relationships.blocking()
            blockers = self.request.user.relationships.blockers()
            qs= Entry.objects.filter(user__in=following).exclude(user__in=blocking).exclude(user__in=blockers).select_subclasses()

            qs2 = Entry.objects.filter(user=self.request.user)
            return qs | qs2


class EntryView(generics.RetrieveAPIView):
    model = Entry
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = EntryObjSerializer


class AbstractEntryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        following = self.request.user.relationships.following()
        blocking = self.request.user.relationships.blocking()
        blockers = self.request.user.relationships.blockers()
        qs= self.model.objects.filter(user__in=following).exclude(user__in=blocking).exclude(user__in=blockers)
        qs2 = self.model.objects.filter(user=self.request.user)
        return qs | qs2

    def post_save(self, obj, created=False):
        if type(obj.tags) is list:
        # If tags were provided in the request
            # user = User.objects.get(pk=obj.pk)
            self.model.objects.get(pk=obj).tags.set(*obj.tags)

class TextEntryViewSet(AbstractEntryViewSet):
    model = TextEntry
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = TextEntrySerializer

class PhotoEntryViewSet(AbstractEntryViewSet):
    model = PhotoEntry
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PhotoEntrySerializer

class VideoEntryViewSet(AbstractEntryViewSet):
    model = VideoEntry
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = VideoEntrySerializer

class EventEntryViewSet(AbstractEntryViewSet):
    model = Event
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = EventEntrySerializer

class BlogEntryViewSet(AbstractEntryViewSet):
    model = BlogEntry
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = BlogEntrySerializer

class SharedEntryViewSet(AbstractEntryViewSet):
    model = SharedEntry
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = SharedEntrySerializer

class CommentViewSet(viewsets.ModelViewSet):
    model = Comment
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = CommentSerializer

    def post_save(self, obj, created=False):
        notify.send(self.request.user, recipient=obj.entry.user, verb=u'left you a comment!', target=obj.entry)


class FlaggedCreateView(generics.CreateAPIView):
    model = Flagged
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = FlaggedSerializer


class EntryLikeView(generics.UpdateAPIView, generics.DestroyAPIView):
    model = Entry
    permission_classes = (IsAuthenticated,)
    serializer_class = EntryLikeSerializer

    def update(self, request, pk=None):
        user = User.objects.get(id = request.DATA.get('user_id'))
        entry =  Entry.objects.get(pk = pk)
        if entry.likes.filter(pk = user.pk).exists():
            entry.likes.remove(user)
            return Response({'user_likes':'false'}, status=status.HTTP_200_OK)
        else:
            notify.send(self.request.user, recipient=entry.user, verb=u'liked your status', target=entry)
            entry.likes.add(user)
            return Response({'user_likes':'true'}, status=status.HTTP_200_OK)


class GroupEntryView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EntrySerializer
    def get_queryset(self):
        type = self.kwargs.get('type', None)
        tag_name = self.kwargs.get('tag_name', None)
        blocking = self.request.user.relationships.blocking()
        blockers = self.request.user.relationships.blockers()
        if tag_name and not type:
            return Entry.objects.filter(tags__name=tag_name).exclude(user__in=blocking).exclude(user__in=blockers).select_subclasses()
        elif tag_name and type:
            if type == 'text':
                return TextEntry.objects.filter(tags__name=tag_name).exclude(user__in=blocking).exclude(user__in=blockers)
            elif type == 'photo':
                return PhotoEntry.objects.filter(tags__name=tag_name).exclude(user__in=blocking).exclude(user__in=blockers)
            elif type == 'video':
                return VideoEntry.objects.filter(tags__name=tag_name).exclude(user__in=blocking).exclude(user__in=blockers)
            elif type == 'event':
                return Event.objects.filter(tags__name=tag_name).exclude(user__in=blocking).exclude(user__in=blockers)
            elif type == 'blog':
                return BlogEntry.objects.filter(tags__name=tag_name).exclude(user__in=blocking).exclude(user__in=blockers)
            elif type == 'shared':
                return SharedEntry.objects.filter(tags__name=tag_name).exclude(user__in=blocking).exclude(user__in=blockers)
            return []
        else:
            return []

class ListSubEntryView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListEntrySerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        type = self.kwargs.get('type', None)
        if User.objects.filter(pk=pk).exists() and type:
            user = User.objects.get(pk=pk)
            if self.request.user in user.relationships.blocking() or self.request.user in user.relationships.blockers():
                return []
            if type == 'text':
                return TextEntry.objects.filter(user=pk).all()
            elif type == 'photo':
                return PhotoEntry.objects.filter(user=pk).all()
            elif type == 'video':
                return VideoEntry.objects.filter(user=pk).all()
            elif type == 'event':
                return Event.objects.filter(user=pk).all()
            elif type == 'blog':
                return BlogEntry.objects.filter(user=pk).all()
            elif type == 'shared':
                return SharedEntry.objects.filter(user=pk).all()
            elif type == 'transformation':
                return PhotoEntry.objects.filter(user=pk).filter(tags__name='transformation')
            return []
        else:
            return []

class ClientListView(generics.ListAPIView):
    paginate_by = 10
    serializer_class = EntrySerializer
    permission_classes = (ProfessionalOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('-created',)

    def get_queryset(self):
        pro = Professional.objects.get(id=self.request.user.id)
        connections = pro.user_connections.all()
        return Entry.objects.filter(user__in=connections).select_subclasses()


class ClientFilterView(generics.ListAPIView):
    permission_classes = (ProfessionalOnly,)
    serializer_class = ListEntrySerializer
    def get_queryset(self):
        type = self.kwargs.get('type', None)
        pro = Professional.objects.get(id=self.request.user.id)
        connections = pro.user_connections.all()
        if type:
            if type == 'text':
                return TextEntry.objects.filter(user__in=connections).all()
            elif type == 'photo':
                return PhotoEntry.objects.filter(user__in=connections).all()
            elif type == 'video':
                return VideoEntry.objects.filter(user__in=connections).all()
            elif type == 'event':
                return Event.objects.filter(user__in=connections).all()
            elif type == 'blog':
                return BlogEntry.objects.filter(user__in=connections).all()
            elif type == 'shared':
                return SharedEntry.objects.filter(user__in=connections).all()
            return []
        else:
            return []


class RelationshipTypeAheadView(generics.ListAPIView):
    serializer_class = RelationshipTypeAheadSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    search_fields = ('email', )
    paginate_by = 500
    def get_queryset(self):
        user =  self.request.user

        qs = user.relationships.followers() | user.relationships.following()

        #add pro you are connected to
        try:
            # get the professional user is connected too
            user_id = user.connection.id
            qs = qs | User.objects.filter(id=user_id)
        except:
            # no connection has been made so do nothing
            pass

        try: # if the user is a professional, grab all client data
            pro = Professional.objects.get(id=user.id)
            qs = qs|pro.user_connections.all()
        except:
            #not a professional, do nothing
            pass

        return qs.distinct()
