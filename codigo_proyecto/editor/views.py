# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Boletin
from .forms import BoletinForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import os
from django.conf import settings
from django.utils import timezone, text
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.base import ContentFile
from io import BytesIO
from gestor_pdfs.models import DocumentoPDF
import tempfile
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt





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


@csrf_exempt
def lista_boletines(request):
    if request.session.get('supabase_class') not in ['editor', 'administrador']:
        return HttpResponseForbidden("Acceso no permitido.")

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


@csrf_exempt
def editar_boletin(request, pk):
    if request.session.get('supabase_class') != 'editor':
        return HttpResponseForbidden("Acceso no permitido.")

    boletin = get_object_or_404(Boletin, pk=pk)

    if request.method == 'POST':
        form = BoletinForm(request.POST, instance=boletin)
        if form.is_valid():
            form.save()
            return redirect('lista_boletines')
        else:
            print("Errores del formulario:", form.errors)

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
            accion = request.POST.get('accion')

            if accion == 'previsualizar':
                preview_boletin = form.save(commit=False)
                return render(request, 'editor/boletin_preview.html', {
                    'boletin': preview_boletin,
                    'preview': True
                })
            elif accion == 'guardar':
                boletin = form.save(commit=False)
                boletin.publicado = False
                boletin.save()
                return redirect('editar_boletin', pk=boletin.pk)

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
        fecha_creacion= timezone.now(),
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

def exportar_boletin_pdf(boletin):
    html_string = render_to_string('editor/boletin_pdf.html', {'boletin': boletin})
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(target=pdf_file)

    # Guarda el PDF como archivo en memoria
    return ContentFile(pdf_file.getvalue(), name=f"boletin_{boletin.pk}.pdf")

def publicar_boletin(request, pk):
    boletin = get_object_or_404(Boletin, pk=pk)
    if not boletin.contenido.strip():
        messages.error(request, "El boletín no tiene contenido para publicar.")
        return redirect('editar_boletin', pk=pk)
    
    boletin.publicado = True
    boletin.fecha_creacion = timezone.now()  # opcional si no se estableció aún
    boletin.save()

    # Generar el PDF
    pdf_content = exportar_boletin_pdf(boletin)

    # Registrar en la app de PDFs
    DocumentoPDF.objects.create(
        nombre=boletin.titulo,
        archivo=pdf_content,
        etiquetas= text.slugify(boletin.titulo) # o extrae etiquetas desde el boletín si tienes lógica definida
    )

    messages.success(request, "Boletín publicado y PDF generado correctamente.")
    return redirect('editar_boletin', pk=pk)
 


