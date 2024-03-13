from django.shortcuts import render


# Create your views here.

def main_page(request):
    context = {

    }

    return render(request, "main_page/main.html", context)
