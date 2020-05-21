import json
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Account
from insta_ex.settings import SECRET_KEY
import jwt, bcrypt


class SignUpView(View):
	def post(self,request):
		data = json.loads(request.body)
		try:
			if Account.objects.filter(email = data['email']).exists() or Account.objects.filter(name = data['name']).exists():
				return HttpResponse(status=400)

			Account.objects.create(
				email		= data['email'],
				name		= data['name'],
				password	= bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode(),
				)
			return HttpResponse(status=200)
		except KeyError:
			return JsonResponse({"message":"INVALID_KEYS"},status=400)



class SignInView(View):
	def post(self,request):
		data = json.loads(request.body)

		try:
			if Account.objects.filter(name=data['name']).exists():
				account = Account.objects.get(name=data['name'])
			
				if bcrypt.checkpw(data['password'].encode('utf-8'),account.password.encode('utf-8')):
					token = jwt.encode({'name': account.name }, SECRET_KEY, algorithm ="HS256")
					token = token.decode('utf-8')
					return JsonResponse({'Authorization':token},status=200)
				
				return JsonResponse({'message':'비밀번호가 틀렸어요.'},status=401)
		
			return JsonResponse({'message':'미등록 이메일 입니다.'},status=400)

		except KeyError:
			return JsonResponse({"message":"INVALID_KEYS"},status=400)

