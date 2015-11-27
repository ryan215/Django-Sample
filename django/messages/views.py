import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from messages.models import Message
from messages.forms import ComposeForm
from messages.utils import format_quote, get_user_model, get_username_field
from messages.serializers import DeleteSerializer, UnDeleteSerializer, ReplySerializer, InboxSerializer, ComposeSerializer
from messages.serializers import TrashSerializer, SentSerializer, ConnectionSerializer
from messages.permissions import IsAdminOrSelf
User = get_user_model()


from notifications import notify

def compose(request, recipient=None, form_class=ComposeForm,
        template_name='messages/compose.html', success_url=None, recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if request.GET.has_key('next'):
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
        if recipient is not None:
            recipients = [u for u in User.objects.filter(**{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
            form.fields['recipient'].initial = recipients
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))
compose = login_required(compose)

def reply(request, message_id, form_class=ComposeForm,
        template_name='messages/compose.html', success_url=None,
        recipient_filter=None, quote_helper=format_quote):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote. To change the quote format
    assign a different ``quote_helper`` kwarg in your url-conf.

    """
    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(initial={
            'body': quote_helper(parent.sender, parent.body),
            'subject': _(u"Re: %(subject)s") % {'subject': parent.subject},
            'recipient': [parent.sender,]
            })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))
reply = login_required(reply)

def delete(request, message_id, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely.
    A cron-job should prune the database and remove old messages which are
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.

    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    user = request.user
    now = datetime.datetime.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if request.GET.has_key('next'):
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = now
        deleted = True
    if deleted:
        message.save()
        messages.info(request, _(u"Message successfully deleted."))
        if notification:
            notification.send([user], "messages_deleted", {'message': message,})
        return HttpResponseRedirect(success_url)
    raise Http404
delete = login_required(delete)

def undelete(request, message_id, success_url=None):
    """
    Recovers a message from trash. This is achieved by removing the
    ``(sender|recipient)_deleted_at`` from the model.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    undeleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if request.GET.has_key('next'):
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.save()
        messages.info(request, _(u"Message successfully recovered."))
        if notification:
            notification.send([user], "messages_recovered", {'message': message,})
        return HttpResponseRedirect(success_url)
    raise Http404
undelete = login_required(undelete)

def view(request, message_id, template_name='messages/view.html'):
    """
    Shows a single message.``message_id`` argument is required.
    The user is only allowed to see the message, if he is either
    the sender or the recipient. If the user is not allowed a 404
    is raised.
    If the user is the recipient and the message is unread
    ``read_at`` is set to the current datetime.
    """
    user = request.user
    now = datetime.datetime.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404
    if message.read_at is None and message.recipient == user:
        message.read_at = now
        message.save()
    return render_to_response(template_name, {
        'message': message,
    }, context_instance=RequestContext(request))
view = login_required(view)



# 3 MAIN LIST INBOX/SENT/DELETED

class InboxListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    model = Message
    serializer_class = InboxSerializer
    def get_queryset(self):
        """
            Returns all messages that were received by the given user and are not
            marked as deleted.
        """
        return Message.objects.filter(recipient=self.request.user,  recipient_deleted_at__isnull=True,)


class SentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    model = Message
    serializer_class = SentSerializer
    def get_queryset(self):
        """
            Returns all messages that were sent by the given user and are not
            marked as deleted.
        """
        return Message.objects.filter(
            sender=self.request.user,
            sender_deleted_at__isnull=True,
        )


class DeletedListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    model = Message
    serializer_class = TrashSerializer
    def get_queryset(self):
        """
            Returns all messages that were either received or sent by the given
            user and are marked as deleted.
        """
        return Message.objects.filter(
            recipient=self.request.user,
            recipient_deleted_at__isnull=False,
        ) | Message.objects.filter(
            sender=self.request.user,
            sender_deleted_at__isnull=False,
        )


# INDIVIDUAL OBJECT VIEWS

class DeleteMessageObjView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Message
    serializer_class = DeleteSerializer

class UnDeleteMessageObjView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Message
    serializer_class = UnDeleteSerializer


class ComposeMessageObjView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Message
    serializer_class= ComposeSerializer

    def post_save(self, obj, created=False):
        notify.send(self.request.user, recipient=obj.recipient, verb=u'messaged you!', target=obj)


class ReplyMessageObjView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Message
    serializer_class = ReplySerializer


class ConnectionView(generics.UpdateAPIView):
    permission_classes = (IsAdminOrSelf,)
    model = User
    serializer_class = ConnectionSerializer


class MessageView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    model = Message
    serializer_class = InboxSerializer
