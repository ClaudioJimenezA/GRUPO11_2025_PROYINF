# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Boletin
from .forms import BoletinForm

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


