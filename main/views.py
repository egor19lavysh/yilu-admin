from django.shortcuts import render

def get_levels(request):
    return render(request, "main/levels.html")