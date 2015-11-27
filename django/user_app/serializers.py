from django import forms
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()
from rest_framework import serializers, generics
from user_app.models import Professional, UniqueLocation, Certification, Address, StaticTags
from datetime import  timedelta
from notifications import notify
from relationships.models import RelationshipStatus
Block = RelationshipStatus.objects.get(name='Blocking')

# This importation is implemented due to
# django and MTI (Multi Table inheritance)
# not allowing to do a reverse table lookup for
# a specific entry rather only the generic "Entry"
from feed.models import SharedEntry
from taggit.models import Tag


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        exclude = ('user',)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'lat', 'lng', 'gender', 'img')


class TagListSerializer(serializers.WritableField):

    def from_native(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")
        return data

    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj


class SettingsProfessionalSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='email', required=False)
    img = serializers.ImageField(allow_empty_file=True, required=False)
    certifications = CertificationSerializer(many=True, allow_add_remove=True)
    primary_address = AddressSerializer(required=False)
    tags = TagListSerializer(required=False)

    class Meta:
        model = Professional
        fields = ('email', 'img', 'certifications','id', 'first_name', 'last_name', 'tier', 'gender',
                'location', 'lat', 'lng', 'twitter', 'facebook', 'instagram', 'youtube', 'linkedin', 'plus',
                'bio', 'referred_by', 'shopify_id', 'chargify_id', 'stripe_id', 'url', 'phone', 'primary_address',
                'profession', 'is_accepting', 'queue', 'fitness_sales_experience', 'education', 'date_joined', 'tags')

        exclude = ('password', 'is_superuser', 'connection', 'groups', 'user_permissions', "customer_list")


class SettingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id', required=True)
    first_name = serializers.CharField(source='first_name', required=False)
    last_name = serializers.CharField(source='last_name', required=False)
    email = serializers.EmailField(source='email', required=False)
    last_login_on = serializers.DateTimeField(source='last_login',read_only=True)
    joined_on = serializers.DateTimeField(source='date_joined', read_only=True)
    img = serializers.ImageField(allow_empty_file=True, required=False)
    referred_by = SettingsProfessionalSerializer(required=False)
    primary_address = AddressSerializer(required=False)
    tags = TagListSerializer(required=False)

    class Meta:
        model = User
        exclude = ('password','is_superuser','connection','groups','user_permissions',)


    def to_native(self, value):
        obj = super(SettingsSerializer, self).to_native(value)
        tags =  obj.get('tags')
        user_tier = obj.get('tier')
        user_id = obj.get('id')
        if user_tier == 7 or user_tier == 6:
            if Professional.objects.filter(pk = user_id).exists():
                pro = Professional.objects.get(pk=user_id)
                obj = SettingsProfessionalSerializer(instance=pro).data
                obj['shopify_sales'] = pro.shopify_sales()
            obj['type'] = 'professional'
            obj['tags'] = tags
        elif user_tier <= 5 and user_tier >= 2:
            obj['type'] = 'upgraded'
        else:
            obj['type'] = 'user'
        return obj


class ProfileProfessionalSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='email', required=False)
    img = serializers.ImageField(allow_empty_file=True, required=False)
    certifications = CertificationSerializer(many=True, allow_add_remove=True)
    tags = serializers.Field(source='tags.all')
    referrals = UserSerializer(source="user_reference.all")
    def to_native(self, value):
        obj = super(ProfileProfessionalSerializer, self).to_native(value)
        obj['clients'] = value.user_connections.count()
        value.save()
        return obj
    class Meta:
        model = Professional
        exclude = ('password', 'is_superuser', 'connection', 'groups', 'user_permissions', "customer_list",
                    'tier', 'referred_by', 'shopify_id', 'chargify_id', 'stripe_id', 'phone', 'is_professional',
                    'is_upgraded', 'is_superuser', 'primary_address', 'is_staff', 'queue', 'following', 'relationships')


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id', required=True)
    first_name = serializers.CharField(source='first_name', required=False)
    last_name = serializers.CharField(source='last_name', required=False)
    last_login_on = serializers.DateTimeField(source='last_login',read_only=True)
    joined_on = serializers.DateTimeField(source='date_joined', read_only=True)
    img = serializers.ImageField(allow_empty_file=True, required=False)
    tags = TagListSerializer(required=False)

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'connection', 'groups', 'user_permissions', 'primary_address', 'following', 'relationships')

    def to_native(self, value):
        obj = super(ProfileSerializer, self).to_native(value)
        tags =  obj.get('tags')
        user_tier = obj.get('tier')
        user_id = obj.get('id')
        if user_tier == 7 or user_tier == 6:
            if Professional.objects.filter(pk = user_id).exists():
                pro = Professional.objects.get(pk=user_id)
                obj = ProfileProfessionalSerializer(instance=pro).data
            obj['type'] = 'professional'
            obj['tags'] = tags
        elif user_tier <= 5 and user_tier >= 2:
            obj['type'] = 'upgraded'
        else:
            obj['type'] = 'user'
        #data about user logged in accessing this profile
        user = self.context['request'].user

        obj['likes'] = value.entries_liked.count() + value.video_like.count()
        print obj['likes']
        obj['fanatics'] = value.relationships.followers().count()
        obj['fanatics_list'] = UserSerializer(value.relationships.followers()).data
        obj['inspiration'] = SharedEntry.objects.filter(entry__user=value).count() +  value.comments.count()
        # if the value of USER is the same as the logged in users
        # connection then they are connected

        if user.connection and value.pk == user.connection.pk:
            obj['user_connected'] = True
        else:
            obj['user_connected'] = False

        if (user.connected_on and ((now()  - user.connected_on ) < timedelta(days=30))) or user in value.relationships.blocking():
            obj['user_can_connect'] = False
        else:
            obj['user_can_connect'] = True

        # check if user is following this profile
        if value.relationships.followers().filter(pk=user.pk).exists():
            obj['user_follows'] = True
        else:
            obj['user_follows'] = False

        if value.relationships.blockers().filter(pk=user.pk).exists():
            obj['user_blocks'] = True
        else:
            obj['user_blocks'] = False

        # If logged in user likes this user
        obj['user_likes'] = value.likes.filter(pk=user.pk).exists()
        return obj


class UserLikeSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('id', "user_id",)

    def to_native(self, value):
        obj = super(UserLikeSerializer, self).to_native(value)
        user = User.objects.get(email=obj['user_email'])
        # best quick solution for M2M, django doesn't provide
        # a clean solution.
        if value.likes.filter(pk=user.pk).exists():
            obj['user_likes'] = False
            value.likes.remove(user)
        else:
            obj['user_likes'] = True
            value.likes.add(user)

        return obj


class FollowUserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('id', "user_id",)

    def to_native(self, value):
        obj = super(FollowUserSerializer, self).to_native(value)
        user = User.objects.get(id=obj['user_id'])

        if value.relationships.following().filter(pk=user.pk).exists():
            obj['user_follows'] = False
            value.relationships.remove(user)
        else:
            obj['user_follows'] = True
            value.relationships.add(user)
            notify.send(value, recipient=user, verb=u'is following you', target=value)
        return obj

class BlockUserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('id', "user_id",)

    def to_native(self, value):
        obj = super(BlockUserSerializer, self).to_native(value)
        user = User.objects.get(id=obj['user_id'])

        if value.relationships.blocking().filter(pk=user.pk).exists():
            obj['user_blocks'] = False
            value.relationships.remove(user, Block)
        else:
            obj['user_blocks'] = True
            value.relationships.add(user, Block)

        return obj


class ConnectUserSerializer(serializers.ModelSerializer):
    professional_id = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('id', "professional_id",)

    def to_native(self, value):
        obj = super(ConnectUserSerializer, self).to_native(value)
        value.connection = Professional.objects.get(pk=obj.get('professional_id'))
        value.connected_on = now()
        obj['user_connected'] = True
        value.save()
        notify.send(value, recipient=value.connection, verb=u'has connected to you!', target=value)
        notify.send(value.connection, recipient=value, verb=u'connected!', target=value.connection)

        email = EmailMessage()
        email.subject = "Connected To New Trainer"
        email.body = 'Complete attached document and send back to your Trainer'
        email.from_email = value.connection.email
        email.to = [ value.email, ]
        email.attach_file("email/Client Questionarre-ReleaseEverFIT.docx")
        email.send()

        return obj

    def validate_professional_id(self, attrs, source):
        if Professional.objects.filter(pk=attrs['professional_id']).exists():
            pass
        else:
            raise serializers.ValidationError("Must be a Professional")

        pro = Professional.objects.get(pk=attrs['professional_id'])
        if not pro.is_accepting:
            raise serializers.ValidationError("Professional is currently not accepting")



        user = self.context['request'].user
        if user in pro.relationships.blocking():
            raise serializers.ValidationError("Professional is currently blocking")

        if user.connected_on and ((now()  - user.connected_on ) < timedelta(days=30)):
            raise serializers.ValidationError("Cannot change professional for 30 days")
        return attrs


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniqueLocation
        fields = ('location',)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        widget=forms.PasswordInput(),
        required=False
    )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.SlugRelatedField(many=True,
                                               slug_field='codename',
                                               queryset=Permission.objects.all())

    class Meta:
        model = Group
        fields = ('url', 'name', 'permissions')


class ProfessionalListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='email', required=False)
    img = serializers.ImageField(allow_empty_file=True, required=False)
    class Meta:
        model = Professional
        fields = ('id',"first_name", "last_name", "profession", "gender", "location", "is_accepting", "img", 'lat', 'lng', 'queue',)

class UserListSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(allow_empty_file=True, required=False)
    full_name = serializers.Field(source="get_full_name")
    class Meta:
        model = Professional
        fields = ('id', "full_name",  "img",)


class ClientListSerializer(serializers.ModelSerializer):
    full_name = serializers.Field(source="get_full_name")
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'img')


class ModifyMembershipSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='email', required=False)

    class Meta:
        model = User

    def to_native(self, value):
        #do not use this function until it's fix, this does not modify, it only cancels the membership
        obj = super(ModifyMembershipSerializer,self).to_native(value)
        value.stripe_cancel_subscription()
        value.cancel_professional()


class CreditcardSerializer(serializers.ModelSerializer):
    creditcard = serializers.Field(source='stripe_get_creditcard')

    class Meta:
        model = User
        fields = ('id', 'creditcard',)


class PaymentSerializer(serializers.ModelSerializer):
    stripeToken = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','stripeToken',)

    def to_native(self, value):
        obj = super(PaymentSerializer,self).to_native(value)
        stripe_token = obj.get('stripeToken')
        value.stripe_edit_creditcard(stripe_token)
        value.stripe_update_subscription()


class GroupTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'img')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class StaticTagSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=False)
    class Meta:
        model = StaticTags

    def to_native(self, value):
        obj = super(StaticTagSerializer, self).to_native(value)
        return obj.get('tags')

