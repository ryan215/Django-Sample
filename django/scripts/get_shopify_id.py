from shopify_app import shopify_call
users = User.objects.all()

for user in users:
    try:
        print user.email
        user.shopify_id = shopify_call.requests_search(user.email)['id']
        user.save()
        print user.shopify_id
    except:
        print 'doesnt exists'
