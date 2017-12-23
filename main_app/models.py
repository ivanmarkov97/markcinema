from django.db import models

# Create your models here.

class Film(models.Model):
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)
	age = models.IntegerField()
	country = models.CharField(max_length=80)
	producer = models.CharField(max_length=80)

	def __str__(self):
		return self.name

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

class Ticket(models.Model):
	seance = models.ForeignKey('Seance')
	place = models.IntegerField()
	row = models.IntegerField()
	#is_sold = models.BooleanField()

	def __str__(self):
		return str(self.place) + " " + str(self.row)
