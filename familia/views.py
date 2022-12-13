from django.shortcuts import render
from familia.models import familia
from familia.forms import Buscar, familiaform
from django.views import View 
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

def index(request):
    return render(request, "familia/familia.html")

###"""def saludar_a(requet):
   ### return render(request, "ejemplo/saludar_a.html)"""

def mostrar_familiar(request):
  lista_familiares = familia.objects.all()
  return render(request, "familia/familia.html", {"lista_familiares": lista_familiares})

###def buscar(request):
### nombres=[ "Miguel", "Jose", "Enrique", "Santiago" ]
##  query = request.GET["q"]
### if query in nombres.
###  resultado=nombres.index(query)
###  indice= nombre.index(query) (parte 2)
### resultado = nombres[ indice ]
### else:
### resultado="no hay match"
###return render(request, "familia/buscar.html", {"resultado": resuiltado})

class buscar_familiar(View):
    form_class = Buscar
    template_name = 'familia/buscar_familia.html'
    initial = {"nombre":""}
    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get("nombre")
            lista_familiares = familia.objects.filter(nombre__icontains=nombre).all() 
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form':form, 
                                                        'lista_familiares':lista_familiares})
        return render(request, self.template_name, {"form": form})

class AltaFamiliar(View):

    form_class = familiaform
    template_name = 'familia/alta_familia.html'
    initial = {"nombre":"", "direccion":"", "numero_pasaporte":""}

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            msg_exito = f"se cargo con éxito el familiar {form.cleaned_data.get('nombre')}"
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form':form, 
                                                        'msg_exito': msg_exito})
        
        return render(request, self.template_name, {"form": form})

class familialist(ListView):
    model = familia

class familiaCrear(CreateView):
    model = familia
    success_url=""
    fields =["nombre", "direccion", "numero_pasaporte"]

class familiaBorrar(DeleteView):
    model = familia
    success_url=""
    

class Actualizafamilia(UpdateView):
    model = familia
    success_url="/success_updated_messages.html"
    fields =["nombre", "direccion", "numero_pasaporte"]



   