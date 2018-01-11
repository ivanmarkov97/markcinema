from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Film, Hall, Seance, Ticket
from django.core.files import File
from django.core.files.storage import FileSystemStorage
import json

# Create your views here.

def home(request):
	return HttpResponse("Home page")

@csrf_exempt
def film_view(request, film_id):
	resp_data = {}
	if request.method == "GET":
		resp_data = get_film(request, film_id)
	if request.method == "POST":
		resp_data = post_film(request)
	if request.method == "PUT":
		resp_data = put_film(request, film_id)
	if request.method == "DELETE":
		resp_data = del_film(request, film_id)
	return HttpResponse(json.dumps(resp_data), content_type='application/json')

@csrf_exempt
def hall_view(request, hall_id):
	resp_data = {}
	if request.method == "GET":
		resp_data = get_hall(request, hall_id)
	if request.method == "POST":
		resp_data = post_hall(request)
	if request.method == "PUT":
		resp_data = put_hall(request, hall_id)
	if request.method == "DELETE":
		resp_data = del_hall(request, hall_id)
	return HttpResponse(json.dumps(resp_data), content_type='application/json')

@csrf_exempt
def seance_view(request, seance_id):
	resp_data = {}
	if request.method == "GET":
		resp_data = get_seance(request, seance_id)
	if request.method == "POST":
		resp_data = post_seance(request)
	if request.method == "PUT":
		resp_data = put_seance(request, seance_id)
	if request.method == "DELETE":
		resp_data = del_seance(request, seance_id)
	return HttpResponse(json.dumps(resp_data), content_type='application/json')

@csrf_exempt
def ticket_view(request, ticket_id):
	resp_data = {}
	if request.method == "GET":
		resp_data = get_ticket(request, ticket_id)
	if request.method == "POST":
		resp_data = post_ticket(request)
	if request.method == "PUT":
		resp_data = put_ticket(request, ticket_id)
	if request.method == "DELETE":
		resp_data = del_ticket(request, ticket_id)
	return HttpResponse(json.dumps(resp_data), content_type='application/json')

@csrf_exempt
def ticket_sell(request):
	resp_data = {}
	#try:
	tickets = json.loads(request.body)
	time = tickets['time']
	film = tickets['film']
	hall = tickets['hall']
	cost = tickets['cost']
	places = tickets['places']
	film = Film.objects.get(name=film)
	hall = Hall.objects.get(name=hall)
	seance = Seance.objects.get(time=time, cost=cost, hall=hall, film=film)
	m_tickets = Ticket.objects.all().filter(seance=seance)
	#ticks = []
	#resp_data['data'] = ticks
	#for ticket in m_tickets:
	#	ticks.append(str(ticket))
	#return HttpResponse(json.dumps(resp_data), content_type='application/json')
	place = set()
	row = set()
	for pl in places:
		place.add(int(pl['place']))
	for rw in places:
		row.add(int(rw['row']))
	resp_data['changed'] = 0
	for ticket in m_tickets:
		if ticket.place in place and ticket.row in row:
			ticket.is_free = False
			ticket.save()
			resp_data['changed'] = resp_data['changed'] + 1
	resp_data['result'] = 'OK'
	resp_data['errors'] = ''
	#except:
	#	resp_data['result'] = 'failed'
	#	resp_data['errors'] = 'change ticket error'
	return HttpResponse(json.dumps(resp_data), content_type='application/json')

def get_film(request, film_id):
	resp = {}
	films = []
	resp['data'] = films
	if film_id != "":
		try:
			film_id = int(film_id)
			film = Film.objects.get(pk=film_id)
			films.append({
				'id': film.id,
				'name': film.name,
				'description': film.description,
				'age': film.age,
				'country': film.country,
				'producer': film.producer,
				'duration': film.duration,
				'genre': film.genre,
				'image': film.image_url
			})
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'film not found'
	else:
		for film in Film.objects.all():
			films.append({
				'id': film.id,
				'name': film.name,
				'description': film.description,
				'age': film.age,
				'country': film.country,
				'producer': film.producer,
				'duration': film.duration,
				'genre': film.genre,
				'image': film.image_url
			})
		resp['result'] = 200
		resp['errors'] = ''
	return resp		

def post_film(request):
	resp = {}
	new_film = json.loads(request.body)
	try:
		film = Film.objects.create(
			name = new_film['data']['name'],
			description = new_film['data']['description'],
			age = new_film['data']['age'],
			country = new_film['data']['country'],
			producer = new_film['data']['producer']
		)
		film.save()
		resp['result'] = 200
		resp['errors'] = ''
	except:
		resp['result'] = 500
		resp['errors'] = 'cant create film'
	return resp

def put_film(request, film_id):
	resp = {}
	if film_id != "":
		new_film = json.loads(request.body)
		film_id = int(film_id)
		try:
			film = Film.objects.get(pk=film_id)
			film.name = new_film['data']['name']
			film.description = new_film['data']['description']
			film.age = new_film['data']['age']
			film.country = new_film['data']['country']
			film.producer = new_film['data']['producer']

			film.save()
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 500
			resp['errors'] = 'attribute error'
	else:
		resp['result'] = 404
		resp['errors'] = 'input film_id'
	return resp
 
def del_film(request, film_id):
	resp = {}
	if film_id != "":
		film_id = int(film_id)
		try:
			film = Film.objects.get(pk=film_id)
			film.delete()
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'no such film'
	else:
		resp['result'] = 500
		resp['errors'] = 'input film_id'
	return resp


def get_hall(request, hall_id):
	resp = {}
	halls = []
	resp['data'] = halls
	if hall_id != "":
		try:
			hall_id = int(hall_id)
			hall = Hall.objects.get(pk=hall_id)
			halls.append({
				'id': hall.id,
				'name': hall.name,
				'num_rows': hall.num_rows,
				'num_colums': hall.num_columns,
				'is_valid': hall.is_valid,
			})
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'film not found'
	else:
		for hall in Hall.objects.all():
			halls.append({
				'id': hall.id,
				'name': hall.name,
				'num_rows': hall.num_rows,
				'num_colums': hall.num_columns,
				'is_valid': hall.is_valid,
			})
		resp['result'] = 200
		resp['errors'] = ''
	return resp		

def post_hall(request):
	resp = {}
	new_hall = json.loads(request.body)
	try:
		hall = Hall.objects.create(
			name = new_hall['data']['name'],
			num_rows = new_hall['data']['num_rows'],
			num_columns = new_hall['data']['num_colums'],
			is_valid = new_hall['data']['is_valid']
		)
		hall.save()
		resp['result'] = 200
		resp['errors'] = ''
	except:
		resp['result'] = 500
		resp['errors'] = 'cant create hall'
	return resp

def put_hall(request, hall_id):
	resp = {}
	if hall_id != "":
		new_hall = json.loads(request.body)
		hall_id = int(hall_id)
		try:
			hall = Hall.objects.get(pk=hall_id)
			hall.name = new_hall['data']['name']
			hall.num_rows = new_hall['data']['num_rows']
			hall.num_columns = new_hall['data']['num_colums']
			hall.is_valid = new_hall['data']['is_valid']

			hall.save()
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 500
			resp['errors'] = 'attribute error'
	else:
		resp['result'] = 404
		resp['errors'] = 'input hall_id'
	return resp

def del_hall(request, hall_id):
	resp = {}
	if hall_id != "":
		hall_id = int(hall_id)
		try:
			hall = Hall.objects.get(pk=hall_id)
			hall.delete()
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'no such film'
	else:
		resp['result'] = 500
		resp['errors'] = 'input hall_id'
	return resp


def get_seance(request, seance_id):
	resp = {}
	seances = []
	resp['data'] = seances
	if seance_id != "":
		try:
			seance_id = int(seance_id)
			seance = Seance.objects.get(pk=seance_id)
			seances.append({
				'id': seance.id,
				'time': str(seance.time),
				'cost': seance.cost,
				'hall': str(seance.hall),
				'film': str(seance.film),
			})
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'seance not found'
	else:
		for seance in Seance.objects.all():
			seances.append({
				'id': seance.id,
				'time': str(seance.time),
				'cost': seance.cost,
				'hall': str(seance.hall),
				'film': str(seance.film),
			})
		resp['result'] = 200
		resp['errors'] = ''
	return resp		

def post_seance(request):
	resp = {}
	new_seance = json.loads(request.body)
	try:
		hall = Hall.objects.get(pk=int(new_seance['data']['hall_id']))
		film = Film.objects.get(pk=int(new_seance['data']['film_id']))
		seance = Seance.objects.create(
			time = new_seance['data']['time'],
			cost = new_seance['data']['cost'],
			hall = hall,
			film = film
		)
		seance.save()
		resp['result'] = 200
		resp['errors'] = ''
	except:
		resp['result'] = 500
		resp['errors'] = 'cant create hall'
	return resp

def put_seance(request, seance_id):
	resp = {}
	if seance_id != "":
		new_seance = json.loads(request.body)
		seance_id = int(seance_id)
		try:
			hall = Hall.objects.get(pk=int(new_seance['data']['hall_id']))
			film = Film.objects.get(pk=int(new_seance['data']['film_id']))
			seance = Seance.objects.get(pk=seance_id)
			seance.time = new_seance['data']['time']
			seance.cost = new_seance['data']['cost']
			seance.hall = hall
			seance.film = film

			seance.save()
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 500
			resp['errors'] = 'attribute error'
	else:
		resp['result'] = 404
		resp['errors'] = 'input hall_id'
	return resp

def del_seance(request, seance_id):
	resp = {}
	if seance_id != "":
		seance_id = int(seance_id)
		try:
			seance = Seance.objects.get(pk=seance_id)
			seance.delete()
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'no such seance'
	else:
		resp['result'] = 500
		resp['errors'] = 'input seance_id'
	return resp

def get_ticket(request, ticket_id):
	resp = {}
	tickets = []
	resp['data'] = tickets
	if ticket_id != "":
		try:
			ticket_id = int(ticket_id)
			ticket = Ticket.objects.get(pk=ticket_id)
			tickets.append({
				'id': ticket.id,
				'seance': str(seance),
				'film': str(seance.film),
				'place': ticket.place,
				'row': ticket.row,
				'is_free': ticket.is_free
			})
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'ticket not found'
	elif request.GET.get('hall'):
		try:
			hall_id = int(request.GET['hall'])
			hall = Hall.objects.get(pk=hall_id)
			seance = Seance.objects.all().filter(hall=hall)
			ticket = Ticket.objects.all().filter(seance=seance)
			tickets.append({
				'id': ticket.id,
				'seance': str(seance),
				'film': str(seance.film),
				'place': ticket.place,
				'row': ticket.row,
				'is_free': ticket.is_free
			})
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'hall not found'
	elif request.GET.get('film'):
		try:
			film_id = int(request.GET['film'])
			film = Film.objects.get(pk=film_id)
			seance = Seance.objects.all().filter(film=film)
			ticket = Ticket.objects.all().filter(seance=seance)
			tickets.append({
				'id': ticket[i].id,
				'seance': str(seance[0]),
				'film': str(seance[0].film),
				'place': ticket[i].place,
				'row': ticket[i].row,
				'is_free': ticket[i].is_free
			})
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'film not found'
	elif request.GET.get('seance'):
		#try:
		seance_id = int(request.GET['seance'])
		seance = Seance.objects.all().get(pk=seance_id)
		ticket = Ticket.objects.all().filter(seance=seance)
		i = 0
		while i < len(ticket):
			tickets.append({
				'id': ticket[i].id,
				'seance': str(seance),
				'hall': str(seance.hall),
				'film': str(seance.film),
				'place': ticket[i].place,
				'row': ticket[i].row,
				'is_free': ticket[i].is_free
			})
			i = i + 1
		resp['result'] = 200
		resp['errors'] = ''
		#except:
		#	resp['result'] = 404
		#	resp['errors'] = 'seance not found'		
	else:
		for ticket in Ticket.objects.all():
			tickets.append({
				'id': ticket.id,
				'seance': str(ticket.seance),
				'film': str(ticket.seance.film),
				'place': ticket.place,
				'row': ticket.row,
				'is_free': ticket.is_free
			})
		resp['result'] = 200
		resp['errors'] = ''
	return resp	


def post_ticket(request):
	resp = {}
	new_ticket = json.loads(request.body)
	if new_ticket['data']['all'] == True:
		try:
			seance = Seance.objects.get(pk=int(new_ticket['data']['seance_id']))
			num_rows = seance.hall.num_rows
			num_columns = seance.hall.num_columns
			num_places = num_rows * num_columns
			i = 0
			j = 0
			resp['row'] = num_rows
			resp['col'] = num_columns
			while i < num_rows:
				while j < num_columns:
					ticket = Ticket.objects.create(
						seance = seance,
						place = j,
						row = i,
						is_free = True
					)
					ticket.save()
					j = j + 1
				j = 0
				i = i + 1
			resp['result'] = 200
			resp['errors'] = 'created ticket'	
		except:
			resp['result'] = 500
			resp['errors'] = 'can not ceate all tickets'
	else:
		try:
			seance = Seance.objects.get(pk=int(new_ticket['data']['seance_id']))
			ticket = Ticket.objects.create(
				seance = seance,
				place = new_ticket['data']['place'],
				row = new_ticket['data']['row'],
				is_free = new_ticket['data']['is_free']
			)
			seance.save()
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 500
			resp['errors'] = 'cant create ticket'
	return resp

def put_ticket(request, ticket_id):
	resp = {}
	if ticket_id != "":
		new_ticket = json.loads(request.body)
		ticket_id = int(ticket_id)
		try:
			ticket = Ticket.objects.get(pk=ticket_id)
			seance = Seance.objects.get(pk=int(new_ticket['data']['seance_id']))
			ticket.seance = seance
			ticket.place = new_ticket['data']['place']
			ticket.row = new_ticket['data']['row']
			ticket.is_free = new_ticket['data']['is_free']

			ticket.save()
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 500
			resp['errors'] = 'attribute error'
	else:
		resp['result'] = 404
		resp['errors'] = 'input ticket_id'
	return resp

def del_ticket(request, ticket_id):
	resp = {}
	if ticket_id != "":
		ticket_id = int(ticket_id)
		try:
			ticket = Ticket.objects.get(pk=seance_id)
			ticket.delete()
			resp['result'] = 200
			resp['errors'] = ''
		except:
			resp['result'] = 404
			resp['errors'] = 'no such ticket'
	else:
		resp['result'] = 500
		resp['errors'] = 'input ticket_id'
	return resp


