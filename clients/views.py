from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import ClientRegistrationForm, UpdateProfileForm, UpdateUserInfoForm, TestimonyForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import State, City, Client, Testimonial
from django.http import JsonResponse
from django.views.generic import ListView

# Create your views here.
class ClientloginView(SuccessMessageMixin, auth_views.LoginView):
    success_url = reverse_lazy('blogger:home')
    template_name = 'clients/login.html'
    success_message = 'You have been logged in successfully'


def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            message = 'Your account was created successfully; Welcome to PAY-T 😊'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('profile')
        else:
            form = ClientRegistrationForm()
            return render(request, 'clients/register.html', {'form': form})
    else:
        form = ClientRegistrationForm()
        return render(request, 'clients/register.html', {'form': form})

def load_states(request):
    country_id = request.GET.get('country')
    states = State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'clients/state_dropdown_list_options.html', {'states': states})

def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'clients/city_dropdown_list_options.html', {'cities': cities})


"""
def load_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    return JsonResponse(list(states.values('id', 'name')), safe=False)

def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)

    
def load_states(request):
    country_id = request.GET.get('country')
    print("Country ID:", country_id)
    states = State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'clients/state_dropdown_list_options.html', {'states': states})

def load_cities(request):
    state_id = request.GET.get('state')
    print("State ID:", state_id)
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'clients/city_dropdown_list_options.html', {'cities': cities})

"""

@login_required    
def profile_view(request):
    profile = get_object_or_404(Client, user=request.user)
    return render(request, 'clients/profile.html', {'profile': profile})


def update_profilezz(request):
    current_user = User.objects.get(id=request.user.id)
    user_form = UpdateUserInfoForm(request.POST or None, instance=current_user)
    profile_form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=current_user.client)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        login(request, current_user)
        message = 'Your Profile has been Updated Successfully ✅'
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('update_profile')
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'clients/update_profile.html', context)
    
def update_profile(request):
    current_user = User.objects.get(id=request.user.id)
    user_form = UpdateUserInfoForm(request.POST or None, instance=current_user)
    profile_form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=current_user.client)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        login(request, current_user)
        message = 'Your Profile has been Updated Successfully ✅'
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('update_profile')
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'clients/update_profile.html', context)

@login_required
def testify(request):

    if request.method == 'POST':
        test_form = TestimonyForm(request.POST or None, request.FILES or None)
        if test_form.is_valid():
            test_form.save()
            mssg = 'Your Testimony has been submitted, thanks for writing about PAY-T'
            messages.add_message(request, messages.SUCCESS, mssg)
            return redirect('about')
        else:
            mesg = 'Sorry, something went wrong. Kindly try again'
            messages.add_message(request, messages.ERROR, mesg)
            test_form = TestimonyForm()
            return render(request, 'clients/testimony.html', {'test_form':test_form})
    else:
        test_form = TestimonyForm()
        return render(request, 'clients/testimony.html', {'test_form':test_form})
    

class TestimonyView(ListView):
    queryset = Testimonial.objects.all()
    template_name = 'blogger/about.html'
    context_object_name = 'testimonials'
    ordering = '-added_on'