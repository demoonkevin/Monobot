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

from gmail import GMail, Message

# Create your views here.

def send_sperant(request):
	if request.method == 'POST':
		authorization = request.META.get('HTTP_AUTHORIZATION')
		if authorization == 'maVyMnGP8gXVZPhp83eQu6P4DyxxXp':
			pwd = 'zihnijxjylgjdvlj'
			data = json.loads(request.body)
			email = data['email']
			fname = data['fname']
			lname = data['lname']
			seller_id = data['seller_id']
			source_id = data['source_id']
			document = data['document']
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
						'document': document,
						'source_id': source_id,
						'project_related': project_related,
						'seller_id': seller_id
					}
				}
			r = requests.post(url, headers=headers, json=info, verify=False)
			if r.status_code == 201:
				data = r.json()
				proyecto = data['client']['projects_related'][0]['name']
				nombre = '%s %s' % (fname, lname)
				captacion = data['client']['captation_way']
				gmail = GMail('Wescon <medios.wescon@gmail.com>', pwd)
				msg = Message('Nuevo Prospecto %s' % (proyecto),
					to='Carlos Huby <carlos.huby@wescon.pe>',
					cc = 'Sandra Calderon <sandra.calderon@wescon.pe>',
					text='Se ha creado un nuevo prospecto para el proyecto %s, proveniente de %s \nNombre: %s \nEmail: %s \n' % (proyecto, captacion, nombre, email))
				gmail.send(msg)
				return HttpResponse('Success')
		else:
			return HttpResponseForbidden('Bad Password')


