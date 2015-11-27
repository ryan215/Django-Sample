from django import forms
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import RelationshipStatus
from django.contrib.auth import get_user_model
User = get_user_model()


class RelationshipStatusAdminForm(forms.ModelForm):
    class Meta:
        model = RelationshipStatus

    def duplicate_slug_check(self, status_slug):
        status_qs = RelationshipStatus.objects.filter(
            Q(from_slug=status_slug) |
            Q(to_slug=status_slug) |
            Q(symmetrical_slug=status_slug)
        )

        if self.instance.pk:
            status_qs = status_qs.exclude(pk=self.instance.pk)

        if status_qs.exists():
            raise forms.ValidationError('"%s" slug already in use on %s' %
                (status_slug, unicode(status_qs[0])))

    def clean_from_slug(self):
        self.duplicate_slug_check(self.cleaned_data['from_slug'])
        return self.cleaned_data['from_slug']

    def clean_to_slug(self):
        self.duplicate_slug_check(self.cleaned_data['to_slug'])
        return self.cleaned_data['to_slug']

    def clean_symmetrical_slug(self):
        self.duplicate_slug_check(self.cleaned_data['symmetrical_slug'])
        return self.cleaned_data['symmetrical_slug']

    def clean(self):
        if self.errors:
            return self.cleaned_data

        if self.cleaned_data['from_slug'] == self.cleaned_data['to_slug'] or \
           self.cleaned_data['to_slug'] == self.cleaned_data['symmetrical_slug'] or \
           self.cleaned_data['symmetrical_slug'] == self.cleaned_data['from_slug']:
            raise forms.ValidationError('from, to, and symmetrical slugs must be different')

        return self.cleaned_data

class UserEmailCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = User


class UserEmailChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = User

