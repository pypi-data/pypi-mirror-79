from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Pet

# Create your views here.
def home(request):

   pets = Pet.objects.all()

   return render(request, 'adoptions/home.html', {'pets': pets})

def pet_detail(request, pet_id):

    try:
        pet = Pet.objects.get(id=pet_id)

    except:

        return Http404('Pet not found')

    return render(request, 'adoptions/pet_detail.html', {'pet': pet})
