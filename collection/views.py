from django.shortcuts import render, redirect

# Create your views here.
# Scan page view
def scan_barcode(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return render(
            request,
            'home/scan.html',
            {}
            )