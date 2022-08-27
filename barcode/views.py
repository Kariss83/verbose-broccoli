import base64
from django.shortcuts import render

from collection.models import Game
from barcode.controllers.barcode_reader import ImageReader, Stringb64Reader
from barcode.controllers.information_gatherer import Gatherer
from barcode.forms import UploadFileForm

# Create your views here. 
# upload view
def upload_barcode(request):
    if request.method == 'POST':
        if request.POST.get('b64img', None) != None:
            img_data_str = request.POST.get('b64img', '').split(',')[1]
            while len(img_data_str) % 4 != 0:
                img_data_str += '='
            img_data = base64.b64decode(img_data_str)
            with open('test_webcam.png', 'wb+') as destination:
                destination.write(img_data)

            context = {'data_url': img_data}

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            

            file_handler = ImageReader(request.FILES['file'])
            file_handler.handle_uploaded_file()
            barcode = file_handler.read_image()

            gatherer = Gatherer(barcode)
            name , img_url= gatherer.get_name_and_avg_price()
            avg_price = gatherer.get_avg_price()

            game = Game.objects.get_or_create(barcode=barcode[0],
                                              avg_price=avg_price,
                                              name=name,
                                              image=img_url,
                                              )[0]
            context = {'game': game,
                    }
        return render(request, 'barcode/upload.html', context)
    else:
        form = UploadFileForm()
        return render(
            request,
            'barcode/scan.html',
            {'form': form}
            )

def show_product(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filename = str(request.FILES['file'])
            file_extension = filename.split('.')[-1]
            barcode = handle_uploaded_file(request.FILES['file'], file_extension)
        context = {'barcode': barcode,
                   'filename': filename,
                   'extension': file_extension,
                   'barcode': barcode,
                   }
        return render(request, 'barcode/scan.html', context)
    else:
        form = UploadFileForm()
        return render(
            request,
            'home/scan.html',
            {'form': form}
            )