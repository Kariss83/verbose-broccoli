from django.shortcuts import render, redirect
from django.contrib import messages


from collection.models import Game, Collection
from barcode.controllers.barcode_reader import ImageReader, Stringb64Reader
from barcode.controllers.information_gatherer import Gatherer
from barcode.forms import UploadFileForm

from pyrate_limiter import BucketFullException


# Create your views here.
# upload view
def upload_barcode(request):
    if request.method == 'POST':
        if request.POST.get('b64img', None) is not None:
            img_data_str = request.POST.get('b64img', '')
            string_handler = Stringb64Reader(img_data_str)
            string_handler.string_to_PNG()
            barcode = string_handler.read_image()

            if len(barcode) == 0:
                messages.error(request, ('No barcode detected - Try again...'))
                return redirect('/barcode/upload')
            else:
                # Try Except block preventing useless API calls
                try:
                    game = Game.objects.get(barcode=barcode[0])
                except Game.DoesNotExist:
                    gatherer = Gatherer(barcode)
                    try:
                        name, img_url = gatherer.get_name_and_img_url()
                        avg_price = gatherer.get_avg_price()

                        game = Game.objects.get_or_create(barcode=barcode[0],
                                                        defaults={
                                                            'avg_price': avg_price,
                                                            'name': name,
                                                            'image': img_url,
                                                        })[0]
                    except BucketFullException as err:
                        messages.error(request, ('Limit of API calls have been reached. Please try again later...'))
                        return redirect('/barcode/upload')
                context = {'game': game}
                if request.user.is_authenticated:
                    collections = Collection.objects.filter(user=request.user)
                    context = {'game': game, 'collections': collections}
        else:
            form = UploadFileForm(request.POST, request.FILES)

            if (request.FILES['file'].size > 10 * 1024 * 1024):
                messages.error(request, 'File too large. Size should not exceed 10 MiB.')
                form = UploadFileForm()
                return render(
                    request,
                    'barcode/scan.html',
                    {'form': form}
                )
            else:
                if form.is_valid():
                    file_handler = ImageReader(request.FILES['file'])
                    barcode = file_handler.get_image_barcode()

                    if len(barcode) == 0:
                        messages.error(request, ('No barcode detected - Try again...'))
                        return redirect('/barcode/upload')
                    else:
                        # Try Except block preventing useless API calls
                        try:
                            game = Game.objects.get(barcode=barcode[0])
                        except Game.DoesNotExist:
                            gatherer = Gatherer(barcode)
                            name, img_url = gatherer.get_name_and_img_url()
                            avg_price = gatherer.get_avg_price()

                            game = Game.objects.get_or_create(barcode=barcode[0],
                                                            defaults={
                                                                'avg_price': avg_price,
                                                                'name': name,
                                                                'image': img_url,
                                                            })[0]
                        context = {'game': game}
                        if request.user.is_authenticated:
                            collections = Collection.objects.filter(user=request.user)
                            context = {'game': game, 'collections': collections}
        return render(request, 'barcode/upload.html', context)
    else:
        form = UploadFileForm()
        return render(
            request,
            'barcode/scan.html',
            {'form': form}
        )


def home_view(request):
    return render(
        request,
        'home.html',
        {}
        )
