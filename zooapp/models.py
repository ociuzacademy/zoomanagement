from django.db import models

# Create your models here.

class Tbl_booking(models.Model):
	name=models.CharField(max_length=100,default='')
	email=models.CharField(max_length=100,default='')
	date=models.CharField(max_length=100,default='')
	time=models.CharField(max_length=100,default='')
	age_cat=models.CharField(max_length=100,default='')
	price=models.CharField(max_length=100,default='')
	count=models.CharField(max_length=100,default='')
	ticket_no=models.IntegerField(default='')
	status=models.CharField(max_length=100,default='')

class Tbl_login(models.Model):
	email=models.CharField(max_length=100,default='')
	pswd=models.CharField(max_length=100,default='')
	utype=models.CharField(max_length=100,default='')

class Tbl_user(models.Model):
	name=models.CharField(max_length=100,default='')
	street=models.CharField(max_length=100,default='')
	city=models.CharField(max_length=100,default='')
	pin=models.CharField(max_length=100,default='')
	phone=models.CharField(max_length=100,default='')
	email=models.CharField(max_length=100,default='')
	pswd=models.CharField(max_length=100,default='')
	utype=models.CharField(max_length=100,default='')

class Tbl_animal(models.Model):
	name=models.CharField(max_length=100,default='')
	category=models.CharField(max_length=100,default='')
	scientific_name=models.CharField(max_length=100,default='')
	life_span=models.CharField(max_length=100,default='')
	age=models.CharField(max_length=100,default='')
	food=models.CharField(max_length=100,default='')
	vaccination=models.CharField(max_length=100,default='')
	medical_history=models.CharField(max_length=100,default='')

class Tbl_leave(models.Model):
	user_id=models.ForeignKey(Tbl_user,on_delete=models.CASCADE,default='')
	reason=models.CharField(max_length=100,default='')
	date=models.CharField(max_length=100,default='')
	status=models.CharField(max_length=100,default='')

class Tbl_appoinment(models.Model):
	doctor_id=models.ForeignKey(Tbl_user,on_delete=models.CASCADE,default='')
	animal_id=models.ForeignKey(Tbl_animal,on_delete=models.CASCADE,default='')
	staff_email=models.CharField(max_length=100,default='')
	date=models.CharField(max_length=100,default='')
	time=models.CharField(max_length=100,default='')
	status=models.CharField(max_length=100,default='')

class Tbl_report(models.Model):
	staff_id=models.ForeignKey(Tbl_user,on_delete=models.CASCADE,default='')
	name=models.CharField(max_length=100,default='')
	email=models.CharField(max_length=100,default='')
	report=models.CharField(max_length=100,default='')
	date=models.CharField(max_length=100,default='')
	status=models.CharField(max_length=100,default='')

class Tbl_notification(models.Model):
	doctor_id=models.ForeignKey(Tbl_user,on_delete=models.CASCADE,default='')
	notice=models.CharField(max_length=100,default='')
	date=models.CharField(max_length=100,default='')
	status=models.CharField(max_length=100,default='')

class Tbl_foodsupply(models.Model):
	supplier_id=models.ForeignKey(Tbl_user,on_delete=models.CASCADE,default='')
	food_name=models.CharField(max_length=100,default='')
	food_qty=models.CharField(max_length=100,default='')
	food_category=models.CharField(max_length=100,default='')
	price=models.CharField(max_length=100,default='')
	date=models.CharField(max_length=100,default='')
	status=models.CharField(max_length=100,default='')

class Tbl_foodstock(models.Model):
	staff_id=models.ForeignKey(Tbl_user,on_delete=models.CASCADE,default='')
	food_name=models.CharField(max_length=100,default='')
	food_qty=models.CharField(max_length=100,default='')
	food_category=models.CharField(max_length=100,default='')
	stock=models.CharField(max_length=100,default='')
	date=models.CharField(max_length=100,default='')
	status=models.CharField(max_length=100,default='')

class Tbl_needs(models.Model):
	staff_id=models.ForeignKey(Tbl_user,on_delete=models.CASCADE,default='')
	food_id=models.ForeignKey(Tbl_foodstock,on_delete=models.CASCADE,default='')
	needs=models.CharField(max_length=100,default='')
	food_qty=models.CharField(max_length=100,default='')
	date=models.CharField(max_length=100,default='')
	status=models.CharField(max_length=100,default='')

class Tbl_vaccine(models.Model):
	staff_id=models.ForeignKey(Tbl_user,on_delete=models.CASCADE,default='')
	animal_id=models.ForeignKey(Tbl_animal,on_delete=models.CASCADE,default='')
	v_name=models.CharField(max_length=100,default='')
	v_date=models.CharField(max_length=100,default='')
	discription=models.CharField(max_length=100,default='')
	status=models.CharField(max_length=100,default='')
	
class Tbl_payment(models.Model):
	book_id=models.ForeignKey(Tbl_booking,on_delete=models.CASCADE,default='')
	amount=models.CharField(max_length=100,default='')
	
	
	

