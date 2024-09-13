from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Q

from django.core.mail import send_mail

from datetime import datetime
import datetime as dt
import requests

from .forms import UserForm
from .models import AppUser, Property, ScheduleTour, PropertyLike, PropertyBookmark, ReserveProperty, ReserveProperty


import random
import string

def ray_randomiser(length=6):
	landd = string.digits
	return ''.join((random.choice(landd) for i in range(length)))




def IndexView(request):
    if request.method == "POST":
        form = UserForm(request.POST or None, request.FILES or None)
        email = request.POST.get("username")

        if request.POST.get("password2") != request.POST.get("password1"):
            messages.warning(request, "Make sure both passwords match")
            return HttpResponseRedirect(reverse("main:index"))
        else:
            try:
                AppUser.objects.get(user__email=email)
                messages.warning(request, "Email Address already taken, try another one!")
                return HttpResponseRedirect(reverse("main:index"))
            except AppUser.DoesNotExist:
                user = form.save(commit=False)
                user.set_password(request.POST.get("password1"))
                user.save()

                app_user = AppUser.objects.create(user=user)
                app_user.otp_code = ray_randomiser()
                app_user.save()

                user.email = email
                user.save()

                if user.is_active:
                    login(request, user)
                    messages.warning(request, "Authenticate your account, your OTP code has been sent to your email.")
                    return HttpResponseRedirect(reverse("main:complete_sign_up"))

    else:
        app_user = AppUser.objects.get(user__pk=request.user.id)
        properties = Property.objects.all()
        form = UserForm()
        context = {"form": form, "app_user": app_user, "properties": properties,}
        # return render(request, "main/index.html", context)
    
    return render(request, "main/index.html", context)



def CompleteSignUpView(request):
	if request.method == "POST":
		otp = request.POST.get("otp")
		
		app_user = AppUser.objects.get(user__pk=request.user.id)
		if otp == app_user.otp_code:
			app_user.ec_status = True
			app_user.save()

			messages.warning(request, "Welcome Onboard!")
			return HttpResponseRedirect(reverse("main:app"))

		else:
			messages.warning(request, "Sorry, Invalid OTP Code.")
			return HttpResponseRedirect(reverse("main:complete_sign_up"))


	else:
		context = {}
		return render(request, "main/complete_sign_up.html", context )



def AppView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    properties = Property.objects.all()

    # Extract distinct values for filtering options
    property_types = set(properties.values_list('property_type', flat=True))
    countries = set(properties.values_list('country', flat=True))
    categories = set(properties.values_list('category', flat=True))
    property_statuses = set(properties.values_list('property_status', flat=True))

    if request.method == "POST":
        # Get the selected filters from the POST request
        property_type = request.POST.get("property_type")
        country = request.POST.get("country")
        category = request.POST.get("category")
        property_status = request.POST.get("property_status")
        sort_by = request.POST.get("sort_by", "newest")  # Default to "newest" if not provided

        # Build a query to filter properties based on the selected filters
        filter_criteria = Q()

        if property_type and property_type != "All Property Types":
            filter_criteria &= Q(property_type=property_type)
        if country and country != "All Countries":
            filter_criteria &= Q(country=country)
        if category and category != "All Categories":
            filter_criteria &= Q(category=category)
        if property_status and property_status != "All Status":
            filter_criteria &= Q(property_status=property_status)

        # Apply the filter to the queryset
        properties = properties.filter(filter_criteria)

        # Apply sorting based on the selected option
        if sort_by == "newest":
            properties = properties.order_by('-pub_date')
        elif sort_by == "oldest":
            properties = properties.order_by('pub_date')

    context = {
        "app_user": app_user,
        "properties": properties,
        "property_types": property_types,
        "countries": countries,
        "categories": categories,
        "property_statuses": property_statuses,
    }
    
    return render(request, "main/app.html", context)



#@login_required(login_url='/app/sign-in/')
def PropertyDetailView(request, property_id):
    try:
        app_user = AppUser.objects.get(user__pk=request.user.id)
    except AppUser.DoesNotExist:
        app_user = None

    prop = get_object_or_404(Property, id=property_id)
    
    # Check if the property is already liked, bookmarked, or reserved by the user
    liked = bookmarked = reserved = False
    if app_user:
        liked = PropertyLike.objects.filter(user=app_user, prop=prop).exists()
        bookmarked = PropertyBookmark.objects.filter(user=app_user, prop=prop).exists()
        reserved = ReserveProperty.objects.filter(user=app_user, prop=prop).exists()

    if request.method == "POST":
        if 'schedule_tour' in request.POST:
            if app_user:
                # Handle tour scheduling
                tour_date = request.POST.get("tour_date")
                tour_time = request.POST.get("tour_time")
                tour_type = request.POST.get("tour_type", "In Person")
                message = request.POST.get("message", "")

                ScheduleTour.objects.create(
                    prop=prop,
                    user=app_user,
                    tour_date=tour_date,
                    tour_time=tour_time,
                    tour_type=tour_type,
                    message=message
                )

                messages.success(request, "Tour scheduled successfully!")
                return redirect('main:property_detail', property_id=property_id)
            else:
                messages.error(request, "User not authenticated.")
                return redirect('main:sign_in')

        elif 'like_property' in request.POST:
            if app_user:
                if liked:
                    PropertyLike.objects.filter(user=app_user, prop=prop).delete()
                    messages.success(request, "You have unliked this property.")
                else:
                    PropertyLike.objects.create(user=app_user, prop=prop)
                    messages.success(request, "You have liked this property.")
                return redirect('main:property_detail', property_id=property_id)
            else:
                messages.error(request, "User not authenticated.")
                return redirect('main:sign_in')

        elif 'bookmark_property' in request.POST:
            if app_user:
                if bookmarked:
                    PropertyBookmark.objects.filter(user=app_user, prop=prop).delete()
                    messages.success(request, "You have removed the bookmark from this property.")
                else:
                    PropertyBookmark.objects.create(user=app_user, prop=prop)
                    messages.success(request, "You have bookmarked this property.")
                return redirect('main:property_detail', property_id=property_id)
            else:
                messages.error(request, "User not authenticated.")
                return redirect('main:sign_in')

        elif 'reserve_property' in request.POST:
            if app_user:
                if reserved:
                    ReserveProperty.objects.filter(user=app_user, prop=prop).delete()
                    messages.success(request, "You have removed the reservation.")
                else:
                    ReserveProperty.objects.create(user=app_user, prop=prop)
                    messages.success(request, "You have reserved this property.")
                return redirect('main:reserve_property', property_id=property_id)
            else:
                messages.error(request, "User not authenticated.")
                return redirect('main:sign_in')

    properties = Property.objects.all()

    context = {
        "app_user": app_user,
        "prop": prop,
        "properties": properties,
        "liked": liked,
        "reserved": reserved,
        "bookmarked": bookmarked
    }
    
    return render(request, "main/property_detail.html", context)

def ReservePropertyView(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    
    # Add logic here to handle the reservation confirmation or details.
    
    context = {
        "prop": prop,
    }
    
    return render(request, "main/reserve_property.html", context)

def ForgotPasswordView(request):
    
    if request.method == "POST":
        email = request.POST.get("username")
        
        app_users = AppUser.objects.filter(user__username=email)
        
        if len(app_users) > 0:
            app_user = app_users.last()
            app_user.otp_code = ray_randomiser()
            app_user.save()
            
            # RaySendMail(request, subject="Password Reset.", message="Looks like you lost your password. Kindly use this OTP code; %s to retrieve your account." % (app_user.otp_code), to_email=app_user.user.username, code=app_user.otp_code)

        
            messages.warning(request, "Set new password.")
            return HttpResponseRedirect(reverse("main:set_new_p"))
        
        else:
            messages.warning(request, "Sorry, Invalid OTP code.")
            return HttpResponseRedirect(reverse("main:forgot_password"))
        
        
    else:
        
        context = {}
        return render(request, "main/forgot_password.html", context)
        
        



def SetNewPView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    if request.method == "POST":
        otp = request.POST.get("otp")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        app_users = AppUser.objects.filter(otp_code=otp)
        
        if request.POST.get("password2") != request.POST.get("password1"):
            messages.warning(request, "Make sure both passwords match")
            return HttpResponseRedirect(reverse("main:set_new_p"))
            
        elif len(app_users) > 0:
            app_user = app_users.last()
            
            user = app_user.user
            user.set_password(str(password2))
            user.save()
        
            messages.warning(request, "New Password Created!")
            return HttpResponseRedirect(reverse("main:sign_in"))
            
        else:
            messages.warning(request, "Sorry, Invalid OTP code.")
            return HttpResponseRedirect(reverse("main:set_new_p"))
        
        
    else:
        context = {"app_user":app_user}
        return render(request, "main/set_new_p.html", context)



def SignInView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                
                messages.success(request, "Welcome Onboard")
                return HttpResponseRedirect(reverse("main:app"))
                
            else:
                messages.warning(request, "Sorry, Invalid Login Details")
                return HttpResponseRedirect(reverse("main:sign_in"))
                
        else:
            messages.warning(request, "Sorry, Invalid Login Details")
            return HttpResponseRedirect(reverse("main:sign_in"))

    else:
        context = {}
        return render(request, "main/sign_in.html", context)
        


def DashboardView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    
    # Count the number of liked, reserved, and bookmarked properties
    liked_count = PropertyLike.objects.filter(user=app_user).count()
    reserved_count = ReserveProperty.objects.filter(user=app_user).count()
    bookmarked_count = PropertyBookmark.objects.filter(user=app_user).count()

    context = {
        "app_user": app_user,
        "prop": Property.objects.all(),
        "liked_count": liked_count,
        "reserved_count": reserved_count,
        "bookmarked_count": bookmarked_count,
    }
    
    return render(request, "main/dashboard.html", context)


def LikedView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    
    # Get all properties liked by the user
    liked_properties = Property.objects.filter(propertylike__user=app_user)

    context = {
        "app_user": app_user,
        "liked_properties": liked_properties,
    }
    
    return render(request, "main/liked.html", context)


def BookmarkedView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    
    # Get all properties bookmarked by the user
    bookmarked_properties = Property.objects.filter(propertybookmark__user=app_user)

    context = {
        "app_user": app_user,
        "bookmarked_properties": bookmarked_properties,
    }
    
    return render(request, "main/bookmarked.html", context)

def ReservedView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    
    # Get all properties reserved by the user
    reserved_properties = ReserveProperty.objects.filter(user=app_user).select_related('prop')

    context = {
        "app_user": app_user,
        "reserved_properties": reserved_properties,
    }
    
    return render(request, "main/reserve.html", context)


def SignOutView(request):

    logout(request)
    return HttpResponseRedirect(reverse("main:sign_in"))