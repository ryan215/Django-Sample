from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from taggit.models import Tag
from rest_framework.authtoken.models import Token
from taggit.managers import TaggableManager
from shopify_app import shopify_call
from stripe_payments.views import*


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email),
            is_staff=False, is_active=True, is_superuser=False,
            last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


def default_ref():
    return Professional.objects.get(email='rory@heavenly-homes.com').id


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.
    Email and password are required. Other fields are optional.
    """
    #username = models.CharField(_('username'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), max_length=50, unique=True, db_index=True, )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    likes = models.ManyToManyField('self', related_name='liked', blank=True,null=True)
    #custom fields
    TIER_CHOICES = (
        (1, 'Tier 1'),
        (2, 'Tier 2'),
        (3, 'Tier 3'),
        (4, 'Tier 4'),
        (5, 'Tier 5'),
        (6, 'Grandfather Professional'),
        (7, 'Professional'),
    )
    tier = models.IntegerField(_('tier'), max_length=1, blank=True, choices=TIER_CHOICES, default=1, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(_('gender'), max_length=1, blank=True, choices=GENDER_CHOICES)
    location = models.CharField(_('location'), max_length=100, blank=True)
    lat = models.CharField(_('latitude'), max_length=30, blank=True, default="29.760193")
    lng = models.CharField(_('longitude'), max_length=30, blank=True, default="-95.369390")

    tags = TaggableManager(blank=True)

    twitter = models.CharField(_('twitter'), max_length=100, blank=True)
    facebook = models.CharField(_('facebook'), max_length=100, blank=True)
    instagram = models.CharField(_('instagram'), max_length=100, blank=True)
    youtube = models.CharField(_('youtube'), max_length=100, blank=True)
    linkedin = models.CharField(_('linkedin'), max_length=100, blank=True)
    plus = models.CharField(_('plus'), max_length=100, blank=True)

    #Image field requires the lib pillow
    img = models.ImageField(_('image'), upload_to="user_app/profile", blank=True, default='default-profile.svg')
    bio = models.CharField(_('biography'), max_length=5000, blank=True)
    referred_by = models.ForeignKey('Professional', null=True, related_name='user_reference', blank=True, default=default_ref)
    shopify_id = models.IntegerField(default=0, blank=True)
    chargify_id = models.IntegerField(default=0, blank=True)
    stripe_id = models.CharField(max_length=255, blank=True, default='')

    url = models.CharField(_('url'), max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    connection = models.ForeignKey('Professional', null=True, related_name='user_connections', blank=True)
    connected_on = models.DateTimeField(_('Connection on'), null=True, blank=True)

    primary_address = models.OneToOneField('Address', null=True, blank=True, on_delete=models.SET_NULL, related_name='owner')

    is_professional = models.BooleanField(_('is professional'), default=False)
    is_upgraded = models.BooleanField(_('is upgraded'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    recently_viewed = models.DateTimeField(_('date joined'), default=timezone.now, auto_now=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def setup(self, password, referred_by):
        self.attach_referral(referred_by)
        self.create_primary_address()
        errors = self.shopify_create(password)
        self.save()
        return errors

    def setup_upgrade(self, password, referred_by):
        self.attach_referral(referred_by)
        self.create_primary_address()
        errors = self.shopify_create(password)
        self.is_upgraded = True
        self.save()
        return errors

    def get_absolute_url(self):
        return "/profile/view?id=%s" % urlquote(self.id)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_url(self):
        url = '/profile/view?id=%s' % (self.id)
        return url.strip()

    def get_all_data(self):
        return {'name': self.get_full_name(),
                'gender': self.gender,
                'location': self.location,
                'lat': self.lat,
                'lng': self.lng,
                'url': self.get_url(),
                'img': str(self.img),
                'bio': self.bio,
                'email': self.email,
                'id': self.id,
                'facebook': self.facebook,
                'tier': self.tier,
                'is_professional': self.is_professional,
                'is_upgraded': self.is_upgraded,
        }

    def get_address(self):
        # grabs primary address
        return self.primary_address.shopify_format()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this user.

        """
        send_mail(subject, message, from_email, [self.email])

    def attach_referral(self, reference):
        if not self.referred_by:
            try:
                prof = Professional.objects.get(email=reference)
            except:
                prof = Professional.objects.get(email='rory@heavenly-homes.com')

            self.referred_by = prof
            self.save()

    def create_primary_address(self):
        if not self.primary_address:
            self.primary_address = Address.objects.empty_address()
            self.save()

    def make_professional(self):
        if not self.is_professional:
            extended_user = Professional(lefuser_ptr=self)
            extended_user.__dict__.update(self.__dict__)
            extended_user.is_upgraded = True
            extended_user.is_professional = True
            extended_user.save()
        else:
            self.is_upgraded = True
            self.save()

    def cancel_professional(self):
        self.tier = 1
        self.is_professional = False
        self.is_upgraded = False
        self.save()

    def delete_professional(self):
        # this function is called to delete a professional
        # who was not accepted
        # so it returns them back to the tier they were at
        if self.tier == 6 or self.tier == 7:
            self.tier = 1

        self.save()

    def add_to_locations(self):
        try:
            UniqueLocation.objects.get(location= self.location)
        except:
            UniqueLocation(location= self.location).save()

    # SHOPIFY FUNCTIONS
    # made them easy for insertion to a abstract base class
    shopify_create = shopify_call.customer_create
    shopify_get = shopify_call.customer_get
    shopify_edit = shopify_call.customer_edit
    shopify_delete = shopify_call.customer_delete
    shopify_orders = shopify_call.customer_orders
    shopify_meta = shopify_call.customer_metafield

    def get_shopify_id(self):
        return self.shopify_id

    #Stripe
    stripe_get_or_create_customer = get_or_create_customer
    stripe_delete_customer= delete_customer
    stripe_edit_creditcard= edit_creditcard
    stripe_get_creditcard = get_creditcard
    stripe_update_subscription= update_subscription
    stripe_cancel_subscription= cancel_subscription


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
        address = Address()
        address.save()
        instance.primary_address = address
        instance.save()

@receiver(pre_delete, sender=CustomUser)
def delete_customuser(sender, instance, **kwargs):
    instance.shopify_delete()


class AddressManager(models.Manager):
    def empty_address(self):
        new_address = self.model()
        new_address.save()
        return new_address

    def get_primary(self):
        pass


class Address(models.Model):
    """
    Standard Address Model:
    If needing in a specific format such as street_line1 should billing_street_line1
    write a custom function to deliver your data specified
    Typically custom functions used for using a 3rd party API such as Stripe or Shopify
    """
    TYPES_CHOICES = (
        ('HOME', 'Home'),
        ('WORK', 'Work'),
        ('OTHER', 'Other'),
    )
    type = models.CharField(_('Type'), max_length=20, choices = TYPES_CHOICES, blank=True,)
    firstname = models.CharField(_('Firstname'), max_length = 50, blank = True)
    lastname = models.CharField(_('Lastname'), max_length = 50, blank = True)
    department = models.CharField(_('Departement'), max_length = 50, blank = True)
    corporation = models.CharField(_('Corporation'), max_length = 100, blank = True)
    street_line1 = models.CharField(_('Address 1'), max_length = 100, blank = True)
    street_line2 = models.CharField(_('Address 2'), max_length = 100, blank = True)
    zipcode = models.CharField(_('ZIP code'), max_length = 5, blank = True)
    city = models.CharField(_('City'), max_length = 100, blank = True)
    state = models.CharField(_('State'), max_length = 100, blank = True)
    postal_box = models.CharField(_('Postal box'), max_length = 20, blank = True)
    country = models.CharField(_('Country'), max_length = 100, blank = True, default='US')
    objects = AddressManager()

    lat = models.CharField(_('latitude'), max_length=30, blank=True)
    lng = models.CharField(_('longitude'), max_length=30, blank=True)

    def __unicode__(self):
        return self.street_line1

    class Meta:
        verbose_name_plural = "Address"

    def shopify_format(self):
        """A consistant dictionary that matches shopifies
        """
        return {
            'province': self.state, 'city': self.city, 'first_name': self.owner.first_name, 'last_name': self.owner.last_name,
            'zip': self.zipcode, 'default': True, 'address1': self.street_line1,
            'address2': self.street_line2, 'phone': self.owner.phone, 'country': self.country, 'company': self.corporation
        }

    def custom_format(self):
        """A consistant dictionary that matches custom needs
        """
        return {
            'state': self.state, 'city': self.city, 'first_name': self.owner.first_name, 'last_name': self.owner.last_name,
            'zip': self.zipcode, 'default': True, 'billing_address1': self.street_line1,
            'billing_address2': self.street_line2, 'phone': self.owner.phone, 'country': self.country, 'company': self.corporation
        }


class UniqueLocation(models.Model):
    location = models.CharField(max_length=100)
    counter = models.IntegerField(default=0)

    #Metadata
    def __unicode__(self):
        return self.location

    def counter_loc(self):
        return self.counter

    def location_name(self):
        return self.location

    def get_all_data(self):
        return {
            'name': self.location_name(),
            'counter': self.counter_loc()
        }


class Certification(models.Model):
    user = models.ForeignKey(CustomUser, related_name='certifications', blank=True,null=True)
    certification_name = models.CharField(_('certification name'), max_length=100, blank=True)
    certification_number = models.CharField(_('cetification number'), max_length=100, blank=True)

    def __unicode__(self):
        return self.certification_name


class ProfessionalManager(models.Manager):
    def create_prof(self, user):
        extended_user = Professional(customuser_ptr=user)
        extended_user.__dict__.update(user.__dict__)
        extended_user.save()
        return extended_user


class Professional(CustomUser):
    PROFESSIONAL_CHOICES = (
        ('Nutritionist', 'Nutritionist'),
        ('Trainer', 'Trainer'),
        ('Promoter', 'Promoter'),
        ('Instructor', 'Instructor'),
    )

    profession = models.CharField(_('profession'), max_length=30, blank=True, choices=PROFESSIONAL_CHOICES)
    is_accepting = models.BooleanField(_('accepting'), default=False)

    queue = models.BooleanField(_("queue"), default=True)
    objects = ProfessionalManager()

    fitness_sales_experience = models.CharField(_('fitness sales experience'), max_length=100   , blank=True)
    education = models.CharField(_('education'), max_length=30, blank=True)
    group_fitness_experience = models.CharField(_('group fitness experience'), max_length=100, blank=True)
    nutritionist_experience = models.CharField(_('nutritionist experience'), max_length=100, blank=True)
    certified_nutritionist = models.BooleanField(_('certified nutritionist'), default=False)
    certified_group_fitness = models.BooleanField(_('certified group fitness'), default=False)

    certification_name1 = models.CharField(_('certification name 1'), max_length=100, blank=True)
    certification_number1 = models.CharField(_('cetification number 1'), max_length=100, blank=True)
    certification_name2 = models.CharField(_('certification name 2'), max_length=100, blank=True)
    certification_number2 = models.CharField(_('cetification number 2'), max_length=100, blank=True)

    shopify_sales = shopify_call.customer_sales_to_date


    #Metadata
    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = _('Professional')
        verbose_name_plural = _('Professionals')
    def get_model_fields(model):
        return model._meta.fields


    def get_all_data(self):
        data = super(Professional, self).get_all_data()
        data['profession'] = self.profession
        data['specialty'] = list(self.tags.names())
        data['specialty_list'] = ','.join(self.tags.names())
        data['is_accepting'] = self.is_accepting
        return data

    def get_shopify_id(self):
        return self.shopify_id

    def setup_professional(self, password, referred_by):
        self.attach_referral(referred_by)
        self.create_primary_address()
        errors = self.shopify_create(password)
        self.add_to_locations()
        self.is_upgraded = True
        self.is_professional = True
        self.save()
        return errors


class FeaturedProfessional(models.Model):
    professional = models.ForeignKey(Professional)


class StaticTags(models.Model):
    tags = models.ForeignKey(Tag, blank=True, null=True)

    def __unicode__(self):
        return str(self.tags)

    class Meta:
        verbose_name = _('StaticTags')
        verbose_name_plural = _('StaticTags')

