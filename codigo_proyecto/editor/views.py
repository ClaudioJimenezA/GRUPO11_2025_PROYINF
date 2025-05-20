# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Boletin
from .forms import BoletinForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from django.conf import settings
from django.utils.timezone import now
from django.core.files.storage import default_storage


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
    plantillas = Boletin.objects.filter(es_plantilla=True)
    return render(request, 'editor/boletin_list.html', {'boletines': boletines, 'plantillas': plantillas})

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

# def boletin_form(request, pk=None):
#     instance = Boletin.objects.get(pk=pk) if pk else None
#     if request.method == 'POST':
#         form = BoletinForm(request.POST, instance=instance)
#         if form.is_valid():
#             boletin = form.save(commit=False)
#             accion = request.POST.get('accion')

#             if accion == 'guardar':
#                 boletin.estado = 'borrador'
#                 boletin.save()
#                 return redirect('lista_boletines')

#             elif accion == 'previsualizar':
#                 return render(request, 'editor/boletin_preview.html', {'boletin': boletin, 'preview': True})
#     else:
#         form = BoletinForm(instance=instance)

#     return render(request, 'editor/boletin_form.html', {'form': form})

def boletin_form(request, pk=None):
    print("LLEGÓ AL FORMULARIO")
    print("Método:", request.method)

    boletin = get_object_or_404(Boletin, pk=pk) if pk else None

    if request.method == 'POST':
        print("SE ENVÍO UN POST")
        print("Datos POST:", request.POST)

        form = BoletinForm(request.POST, instance=boletin)

        if form.is_valid():
            print("Formulario válido")
            boletin = form.save(commit=False)
            boletin.publicado = False  # o True, según tu lógica
            boletin.save()
            return redirect('lista_boletines')
        else:
            print("Formulario inválido:", form.errors)

    else:
        form = BoletinForm(instance=boletin)

    return render(request, 'editor/boletin_form.html', {'form': form})

def usar_plantilla(request, pk):
    plantilla = get_object_or_404(Boletin, pk=pk, es_plantilla=True)
    nuevo_boletin = Boletin.objects.create(
        titulo="Nuevo boletín desde plantilla: " + plantilla.titulo,
        contenido=plantilla.contenido,
        imagen=plantilla.imagen,
        publicado=False,
        es_plantilla=False,
        fecha_creacion=now(),
    )
    return redirect('editar_boletin', pk=nuevo_boletin.pk)

def eliminar_boletin(request, pk):
    boletin = get_object_or_404(Boletin, pk=pk)
    if not boletin.publicado:
        boletin.delete()
    return redirect('lista_boletines')

def tinymce_templates(request):
    plantillas = Boletin.objects.filter(es_plantilla=True).exclude(contenido__isnull=True).exclude(contenido__exact='')


    templates = []
    for plantilla in plantillas:
        templates.append({
            'title': plantilla.titulo,
            'description': f'Plantilla: {plantilla.titulo}',
            'content': plantilla.contenido,
        })

    return JsonResponse(templates, safe=False)