# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import random
from bs4 import BeautifulSoup
import re
# Create your views here.

@csrf_exempt
def web_sperant(request):
	if request.method == 'POST':
		authorization = request.META.get('HTTP_AUTHORIZATION')
		if authorization == 'maVyMnGP8gXVZPhp83eQu6P4DyxxXp':
			data = json.loads(request.body)
			print 'DEBERIA IMPRIMIR DATA AQUI'
			print data
			email = data['email']
			fname = data['fname']
			lname = data['lname']
			#main_telephone = data['main_telephone']
			source_id = data['source_id']
			document = str(data['document'])
			message = data['message']
			project_related = data['project_related']
			sellers = str(data['seller_id'])
			seller = random.choice(sellers.split())
			seller_id = int(seller.split('|')[0])
			seller_email = seller.split('|')[1]
			token = data['token']
			url = 'https://api.sperant.com/v2/clients'
			headers = {
				'Authorization': 'Bearer %s' % (token),
				'Cache-Control': 'no-cache',
				'Content-Type': 'application/json'
			}
			if document:
				if document == '':
					info = {
						'data': {
							'email': email,
							'fname': fname,
							'lname': lname,
							'main_telephone': main_telephone,
							'source_id': source_id,
							'project_related': project_related,
							'seller_id': seller_id
						}
					}
				else:
					info = {
						'data': {
							'email': email,
							'fname': fname,
							'lname': lname,
							'main_telephone': main_telephone,
							'document': document,
							'source_id': source_id,
							'project_related': project_related,
							'seller_id': seller_id
						}
					}
			else:
				info = {
					'data': {
						'email': email,
						'fname': fname,
						'lname': lname,
						'main_telephone': main_telephone,
						'document': document,
						'source_id': source_id,
						'project_related': project_related,
						'seller_id': seller_id
					}
				}
			r = requests.post(url, headers=headers, json=info, verify=False)
			if r.status_code == 201:
				print 'GENIAL FUNCIONANDO'
				data = r.json()
				print data
				proyecto = data['client']['projects_related'][0]['name']
				nombre = '%s %s' % (fname, lname)
				captacion = data['client']['captation_way']
				#parte de mailgun
				auth = ('api', 'key-68d719923cdad783196b7c68aedb927a')
				url = 'https://api.mailgun.net/v3/go.monomedia.pe/messages'
				data = {
					'from': 'Mono Media <postmaster@go.monomedia.pe>',
					'to': ['demoonkevin@gmail.com'],
					#'to': ['carlos.huby@wescon.pe', 'sandra.calderon@wescon.pe', '%s' % seller_email],
					'subject': 'Nuevo prospecto para %s' % (proyecto),
					'text': 'Se ha creado un nuevo prospecto para el proyecto %s, proveniente de %s\nNombre: %s\nEmail: %s\nMensaje:%s\n Puedes verlo en Sperant.' % (proyecto, captacion, nombre, email, message)				
				}
				r = requests.post(url, auth=auth, data=data)
				#fin mailgun
				return HttpResponse('Success')
			else:
				return HttpResponse('Error, %s, %s' % (r.status_code, r.text))
		else:
			return HttpResponseForbidden('Bad Password')

@csrf_exempt
def send_sperant(request):
	if request.method == 'POST':
		authorization = request.META.get('HTTP_AUTHORIZATION')
		if authorization == 'maVyMnGP8gXVZPhp83eQu6P4DyxxXp':
			data = json.loads(request.body)
			email = data['email']
			fname = data['fname']
			lname = data['lname']
			main_telephone = str(data['main_telephone'])
			if main_telephone != '':
				main_telephone = main_telephone[3:len(main_telephone)]
			sellers = str(data['seller_id'])
			seller = random.choice(sellers.split())
			seller_id = int(seller.split('|')[0])
			seller_email = seller.split('|')[1]
			source_id = data['source_id']
			document = str(data['document'])
			project_related = data['project_related']
			token = data['token']
			url = 'https://api.sperant.com/v2/clients'
			headers = {
				'Authorization': 'Bearer %s' % (token),
				'Cache-Control': 'no-cache',
				'Content-Type': 'application/json'
			}
			if document:
				if document == '':
					info = {
						'data': {
							'email': email,
							'fname': fname,
							'lname': lname,
							'main_telephone': main_telephone,
							'source_id': source_id,
							'project_related': project_related,
							'seller_id': seller_id
						}
					}
				else:
					info = {
						'data': {
							'email': email,
							'fname': fname,
							'lname': lname,
							'main_telephone': main_telephone,
							'document': document,
							'source_id': source_id,
							'project_related': project_related,
							'seller_id': seller_id
						}
					}
			else:
				info = {
					'data': {
						'email': email,
						'fname': fname,
						'lname': lname,
						'main_telephone': main_telephone,
						'document': document,
						'source_id': source_id,
						'project_related': project_related,
						'seller_id': seller_id
					}
				}
			r = requests.post(url, headers=headers, json=info, verify=False)
			print r.text
			if r.status_code == 201:
				print 'GENIAL FUNCIONANDO'
				data = r.json()
				print data
				proyecto = data['client']['projects_related'][0]['name']
				nombre = '%s %s' % (fname, lname)
				captacion = data['client']['captation_way']
				#parte de mailgun
				auth = ('api', 'key-68d719923cdad783196b7c68aedb927a')
				url = 'https://api.mailgun.net/v3/go.monomedia.pe/messages'
				data = {
					'from': 'Mono Media <postmaster@go.monomedia.pe>',
					'to': ['carlos.huby@wescon.pe', 'sandra.calderon@wescon.pe', '%s' % seller_email],
					'subject': 'Nuevo prospecto para %s' % (proyecto),
					'text': 'Se ha creado un nuevo prospecto para el proyecto %s, proveniente de %s\nNombre: %s\nEmail: %s\n Puedes verlo en Sperant.' % (proyecto, captacion, nombre, email)				
				}
				r = requests.post(url, auth=auth, data=data)
				#fin mailgun
				return HttpResponse('Success')
			else:
				return HttpResponse('Error, %s, %s' % (r.status_code, r.text))
		else:
			print authorization
			return HttpResponseForbidden('Bad Password')

@csrf_exempt
def nexo_sperant(request):
	if request.method == 'POST':
		authorization = request.META.get('HTTP_AUTHORIZATION')
		if authorization == 'maVyMnGP8gXVZPhp83eQu6P4DyxxXp':
			data = json.loads(request.body)
			project_related = data['project_related']
			token = data['token']
			sellers = str(data['seller_id'])
			seller = random.choice(sellers.split())
			seller_id = int(seller.split('|')[0])
			seller_email = seller.split('|')[1]
			source_id = data['source_id']
			html = data['html']
			soup = BeautifulSoup(html, 'html.parser')
			fname = soup.find('span', text='Nombre: ').parent.findChildren()[1].text
			lname = soup.find('span', text='Apellido: ').parent.findChildren()[1].text
			email = soup.find('span', text='Correo: ').parent.findChildren()[1].text
			document = str(soup.find('span', text='DNI: ').parent.findChildren()[1].text)
			main_telephone = soup.find('span', text=re.compile('fono')).parent.findChildren()[1].text
			url = 'https://api.sperant.com/v2/clients'
			headers = {
				'Authorization': 'Bearer %s' % (token),
				'Cache-Control': 'no-cache',
				'Content-Type': 'application/json'
			}
			info = {
				'data': {
					'email': email,
					'fname': fname,
					'lname': lname,
					'main_telephone': main_telephone,
					'document': document,
					'source_id': source_id,
					'project_related': project_related,
					'seller_id': seller_id
				}
			}
			r = requests.post(url, headers=headers, json=info, verify=False)
			if r.status_code == 201:
				print 'GENIAL FUNCIONANDO'
				data = r.json()
				print data
				proyecto = data['client']['projects_related'][0]['name']
				nombre = '%s %s' % (fname, lname)
				captacion = data['client']['captation_way']
				#parte de mailgun
				auth = ('api', 'key-68d719923cdad783196b7c68aedb927a')
				url = 'https://api.mailgun.net/v3/go.monomedia.pe/messages'
				data = {
					'from': 'Mono Media <postmaster@go.monomedia.pe>',
					'to': ['carlos.huby@wescon.pe', 'sandra.calderon@wescon.pe', '%s' % seller_email],
					'subject': 'Nuevo prospecto para %s' % (proyecto),
					'text': 'Se ha creado un nuevo prospecto para el proyecto %s, proveniente de %s\nNombre: %s\nEmail: %s\n Puedes verlo en Sperant.' % (proyecto, captacion, nombre, email)				
				}
				r = requests.post(url, auth=auth, data=data)
				#fin mailgun
				return HttpResponse('Success')
			else:
				return HttpResponse('Error, %s, %s' % (r.status_code, r.text))
		else:
			return HttpResponseForbidden('Bad Password')


@csrf_exempt
def urbania_sperant(request):
	if request.method == 'POST':
		authorization = request.META.get('HTTP_AUTHORIZATION')
		if authorization == 'maVyMnGP8gXVZPhp83eQu6P4DyxxXp':
			data = json.loads(request.body)
			project_related = data['project_related']
			token = data['token']
			sellers = str(data['seller_id'])
			seller = random.choice(sellers.split())
			seller_id = int(seller.split('|')[0])
			seller_email = seller.split('|')[1]
			source_id = data['source_id']
			html = data['html']
			soup = BeautifulSoup(html, 'html.parser')
			pre_name = soup.find('span', text=re.compile('Contacto')).parent.text
			name = pre_name[10:len(pre_name)]
			name_split = name.split()
			pre_email = soup.find('span', text=re.compile('Email')).parent.text
			email = pre_email[7:len(pre_email)]
			main_telephone = str(soup.find('span', text=re.compile('fono')).parent.find('a').get_text())
			if len(name_split) == 1:
				fname = name
				lname = 'Apellido Desconocido'
			elif len(name_split) == 2:
				fname = name_split[0]
				lname = name_split[1]
			elif len(name_split) == 3:
				fname = name_split[0]
				lname = '%s %s' % (name_split[1], name_split[2])
			elif len(name_split) > 3:
				fname = '%s %s' % (name_split[0], name_split[1])
				lname = name[len(fname):len(name)]
			url = 'https://api.sperant.com/v2/clients'
			headers = {
				'Authorization': 'Bearer %s' % (token),
				'Cache-Control': 'no-cache',
				'Content-Type': 'application/json'
			}
			info = {
				'data': {
					'email': email,
					'fname': fname,
					'lname': lname,
					'main_telephone': main_telephone,
					'source_id': source_id,
					'project_related': project_related,
					'seller_id': seller_id
				}
			}
			r = requests.post(url, headers=headers, json=info, verify=False)
			if r.status_code == 201:
				print 'GENIAL FUNCIONANDO'
				data = r.json()
				print data
				proyecto = data['client']['projects_related'][0]['name']
				nombre = '%s %s' % (fname, lname)
				captacion = data['client']['captation_way']
				#parte de mailgun
				auth = ('api', 'key-68d719923cdad783196b7c68aedb927a')
				url = 'https://api.mailgun.net/v3/go.monomedia.pe/messages'
				data = {
					'from': 'Mono Media <postmaster@go.monomedia.pe>',
					'to': ['carlos.huby@wescon.pe', 'sandra.calderon@wescon.pe', '%s' % seller_email],
					'subject': 'Nuevo prospecto para %s' % (proyecto),
					'text': 'Se ha creado un nuevo prospecto para el proyecto %s, proveniente de %s\nNombre: %s\nEmail: %s\n Puedes verlo en Sperant.' % (proyecto, captacion, nombre, email)				
				}
				r = requests.post(url, auth=auth, data=data)
				#fin mailgun
				return HttpResponse('Success')
			else:
				return HttpResponse('Error, %s, %s' % (r.status_code, r.text))
		else:
			return HttpResponseForbidden('Bad Password')
