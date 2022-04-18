from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .serializer import * 
from core.models import Customer

#email
from django.core.mail import send_mail

# pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
# *************

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/main.html'


# pdf of our models
def customer_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    customer = get_object_or_404(Customer, pk=pk)

    template_path = 'customers/pdf2.html'
    context = {'customer': customer}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #if display:
    response['Content-Disposition'] =  'filename="report.pdf"'


    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#render template pdf
def render_pdf_view(request):
    template_path = 'customers/pdf1.html'
    context = {'myvar': 'pedro is gay, right?'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #if display:
    response['Content-Disposition'] =  'filename="report.pdf"'


    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def index(request):

   print('kkkkkkkkkkkkkkkkkkk')
   send_mail('Hello from Marcos',
   'Hello There, this is an automated message',
   'viniciustatuta@gmail.com',
   ['marcosstatuta@gmail.com'],
   fail_silently=False)
   print('kkkkkkkFOIIIIIkkkkkkkkkkkk')
   
   return render(request, 'send/index.html')

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer    