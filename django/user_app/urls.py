from django.conf.urls import patterns, include, url
from rest_framework import routers
from .views import UserViewSet, GroupViewSet, ProfessionalListView, LocationViewSet, ProfessionalObjView, PaymentView, ModifyMembershipView

from .views import ClientListView, CreditcardView, ProfileView, FollowUserView, BlockUserView, ConnectUserView, FanaticsListView
from .views import GroupTagView, StaticTagViewSet, UserListView


router = routers.SimpleRouter(trailing_slash=False)

router.register(r'/groups', GroupViewSet)
router.register(r'/location', LocationViewSet)

# urlpatterns = router.urls

urlpatterns = patterns('',
    # Main View
    url(r'^$', UserListView.as_view()),
    url(r'^/(?P<pk>[0-9]+)$', UserViewSet.as_view()),
    url(r'^/profile/(?P<pk>[0-9]+)$', ProfileView.as_view()),
    url(r'^/follow/(?P<pk>[0-9]+)$', FollowUserView.as_view()),
    url(r'^/block/(?P<pk>[0-9]+)$', BlockUserView.as_view()),
    url(r'^/connect/(?P<pk>[0-9]+)$', ConnectUserView.as_view()),
    # Professionals
    url(r'^/fanatics$', FanaticsListView.as_view()),
    url(r'^/professionals$', ProfessionalListView.as_view()),
    url(r'^/professionals/(?P<pk>[0-9]+)$', ProfessionalObjView.as_view()),
    url(r'^/professionals/client-list$', ClientListView.as_view()),
    # Modify Payment Details
    url(r'^/modify-payment-details/(?P<pk>[0-9]+)$', PaymentView.as_view()),
    url(r'^/modify-membership/(?P<pk>[0-9]+)$', ModifyMembershipView.as_view()),
    # Retrieve Creditcards
    url(r'^/creditcards/(?P<pk>[0-9]+)$', CreditcardView.as_view()),
    url(r'^/group/(?P<type>[a-z]+)', GroupTagView.as_view()),
    url(r'^/tags$', StaticTagViewSet.as_view()),
    url(r'^', include(router.urls)),

)
