from django.db import models

# Create your models here.

class Report(models.Model):
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)

	def __str__(self):
		return str(self.name)

class FilmProfitReport(models.Model):
	month = models.IntegerField(default=0)
	year = models.IntegerField(default=2017)
	film = models.CharField(max_length=80)
	profit = models.IntegerField(default=0)
	report = models.ForeignKey('Report')

	def __str__(self):
		return str(self.month) + " " + str(self.year) + " " + str(self.profit)

class SeanceReport(models.Model):
	month = models.IntegerField(default=0)
	year = models.IntegerField(default=2017)
	cost = models.IntegerField(default=0)
	time = models.DateTimeField()
	tickets = models.IntegerField(default=0)

	def __str__(self):
		return str(self.month) + " " + str(self.year) + " " + str(self.cost) + " " + str(self.tickets)
