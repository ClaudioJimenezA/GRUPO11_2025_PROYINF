from django.shortcuts import render, redirect
import json
from .models import Fuente  # Importa el modelo Fuente que creaste


def index_fuentes(request):
    fuentes = Fuente.objects.all()  # Obtener todas las fuentes
    return render(request, 'buscador_fuentes/index_fuentes.html', {'fuentes': fuentes})

def agregar_fuentes(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        url = request.POST.get("url")
        etiquetas = request.POST.get("etiquetas").split(",")

        # Crea una nueva fuente
        nueva_fuente = Fuente(nombre=nombre, url=url, etiquetas=json.dumps(etiquetas))
        nueva_fuente.save()
        return redirect("index_fuentes")
    return render(request, 'buscador_fuentes/agregar_fuentes.html')

# Búsqueda de fuentes para modificar
def buscar_para_modificar(request):
    query = request.GET.get("query")
    resultados = Fuente.objects.filter(nombre__icontains=query) | Fuente.objects.filter(etiquetas__contains=query)
    return render(request, "buscador_fuentes/modificar_fuentes.html", {"resultados": resultados})

# Búsqueda de fuentes para borrar
def buscar_para_borrar(request):
    query = request.GET.get("query")
    resultados = Fuente.objects.filter(nombre__icontains=query) | Fuente.objects.filter(etiquetas__contains=query)
    return render(request, "buscador_fuentes/borrar_fuentes.html", {"resultados": resultados})

# Modificar una fuente
def modificar_fuentes(request, fuente_id):
    fuente = Fuente.objects.get(id=fuente_id)
    if request.method == "POST":
        fuente.nombre = request.POST.get("nombre")
        fuente.link = request.POST.get("link")
        fuente.etiquetas = json.dumps(request.POST.get("etiquetas").split(","))
        fuente.save()
        return redirect("index_fuentes")
    return render(request, "buscador_fuentes/modificar_detalle.html", {"fuente": fuente})

# Borrar una fuente
def borrar_fuentes(request, fuente_id):
    fuente = Fuente.objects.get(id=fuente_id)
    if request.method == "POST":
        fuente.delete()
        return redirect("index_fuentes")
    return render(request, "buscador_fuentes/borrar_confirmar.html", {"fuente": fuente})
def vistas_fuentes(request):
    return render(request, 'buscador_fuentes/vistas_fuentes.html')

def buscar_fuentes(request):
    query = request.GET.get('query', '').strip()
    etiqueta = request.GET.get('etiqueta', '').strip()
    resultados = []

    if query or etiqueta:
        if query:
            resultados = Fuente.objects.filter(nombre__icontains=query)
        elif etiqueta:
            resultados = Fuente.objects.filter(etiquetas__icontains=etiqueta)
    
    etiquetas = Fuente.objects.values_list('etiquetas', flat=True).distinct()

    return render(request, 'buscador_fuentes/buscar_fuentes.html', {
        'resultados': resultados,
        'etiquetas': etiquetas,
    })

