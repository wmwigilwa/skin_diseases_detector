from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm, UserForm
from django.contrib.auth.models import User
from .forms import UserProfileForm
from .models import UserProfile, Disease
from django.contrib.auth.views import PasswordChangeDoneView,PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import numpy as np
from PIL import Image
import datetime
#Model loading
###import tensorflow as tf
###from tensorflow.keras.models import load_model







def index(request):
    return render(request, 'index_new.html')

@login_required(login_url='/login/')
def detect(request):
    return render(request, 'upload_image.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = "Invalid username or password."
    else:
        message = ""
    return render(request, 'login.html', {'message': message})

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    return render(request, 'profile.html')
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def update_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

def user_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def password_change_done_view(request):
    return render(request, 'password_change_done.html')

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
            )
            messages.success(request, 'Password reset email has been sent. Please check your email.')
            return redirect('login') 
    else:
        form = PasswordResetForm()
    
    return render(request, 'forgot_password.html', {'form': form})

#Making predictions
def upload_image(request):
    if request.method == 'POST' and request.FILES:
        if not request.FILES['image']:
            messages.error(request, 'Plesse upload an image')
            return redirect(upload_image)
        uploaded_image = request.FILES['image']
        
        # Generate a timestamp for the image file name
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        image_name = f"{timestamp}_{uploaded_image.name}"
        
        # Save the uploaded image with the timestamped file name
        with open('media/' + image_name, 'wb') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)
        
        # Perform additional image processing operations
        #Loading an external data
        image = Image.open('media/' + image_name)
        
        #Preprocess the input
        width_size = 100  # Adjust the desired width size
        height_size = 100  # Adjust the desired height size
        image = image.resize((width_size, height_size))
        image = np.array(image)
        image = np.expand_dims(image, axis=0)
        image_tensor = np.vstack([image])
        
        # Make predictions using the loaded model
        # Load the model
        ###loaded_model = load_model('C:/Users/HERMES/Desktop/Uchwara/57%/filtered_model.h5')
        #prediction
        ###predictions = loaded_model.predict(image_tensor)
        
        # Get the predicted label
        ###predicted_label = np.argmax(predictions, axis=1)[0]
        # For trial purpose
        predicted_label = 0
        
        # Mapping between predicted labels and class names
        class_labels = {
            0: 'Acne and Rosacea', 
            1: 'Eczema', 
            2: 'Melanoma Skin Cancer Nevi and Moles',
            3: 'Psoriasis pictures Lichen Planus and related diseases',
            4: 'Scabies Lyme Disease and other Infestations and Bites',
            5: 'Tinea Ringworm Candidiasis and other Fungal Infections',
        }
        
        # Find the predicted label in the class_labels dictionary
        predicted_disease = class_labels.get(predicted_label)
        #disease info
        disease = Disease.objects.filter(disease_name = predicted_disease)
        
        
        # Render the image preview template with the predicted disease
        return render(request, 'image_preview.html', {'disease':disease, 'predicted_disease': predicted_disease})
    
    return render(request, 'upload_image.html')


