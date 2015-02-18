from django.db import models


class Url(models.Model):
	id		    = models.AutoField(primary_key=True)
	url			= models.CharField(max_length=256)
	type		= models.CharField(max_length=256)
	crawled_at  = models.DateTimeField(auto_now_add=True)
	created_at  = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now_add=True, auto_now=True)

	class Meta():
		unique_together = ('url', 'type')

class Matrix(models.Model):
	id          		= models.AutoField(primary_key=True)
	url				= models.ForeignKey('Url')
	page_rank   		= models.IntegerField(max_length=256, blank=True)
	domain_authority 	= models.IntegerField(max_length=256, blank=True)
	moz_rank			= models.IntegerField(max_length=256, blank=True)
	alexa_rank			= models.IntegerField(max_length=256, blank=True)
	title				= models.CharField(max_length=256, blank=True)
	description 		= models.TextField()
	alexa_country 		= models.CharField(max_length=256, blank=True)
	alexa_global_rank 	= models.IntegerField(max_length=256, blank=True)
	domain_status 		= models.CharField(max_length=256, blank=True)
	ip_address			= models.CharField(max_length=256, blank=True)
	external_links 		= models.IntegerField(max_length=256, blank=True)
	internal_links 		= models.IntegerField(max_length=256, blank=True)
	index_count 		=  models.IntegerField(max_length=256, blank=True)
	page_authority 		= models.IntegerField(max_length=256, blank=True)
	back_links	 		= models.IntegerField(max_length=256, blank=True)
	created_at  		= models.DateTimeField(auto_now_add=True)
	modified_at 		= models.DateTimeField(auto_now_add=True, auto_now=True)

# Create your models here.
