from io import BytesIO
from django.shortcuts import render, get_object_or_404
from core.services import render_to_pdf
from rest_framework.viewsets import ModelViewSet
from .serializer import * 
from core.models import Customer

from django.views.generic import View

#email
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
# *************

#***********
from weasyprint import HTML, CSS

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
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #if display:
   #  response['Content-Disposition'] =  'filename="report.pdf"'


    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)



    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)

    subject = 'Management Automated Email- '
    html_message = render_to_string('send/pdf.html')
    pdf = HTML(string=html, base_url='customers/pdf2.html').write_pdf(
        stylesheets=[CSS(string='body { font-family: serif}')])   
    plain_message = 'foi'
    recipient_list = ['marcosstatuta@gmail.com']
    from_email = 'viniciustatuta@gmail.com'
    toaddrs = recipient_list 
    mail = EmailMessage(subject, body='oiiiiiiii', from_email=from_email, to=recipient_list )
    mail.attach('.pdf', pdf, "application/pdf")
    mail.content_subtype = "pdf"  # Main content is now text/html
    mail.encoding = 'utf-8'
    mail.send()      

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

# def index(request):

#    print('kkkkkkkkkkkkkkkkkkk')
#    send_mail('Hello from Marcos',
#    'Hello There, this is an automated message',
#    'viniciustatuta@gmail.com',
#    ['marcosstatuta@gmail.com'],
#    fail_silently=False)
#    print('kkkkkkkFOIIIIIkkkkkkkkkkkk')
   
#    return render(request, 'send/index.html')

@api_view(['POST'])
def index(request):
    subject = 'Management Automated Email- '
    html_message = render_to_string('send/pdf.html')
    pdf = HTML(string=html_message, base_url='').write_pdf(
        stylesheets=[CSS(string='body { font-family: serif}')])   
    plain_message = 'foi'
    recipient_list = ['marcosstatuta@gmail.com']
    from_email = 'viniciustatuta@gmail.com'
    toaddrs = recipient_list 
    mail = EmailMessage(subject, body='oiiiiiiii', from_email=from_email, to=recipient_list )
    mail.attach('.pdf', pdf, "application/pdf")
    mail.content_subtype = "pdf"  # Main content is now text/html
    mail.encoding = 'utf-8'
    mail.send()

    return Response(status=status.HTTP_200_OK, 
      data={
        'message': 'Success',
      }  
    )     



# def index(request, serial_no):
#     user = get_object_or_404(Student, pk=serial_no)
#     # roll_no = {'roll': str(user['roll_no'])}
#     html = render_to_string('card.html',
#                             {'user': user})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename={}'.format(user.roll_no + '.pdf')
#     pdf = weasyprint.HTML(string=html, base_url='').write_pdf(
#         stylesheets=[weasyprint.CSS(string='body { font-family: serif}')])
#     to_emails = [str(user.roll_no) + '@gmail.com']
#     subject = "Certificate from Nami Montana"
#     email = EmailMessage(subject, body=pdf, from_email='SSC', to=to_emails)
#     email.attach("{}".format(user.roll_no) + '.pdf', pdf, "application/pdf")
#     email.content_subtype = "pdf"  # Main content is now text/html
#     email.encoding = 'utf-8'
#     email.send()
#     return HttpResponseRedirect(reverse('id_card:submit'))

# @api_view(['POST'])
# def index(request):
#    email = EmailMessage(
#       'Subject here', 'Here is the message.', 'viniciustatuta@gmail.com', ['marcosstatuta@gmail.com'])
#    email.attach_file('core/Document.pdf')
#    email.send()
#    email.send()

#    return Response(status=status.HTTP_200_OK, 
#       data={
#         'message': 'Success',
#       }  
#     ) 


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer    