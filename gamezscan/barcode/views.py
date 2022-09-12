from django.shortcuts import render, redirect
from django.contrib import messages

from gamezscan.barcode.forms import UploadFileForm

from gamezscan.barcode.helpers import convert_img_str_to_barcode
from gamezscan.barcode.helpers import uploadfile_size_too_big
from gamezscan.barcode.helpers import barcode_not_found
from gamezscan.barcode.helpers import find_or_create_game_from_barcode
from gamezscan.barcode.helpers import parse_img_to_barcode


# Create your views here.
# upload view
def upload_barcode(request):
    if request.method == "POST":
        if request.POST.get("b64img", None) is not None:
            img_data_str = request.POST.get("b64img", "")
            barcode = convert_img_str_to_barcode(img_data_str)

            if barcode_not_found(barcode):
                messages.error(request, ("No barcode detected - Try again..."))
                return redirect("/barcode/upload")
            else:
                context = find_or_create_game_from_barcode(barcode, request)
        else:
            form = UploadFileForm(request.POST, request.FILES)

            if uploadfile_size_too_big(request.FILES["file"]):
                messages.error(
                    request, "File too large. Size should not exceed 10 MiB."
                )
                form = UploadFileForm()
                return render(request, "barcode/scan.html", {"form": form})
            else:
                if form.is_valid():
                    barcode = parse_img_to_barcode(request.FILES["file"])

                    if barcode_not_found(barcode):
                        messages.error(request, ("No barcode detected - Try again..."))
                        return redirect("/barcode/upload")
                    else:
                        context = find_or_create_game_from_barcode(barcode, request)
        return render(request, "barcode/upload.html", context)
    else:
        form = UploadFileForm()
        return render(request, "barcode/scan.html", {"form": form})


def home_view(request):
    return render(request, "home.html", {})
