from django.shortcuts import render

# Create your views here.


# upload view
def upload_barcode(request):
    return render(
        request,
        'barcode/upload.html',
        {}
    )
