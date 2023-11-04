from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import UserRecord
from .models import UserImages
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from .models import UserRecord
from app.forms import Imageform
from .forms import CertificateForm
from django.contrib.auth.decorators import login_required





def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        mobile_number = request.POST['mobile']

        if len(pass1) < 8:
            messages.error(request, "Password should be at least 8 characters")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        try:
            myuser = User.objects.create_user(username=email, email=email, password=pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

            # Create a UserRecord for the user
            user_record = UserRecord(user=myuser, first_name=fname, last_name=lname, email=email, mobile_number=mobile_number)
            user_record.save()

            messages.success(request, "Your account has been successfully created")
            return redirect('signin')
        except Exception as e:
            messages.error(request, "Email Id already used")
            return redirect('signup')

    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        pass1 = request.POST.get('pass1', '')

        if email and pass1:  # Check if 'email' and 'pass1' are not empty
            user = authenticate(username=email, password=pass1)

            if user is not None:
                login(request, user)
                fname = user.first_name
                return render(request, "main.html", {'fname': fname})
            else:
                messages.error(request, "Email Id or Password is Wrong")
        else:
            messages.error(request, "Please fill out both email and password fields.")
            return redirect('signin')  # Redirect back to the sign-in page

    # If the user is not authenticated or the request is not POST, render the signin.html template
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')

def main(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        return render(request, "main.html", {'fname': fname})
    else:
        return redirect('signin')




def generate_certificate(request):
    fname = request.user.first_name

    if request.method == 'POST':
        certificate_form = CertificateForm(request.POST)
        if certificate_form.is_valid():
            selected_activities = certificate_form.cleaned_data.get('activity')

            if not selected_activities:
                messages.error(request, "Please select activities for the certificate.")
            else:
                # Custom conditions for selecting certificates based on activities
                selected_templates = []

                if 'essay' in selected_activities:
                    selected_templates.append('essay')

                if 'drawing' in selected_activities:
                    selected_templates.append('drawing')

                if 'fancy_dress' in selected_activities:
                    selected_templates.append('fancy_dress')

                if len(selected_templates) == 0:
                    messages.error(request, "No matching certificate found for the selected activities.")
                else:
                    template_name = None

                    if len(selected_templates) == 1:
                        template_name = f'{selected_templates[0]}_certificate_template.html'
                    elif len(selected_templates) == 2:
                        template_name = f'{selected_templates[0]}_{selected_templates[1]}_certificate_template.html'
                    elif len(selected_templates) == 3:
                        template_name = 'all_three_certificate_template.html'

                    if template_name:
                        # Generate the certificate based on the selected template name
                        # Set the generated certificate in the context and display it on the template
                        generated_certificate = "Your certificate content here."

                        context = {
                            'generated_certificate': generated_certificate,
                            'fname': fname,  # Pass the first name to the certificate template
                        }
                        return render(request, template_name, context)
                    else:
                        return HttpResponse("No matching certificate found for the selected activities.")

    else:
        certificate_form = CertificateForm()

    return render(request, 'generate_certificate.html', {'certificate_form': certificate_form})






def generate_certificate_redirect(request):
    return redirect('generate_certificate')


def upload_images(request, *args, **kwargs):
    if request.method == "POST":
        form = Imageform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['images_uploaded'] = True  # Set the session flag
    else:
        form = Imageform()

    # Get the user's first name
    fname = request.user.first_name  # Assuming the user is logged in

    return render(request, 'main.html', {'form': form, 'fname': fname})



@login_required
def main(request):
    images_uploaded = request.session.get('images_uploaded', False)

    if images_uploaded:
        # Display a success message if images have been uploaded
        messages.success(request, "Images uploaded successfully.")
        # Clear the session flag to prevent showing the message again
        request.session['images_uploaded'] = False

    return render(request, "main.html", {'images_uploaded': images_uploaded})



from .models import UserRecord, UserImages

@staff_member_required
def dashboard(request):
    # Retrieve user data from UserRecord model
    user_data_list = UserRecord.objects.all()

    # Retrieve images from UserImages model
    user_images_list = UserImages.objects.all()

    context = {
        'user_data_list': user_data_list,
        'user_images_list': user_images_list,
    }
    return render(request, 'dashboard.html', context)




@login_required
def table(request):
    # Retrieve user data from UserRecord model
    user_data_list = UserRecord.objects.all()

    # Retrieve associated UserImages objects
    user_images_list = UserImages.objects.filter(user_record__in=user_data_list)

    # Pass the user data and associated images to the template
    context = {
        'user_data_list': user_data_list,
        'user_images_list': user_images_list,
    }

    return render(request, 'table.html', context)
