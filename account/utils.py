import json, jwt, requests
from django.http import JsonResponse,HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from insta_ex.settings import SECRET_KEY
from account.models  import Account

def login_decorator(func):
	def wrapper(self, request, *args, **kwargs):
			try:
				access_token    = request.headers.get('Authorization',None)
				payload         = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
				user            = Account.objects.get(name = payload['name'])
				request.user    = user
		
			except KeyError:
				return HttpResponse(status = 400)

			except jwt.exceptions.DecodeError:
				return JsonResponse({ 'message' : 'INVALID_TOKEN' }, status = 400)

			except Account.DoesNotExist:
				return JsonResponse({ 'message' : 'INVALID_USER' }, status = 400)

			return func(self, request, *args, **kwargs)

	return wrapper


