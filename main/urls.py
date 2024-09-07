from django.urls import path
from . import views

app_name = "main"

urlpatterns = [

	path("", views.IndexView, name="index"),
	path("complete/", views.CompleteSignUpView, name="complete_sign_up"),
	path("app/", views.AppView, name="app"),
	path("sign-in/", views.SignInView, name="sign_in"),
	path("sign-out/", views.SignOutView, name="sign_out"),
	path("forgot-password/", views.ForgotPasswordView, name="forgot_password"),
	path("set-new-password/", views.SetNewPView, name="set_new_p"),
	path("property-detail/<int:property_id>/", views.PropertyDetailView, name="property_detail"),
	# path("about", views.AboutView, name="about"),

]