from django.shortcuts import render_to_response, redirect, render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
import shopify

from user_app.models import CustomUser
from shopify_app.models import ShopifySession

from django.contrib.auth.decorators import user_passes_test


#@user_passes_test(lambda u: u.is_superuser)
def home(request):
    lef_users = CustomUser.objects.all()

    individual_user = CustomUser.objects.get(email='isaax@utexas.edu')
    individual_user.shopify_create('')
    #individual_user.shopify_create('admin')
    #print individual_user.shopify_create('L00k$yFit')

    return HttpResponse('test')


def authenticate(request):
    shop = settings.SHOPIFY_STORE
    if shop:
        scope = settings.SHOPIFY_API_SCOPE
        redirect_uri = request.build_absolute_uri(reverse('shopify_app.views.finalize'))
        permission_url = shopify.Session.create_permission_url(shop.strip(), scope, redirect_uri)
        print permission_url
        return redirect(permission_url)

    return redirect(_return_address(request))


def finalize(request):
    shop_url = request.REQUEST.get('shop')
    print request.REQUEST
    try:
        shopify_session = shopify.Session(shop_url, request.REQUEST)
    except shopify.ValidationException:
        return redirect(reverse('shopify_app.views.login'))
    request.session['shopify'] = {
                "shop_url": shop_url,
                "access_token": shopify_session.token
            }

    #saves the session token into database
    from shopify_app.models import ShopifySession
    saved_session = ShopifySession.objects.get_session()
    saved_session.shop_url = shop_url
    saved_session.access_token = shopify_session.token
    saved_session.save()


    response = redirect(reverse('shopify_app.views.home'))
    request.session.pop('return_to', None)
    return response


@user_passes_test(lambda u: u.is_superuser)
def logout(request):
    request.session.pop('shopify', None)
    #messages.info(request, "Successfully logged out.")

    return redirect(reverse('shopify_app.views.home'))
