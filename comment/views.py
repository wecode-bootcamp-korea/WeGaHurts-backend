import json
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Comment
from account.utils import login_decorator


class CommentView(View):
	@login_decorator
	def post(self,request):
		data = json.loads(request.body)
		try:
			Comment.objects.create(
					account = request.user,
					content = data['content']
					)

			comment_data = [{
				'id'		: comment.id,
				'name'		: comment.account.name,
				'content'	: comment.content,
				'created_at': comment.created_at
			} for comment in Comment.objects.all()]
			return JsonResponse({ 'data':comment_data },status =200)
			
		except KeyError:
			return JsonResponse({'message':'INVALID_KEYS'},status=400)
		

	@login_decorator
	def get(self,request):
		
		comment_data = [{
                 'id'        : comment.id,
				 'name'      : comment.account.name,
				 'content'   : comment.content,
				 'created_at': comment.created_at
             } for comment in Comment.objects.all()]
		return JsonResponse({ 'data':comment_data },status =200)


