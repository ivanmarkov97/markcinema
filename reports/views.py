from django.shortcuts import render
from django.http import HttpResponse
from .models import Report, FilmProfitReport, SeanceReport
from main_app.models import Ticket
from django.db.models import Sum
from datetime import datetime

# Create your views here.

def home(request):
	return render(request, 'reports/main_report.html', {})

def profit_film_view(request):
	date = request.GET['date']
	year = date[0:4]
	month = date[5:8]
	message = ""
	films = set()
	profit = {}
	tickets = Ticket.objects.filter(is_free=False, seance__time__month=int(month), seance__time__year=int(year))
	for ticket in tickets:
		films.add(str(ticket.seance.film))
	for film in films:
		profit[film] = 0
	for ticket in tickets:
		profit[str(ticket.seance.film)] += ticket.seance.cost
	profit['tickets'] = len(tickets)
	profit['month'] = int(month)
	profit['year'] = int(year)
	report = Report.objects.get(name='Film Profit by month')
	report.description = 'Last modified at ' + str(datetime.now())
	report.save()
	#return HttpResponse(str(profit))

	if len(films) == 0:
		message = 'No tickets for this date'

	context = {
		'message': message,
		'films': films,
		'profit': profit,
		'year': year,
		'month': month,
		'description': 'Last modified at ' + str(datetime.now())
	}
	return render(request, 'reports/film_report.html', context)

def profit_seance_view(request):
	date = request.GET['date']
	context = {
		'reports': Report.objects.all(),
		'date': date,
	}
	return render(request, 'reports/film_report.html', context)

