from django.db import models
from account.models import Account

class Comment(models.Model):
	account		= models.ForeignKey(Account, on_delete = models.SET_NULL, null=True )
	content		= models.CharField(max_length = 500)
	created_at	= models.DateTimeField(auto_now_add=True)
	

	class Meta:
		db_table = "comments"


