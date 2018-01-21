from django.db import models
import base64
# Create your models here.

class Film(models.Model):
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)
	age = models.IntegerField()
	country = models.CharField(max_length=80)
	producer = models.CharField(max_length=80)
	image = models.ImageField(upload_to='photos/', max_length=255, default='media/fit_service_img9.jpg')
	duration = models.IntegerField(default=0)
	genre = models.CharField(max_length=80, default='')

	def __str__(self):
		return self.name

	@property
	def image_url(self):
		return self.image.url
		#try:
		#	img = open(self.image.path, "rb")
		#	data = base64.b64encode(img.read())
		#	return "data:image/jpg;base64,%s" % data
		#except IOError:
		#	return self.image.url

class Hall(models.Model):
	name = models.CharField(max_length=80)
	num_rows = models.IntegerField()
	num_columns = models.IntegerField()
	is_valid = models.BooleanField()

	def __str__(self):
		return self.name

class Seance(models.Model):
	time = models.DateTimeField()
	cost = models.IntegerField()
	hall = models.ForeignKey('Hall')
	film = models.ForeignKey('Film')

	def __str__(self):
		return str(self.time)

	@property
	def get_month(self):
		return (self.time.month)

	@property
	def get_year(self):
		return (self.time.year)

class Ticket(models.Model):
	seance = models.ForeignKey('Seance')
	place = models.IntegerField()
	row = models.IntegerField()
	is_free = models.BooleanField(default=True)
	#is_sold = models.BooleanField()

	def __str__(self):
		return str(self.place) + " " + str(self.row)
