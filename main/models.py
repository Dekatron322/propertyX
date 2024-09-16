from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# from resume.models import Resume


class AppUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	otp_code = models.CharField(default="none",max_length=10)
	

	def __str__(self):
		return self.user.username



class Property(models.Model):
	image_one = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_two = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_three = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_four = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_five = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_six = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_seven = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_eight = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_nine = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_ten = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_eleven = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_twelve = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_thirteen = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_fourtheen = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_fivetheen = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_sixteen = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_seventeen = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_eighteen = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_nineteen = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_twenty = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	image_twenty_one = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	title = models.CharField(max_length=50, default="none")
	price = models.CharField(max_length=30, default="none")
	price_per_sqft = models.CharField(max_length=30, default="none")
	category = models.CharField(max_length=30, default="none")
	description = models.TextField(default="none")

	bedroom_number = models.CharField(max_length=20, default="none")
	bathroom_number = models.CharField(max_length=20, default="none")
	garage = models.CharField(max_length=20, default="none")
	

	address = models.CharField(max_length=120, default="none")
	city = models.CharField(max_length=20, default="none", null=True)
	state = models.CharField(max_length=20, default="none", null=True)
	postal_code = models.CharField(max_length=20, default="none", null=True)
	country = models.CharField(max_length=20, default="none", null=True)
	area = models.CharField(max_length=20, default="none", null=True)
	property_attachment_one = models.FileField(upload_to='account_files/profile_photos/', default="none", null=True)
	property_attachment_two = models.FileField(upload_to='account_files/profile_photos/', default="none", null=True)
	property_attachment_three = models.FileField(upload_to='account_files/profile_photos/', default="none", null=True)
	property_attachment_four = models.FileField(upload_to='account_files/profile_photos/', default="none", null=True)

	property_id = models.CharField(max_length=20, default="none")
	property_size = models.CharField(max_length=20, default="none")
	garage_size = models.CharField(max_length=20, default="none")
	year_built = models.CharField(max_length=20, default="none")
	property_type = models.CharField(max_length=20, default="none")
	property_status = models.CharField(max_length=20, default="none")

	first_floor = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	second_floor = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	third_floor = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	fourth_floor = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none",)
    
	# responsibility = models.TextField(default="none")
	# skill_tag = models.CharField(max_length=2000, default="no skill required", null=True)
	# requirement = models.TextField(default="none")
	

	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

	# reservations = models.ManyToManyField(Application, through="JobApplicationConnector")
	# interviews = models.ManyToManyField(Interview, through="JobInterviewConnector")




	status = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title


class ScheduleTour(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE, )
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    tour_type = models.CharField(max_length=100, default="In Person")
    tour_date = models.DateField()
    tour_time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')

    def __str__(self):
        return self.tour_type


class PropertyLike(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(default=timezone.now)

class PropertyBookmark(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    bookmarked_at = models.DateTimeField(default=timezone.now)


class Solicitor(models.Model):
	profile = models.FileField(upload_to='account_files/profile_photos/', blank=True, default="none")
	name = models.CharField(max_length=100)
	email = models.EmailField()
	phone_number = models.CharField(max_length=120, null=True, blank=True)
	mobile_number = models.CharField(max_length=120, null=True, blank=True)
	twitter = models.CharField(max_length=120, null=True, blank=True)
	facebook = models.CharField(max_length=120, null=True, blank=True)
	instagram = models.CharField(max_length=120, null=True, blank=True)
	likedin = models.CharField(max_length=120, null=True, blank=True)
	position = models.CharField(max_length=120, null=True, blank=True)
	firm_name = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.name


class ReserveProperty(models.Model):
	user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	prop = models.ForeignKey(Property, on_delete=models.CASCADE)
	solicitor = models.ForeignKey(Solicitor, on_delete=models.SET_NULL, null=True, blank=True)
	bookmarked_at = models.DateTimeField(default=timezone.now)        
        
