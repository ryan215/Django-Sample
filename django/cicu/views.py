import os
from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files import File
from PIL import Image
from os import path, sep, makedirs
from .forms import UploadedFileForm
from .models import UploadedFile
from .settings import IMAGE_CROPPED_UPLOAD_TO
from django.conf import settings
import math
from django.contrib.auth import get_user_model
User = get_user_model()



@csrf_exempt
@require_POST
def upload(request):
    form = UploadedFileForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        uploaded_file = form.save()
        # pick an image file you have in the working directory
        # (or give full path name)
        img = Image.open(uploaded_file.file.path, mode='r')
        # get the image's width and height in pixels
        width, height = img.size
        data = {
            'path': uploaded_file.file.url,
            'id' : uploaded_file.id,
            'width' : width,
            'height' : height,
        }
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseBadRequest(json.dumps({'errors': form.errors}))


@csrf_exempt
@require_POST
def crop(request):
    try:
        if request.method == 'POST':
            box = request.POST.get('cropping', None)
            imageId = request.POST.get('id', None)
            uploaded_file = UploadedFile.objects.get(id=imageId)
            img = Image.open( uploaded_file.file.path, mode='r' )
            values = [int(float(x)) for x in box.split(',')]

            width = abs(values[2] - values[0])
            height = abs(values[3] - values[1])

            if width and height and (width <= img.size[0] or height <= img.size[1]):
                croppedImage = img.crop(values).resize((500,500),Image.ANTIALIAS)
            else:
                raise

            pathToFile = path.join(settings.MEDIA_ROOT,IMAGE_CROPPED_UPLOAD_TO)
            if not path.exists(pathToFile):
                makedirs(pathToFile)
            pathToFile = path.join(pathToFile,uploaded_file.file.path.split(sep)[-1])
            croppedImage.save(pathToFile)

            new_file = UploadedFile()
            f = open(pathToFile, mode='rb')
            new_file.file.save(uploaded_file.file.name, File(f))
            f.close()

            data = {
                'path': new_file.file.url,
                'id' : new_file.id,
            }

            return HttpResponse(json.dumps(data))

    except Exception:
       return HttpResponseBadRequest(json.dumps({'errors': 'illegal request test'}))


@csrf_exempt
@require_POST
def upload_profile_picture(request):
    form = UploadedFileForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        uploaded_file = form.save()
        # pick an image file you have in the working directory
        # (or give full path name)
        img = Image.open(uploaded_file.file.path, mode='r')
        (width_img, height_img) = img.size

        if width_img< 500 and height_img< 500:
            uploaded_file.file.delete(False)
            uploaded_file.delete()
            return HttpResponseBadRequest(json.dumps({'errors': ['Minimum resolution requirement 500x500 not met']}))

        # get the image's width and height in pixels
        width, height = img.size
        data = {
            'path': uploaded_file.file.url,
            'id' : uploaded_file.id,
            'width' : width,
            'height' : height,
        }
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseBadRequest(json.dumps({'errors': [form.errors]}))


@csrf_exempt
@require_POST
def crop_profile_picture(request):
    try:
        if request.method == 'POST':
            box = request.POST.get('cropping', None)
            imageId = request.POST.get('id', None)
            WidthHeight = request.POST.get('WidthHeight', None)
            user_id = request.POST.get('user_id', None)
            uploaded_file = UploadedFile.objects.get(id=imageId)
            img = Image.open( uploaded_file.file.path, mode='r' )
            values = [int(float(x)) for x in box.split(',')]
            wh_values = [int(float(x)) for x in WidthHeight.split(',')]
            (width_img, height_img) = img.size
            user = User.objects.get(id = user_id)

            width_img=float(width_img);
            scale1 = float(width_img/wh_values[0])

            height_img=float(height_img);
            scale2 = float(height_img/wh_values[1])
            scale = (scale1 + scale2)/2

            if(scale):
                i = 0
                for item in values:
                    values[i] = item * scale
                    values[i]=math.ceil(values[i])
                    values[i]= int(values[i])
                    i += 1
            else:
                raise

            width = abs(values[2] - values[0])
            height = abs(values[3] - values[1])

            if width< 500 and height< 500:
                return HttpResponseBadRequest(json.dumps({'errors': ['resolution requirements not met, minumum requirements 500x500']}))

            if width and height and (width <= img.size[0] or height <= img.size[1]):
                croppedImage = img.crop(values).resize((500,500),Image.ANTIALIAS)
            else:
                raise

            pathToFile = path.join(settings.MEDIA_ROOT,IMAGE_CROPPED_UPLOAD_TO)
            if not path.exists(pathToFile):
                makedirs(pathToFile)
            pathToFile = path.join(pathToFile,uploaded_file.file.path.split(sep)[-1])
            croppedImage.save(pathToFile)

            f = open(pathToFile, mode='rb')
            user.img.save(uploaded_file.file.name, File(f))
            f.close()

            file_img = pathToFile
            os.remove(file_img)

            data = {
                'path': user.img.url,
            }

            return HttpResponse(json.dumps(data))

    except Exception:
       return HttpResponseBadRequest(json.dumps({'errors': ['illegal request test']}))
