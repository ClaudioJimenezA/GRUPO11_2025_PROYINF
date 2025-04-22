# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Boletin
from .forms import BoletinForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from django.conf import settings

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('file')
        if not image:
            return JsonResponse({'error': 'No image provided'}, status=400)

        # Ruta donde se guarda la imagen
        image_path = os.path.join('uploads', image.name)
        full_path = os.path.join(settings.MEDIA_ROOT, image_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        image_url = settings.MEDIA_URL + image_path
        return JsonResponse({'location': image_url})


def lista_boletines(request):
    boletines = Boletin.objects.all().order_by('-fecha_creacion')
    return render(request, 'editor/boletin_list.html', {'boletines': boletines})

def detalle_boletin(request, pk):
    boletin = get_object_or_404(Boletin, pk=pk)
    return render(request, 'editor/boletin_detail.html', {'boletin': boletin})

def crear_boletin(request):
    if request.method == 'POST':
        form = BoletinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_boletines')
    else:
        form = BoletinForm()
    return render(request, 'editor/boletin_form.html', {'form': form})
def preview_boletin(request, pk):
    boletin = get_object_or_404(Boletin, pk=pk)
    return render(request, 'editor/boletin_detail.html', {'boletin': boletin})

def editar_boletin(request, pk):
    boletin = get_object_or_404(Boletin, pk=pk)
    if request.method == 'POST':
        form = BoletinForm(request.POST, instance=boletin)
        if form.is_valid():
            form.save()
            return redirect('lista_boletines')
    else:
        form = BoletinForm(instance=boletin)
    return render(request, 'editor/boletin_form.html', {'form': form, 'boletin': boletin})


