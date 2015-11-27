class HttpsMiddleware(object):

    def process_request(self, request): # redirects to HTTPS url
        from django.http import HttpResponseRedirect
        from django.http import HttpResponse

        if 'HTTP_X_FORWARDED_SSL' not in request.META: #ensures that django has ssl else will return this response
            return HttpResponse('WRONG')

        # redirect if not https
        URL = request.build_absolute_uri('')
        print ''
        if URL[0:5] == 'https':
             return None
        else:
            new_URL = "https%s" % URL[4:]
            HttpResponseRedirect(new_URL)

