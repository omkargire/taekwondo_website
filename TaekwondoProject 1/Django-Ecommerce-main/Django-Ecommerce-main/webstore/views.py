import profile
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from email.message import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404, render ,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.contrib import messages
from django.http import JsonResponse
from django.conf import SettingsReference, settings
from django.contrib import admin
from django.urls import path, include
import os
from django.shortcuts import render
from .models import Trainer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from matplotlib.font_manager import MSUserFontDirectories
from .models import User, Category, Product
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from . import views
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date
from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
form_path = 'C:\\Users\\Admin\\OneDrive\\Desktop\\Automatic filling - Copy\\Automatic_filling.pdf'
pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
from django.contrib.auth import authenticate, login


# Views for the app webstore here.

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request,"home.html")

import re

def is_valid_email(email):
    # Regular expression for email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Email validation
        if not is_valid_email(email):
            messages.error(request, "Invalid email format!")
            return redirect('index')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('index')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('index')
        
        if len(username) > 10:
            messages.error(request, "Username must be 10 characters or fewer.")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('index')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('index')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('signin')

    return render(request, "signup.html")


def signin(request):

    if request.method == 'POST' :
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            return render(request,"home.html")
        
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('index')
        
    return render(request,"signin.html")


def Demo(request):
    return render(request, "Demo.html")


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        problem = request.POST.get('problem')

        # Send email using Formspree
        send_mail(
            f"Contact Form Submission from {name}",  # Subject
            f"Name: {name}\nEmail: {email}\nContact: {contact}\nProblem: {problem}",  # Message
            settings.DEFAULT_FROM_EMAIL,  # From email
            ["gireomkar2003@gmail.com"],  # To email (your Formspree email)
            fail_silently=False,
        )
        return render(request, "contact_success.html")  # Render a success page
    return render(request, "contact.html")

def admission(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        contact_info = request.POST.get('contact_info')
        address = request.POST.get('address')
        School = request.POST.get('School')
        branch = request.POST.get('branch')
        Blood = request.POST.get('Blood')
        parent_name = request.POST.get('parent_name')
        Relation = request.POST.get('Relation')
        parent_profession = request.POST.get('parent_profession')

        # Check if date of birth is in the future
        dob = date.fromisoformat(date_of_birth)
        if dob > date.today()  or dob.year > 2020:
            return JsonResponse({'valid': False, 'error_message': 'Date of birth is invalid'})

        # Create a new user
        new_user = User.objects.create_user(
            username = str(first_name) + " " + str(last_name),
            first_name = first_name,
            last_name = last_name,
            date_of_birth = date_of_birth,
            contact_info = contact_info,
            address = address,
            # Add more user fields as needed
        )

        # Generate PDF report
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'contact_info': contact_info,
            'address': address,
            'branch': branch,
            'School' : School,
            'Blood'  : Blood,
            'parent_name': parent_name,
            'parent_profession': parent_profession,
            'Relation': Relation

            # Add more data as necessary
        }

        # Render admission successful pdf page
        pdf_response = generate_pdf_report(user_data)
        return pdf_response

    return render(request, "admission.html")
def store(request):
    context = {
        "products": Product.objects.all(),
        "categories": Category.objects.all()
    }
    return render(request, "store.html",context)

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)

def purchase(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    context = {
        'product': product,
        'user': user
    }
    return render(request, 'purchase.html', context)

def confirm_purchase(request, product_id):
    if request.method == 'POST':
        # Assuming you have a model named PurchaseDetails to store purchase information
        # Retrieve form data and save it to the database
        name = request.POST.get('name')
        address = request.POST.get('address')
        payment_info = request.POST.get('payment')

        # Save purchase details to the database (replace this with your model and save logic)
        # purchase = PurchaseDetails(name=name, address=address, payment_info=payment_info, ...)
        # purchase.save()

        # Fetch the product based on the product_id (for displaying the product details in the confirmation)
        product = get_object_or_404(Product, pk=product_id)

        # Pass the product and purchase details to the confirmation template
        context = {
            'product': product,
            'name': name,
            'address': address,
            'payment_info': payment_info,
            # Add more data as needed
        }

        return render(request, 'confirm_purchase.html', context)
    
def trainers_page(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers.html', {'trainers': trainers})

    # Handle if the request method is not POST (if needed)
    # For example, redirecting to the product detail page or any other view
    return render(request, 'some_other_page.html')

def generate_pdf_report(user_data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admission_report.pdf"'
    today = date.today().strftime("%Y-%m-%d")
    # Create a canvas
    p = canvas.Canvas(response, pagesize=letter)
    
    # image_path = static('img/GTA.jpg')
    image_path = os.path.join(settings.BASE_DIR, 'webstore', 'static', 'img', 'GTA.jpg')


    # Set up text content in the PDF
    # Add more fields as necessary
    

    p.drawImage(image_path,500,710,width=80, height=80)

    p.setFont("Calibri",22)
    p.setFillColorRGB(2,0,0)
    p.drawString(100,730,"Gurukul Taekwondo Acadamy")

    p.setStrokeColor('black')
    p.setLineWidth(2)
    p.line(10,700,600,700)

    p.setStrokeColor('black')
    p.setLineWidth(2)
    p.line(10,650,600,650)

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(20, 610, "Branch:")

    p.setLineWidth(1)
    p.line(65,608,180,608)

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(70, 610, f'{user_data.get("branch")}')

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(300, 610, "Date of Admission:")

    p.setLineWidth(1)
    p.line(410,608,560,608)

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(415, 610, f'{today}')

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(20, 570, "Name of School:")

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(120, 570, f'{user_data.get("School")}')

    p.setFont("Calibri", 24)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(250, 520, "Student Form")


    p.setLineWidth(1)
    p.line(248,518,388,518)

    p.setLineWidth(1)
    p.line(115,568,560,568)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(20, 480,"New Admission")
    p.roundRect(110,473,20,20,2,stroke=1)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(250, 480,"Re-Admission")
    p.roundRect(335,473,20,20,2,stroke=1)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(460, 480,"Renewal Form")
    p.roundRect(550,473,20,20,2,stroke=1)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(20, 435,"Name of the Student:")

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(160, 435, f'{user_data.get("first_name")} {user_data.get("last_name")}')

    p.setLineWidth(1)
    p.line(150,432,470,432)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(20, 410,"Date of Birth:")

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(110, 410, f'{user_data.get("date_of_birth")}')

    p.setLineWidth(1)
    p.line(100,408,300,408)

    p.drawString(305, 410,"(Adhar Card Copy required)")

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(20, 385,"Address:")

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(80, 385, f'{user_data.get("address")}')

    p.setLineWidth(1)
    p.line(75,383,470,383)

    p.setLineWidth(1)
    p.line(20,358,470,358)

    # image_path = static('img/GTA.jpg')
    image_path = os.path.join(settings.BASE_DIR, 'webstore', 'static', 'img', 'profile.jpg')

    # Draw the rounded rectangle
    p.setLineWidth(1)
    p.roundRect(480, 340, 90, 120, 3, stroke=1, fill=0)

    p.drawImage(image_path, 485, 345, width=80, height=110, preserveAspectRatio=True)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(30, 325,"Contact Info:")

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(120, 325, f'{user_data.get("contact_info")}')

    p.setLineWidth(1)
    p.line(120,323,300,323)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(20, 290,"Blood group:")

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(110, 290, f'{user_data.get("Blood")}')

    p.setLineWidth(1)
    p.line(100,288,570,288)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(20, 260,"Name of the Parent:")

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(160, 260, f'{user_data.get("parent_name")}')

    p.setLineWidth(1)
    p.line(150,258,570,258)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(20, 235,"Relation:")

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(80, 235, f'{user_data.get("Relation")}')

    p.setLineWidth(1)
    p.line(80,233,300,233)

    p.setFont("Calibri",14)
    p.setFillColorRGB(0,0,0)
    p.drawString(310, 235,"Profession:")

    p.setFont("Calibri", 14)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(380, 235, f'{user_data.get("parent_profession")}')

    p.setLineWidth(1)
    p.line(380,233,570,233)

    p.showPage()
    p.save()
    return response