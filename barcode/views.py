from django.shortcuts import render, redirect
from django.contrib import messages


from collection.models import Game
from barcode.controllers.barcode_reader import ImageReader, Stringb64Reader
from barcode.controllers.information_gatherer import Gatherer
from barcode.forms import UploadFileForm


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
                    name, img_url = gatherer.get_name_and_avg_price()
                    avg_price = gatherer.get_avg_price()

                    game = Game.objects.get_or_create(barcode=barcode[0],
                                                    defaults={
                                                        'avg_price': avg_price,
                                                        'name': name,
                                                        'image': img_url,
                                                    })[0]
                context = {'game': game}

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file_handler = ImageReader(request.FILES['file'])
            file_handler.handle_uploaded_file()
            barcode = file_handler.read_image()

            if len(barcode) == 0:
                messages.error(request, ('No barcode detected - Try again...'))
                return redirect('/barcode/upload')
            else:
                # Try Except block preventing useless API calls
                try:
                    game = Game.objects.get(barcode=barcode[0])
                except Game.DoesNotExist:
                    gatherer = Gatherer(barcode)
                    name, img_url = gatherer.get_name_and_avg_price()
                    avg_price = gatherer.get_avg_price()

                    game = Game.objects.get_or_create(barcode=barcode[0],
                                                    defaults={
                                                        'avg_price': avg_price,
                                                        'name': name,
                                                        'image': img_url,
                                                    })[0]
                context = {'game': game}
        return render(request, 'barcode/upload.html', context)
    else:
        form = UploadFileForm()
        return render(
            request,
            'barcode/scan.html',
            {'form': form}
            )


# def show_product(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             filename = str(request.FILES['file'])
#             file_extension = filename.split('.')[-1]
#             barcode = handle_uploaded_file(request.FILES['file'], file_extension)
#         context = {'barcode': barcode,
#                    'filename': filename,
#                    'extension': file_extension,
#                    'barcode': barcode,
#                    }
#         return render(request, 'barcode/scan.html', context)
#     else:
#         form = UploadFileForm()
#         return render(
#             request,
#             'home/scan.html',
#             {'form': form}
#             )
