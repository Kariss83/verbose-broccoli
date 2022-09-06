from django.shortcuts import redirect
from django.contrib import messages

from collection.models import Game, Collection
from barcode.controllers.barcode_reader import ImageReader, Stringb64Reader
from barcode.controllers.information_gatherer import Gatherer

from pyrate_limiter import BucketFullException


def parse_img_to_barcode(file):
    file_handler = ImageReader(file)
    return file_handler.get_image_barcode()


def convert_img_str_to_barcode(img_data_str):
    string_handler = Stringb64Reader(img_data_str)
    string_handler.string_to_PNG()
    barcode = string_handler.read_image()
    return barcode


def find_or_create_game_from_barcode(barcode, request):
    try:
        game = Game.objects.get(barcode=barcode[0])
    except Game.DoesNotExist:
        gatherer = Gatherer(barcode)
        try:
            name, img_url = gatherer.get_name_and_img_url()
            try:
                avg_price = gatherer.get_avg_price()
            except KeyError:
                avg_price = 0
                messages.error(
                    request,
                    ('This item have not been found on eBay so price is set to 0.')
                )

            game = Game.objects.get_or_create(
                barcode=barcode[0],
                defaults={
                    'avg_price': avg_price,
                    'name': name,
                    'image': img_url,
                    }
                )[0]
        except BucketFullException as err:
            messages.error(
                request,
                (f'Limit of API calls have been reached. Please try again later... {err}')
            )
            return redirect('/barcode/upload')
        except TypeError as err:
            messages.error(
                request,
                (f'Could not retrieve a name or a picture url -- {err}')
            )
            return redirect('/barcode/upload')
    context = {'game': game}
    if request.user.is_authenticated:
        collections = Collection.objects.filter(user=request.user)
        context = {'game': game, 'collections': collections}
    return context


def uploadfile_size_too_big(file):
    return (file.size > 10 * 1024 * 1024)


def barcode_not_found(barcode):
    return len(barcode) == 0
