from django.shortcuts import render
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from Zoo_management.utils import render_to_pdf
from .models import*

# Create your views here.

def index(request):
	return render(request,'index.html')
def about(request):
	return render(request,'about.html')
def contact(request):
	return render(request,'contact.html')
def gallery(request):
	return render(request,'gallery.html')
from django.db.models import Max
from django.core.mail import send_mail
from django.conf import settings

def booking(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        date = request.POST['date']
        time = request.POST['time']
        count = request.POST['count']
        age_cat = request.POST['cat']

        # Determine price based on category
        if age_cat == 'Adult':
            price = int(count) * 20
        elif age_cat == 'Childrens':
            price = int(count) * 5
        elif age_cat == 'Family Ticket':
            price = int(count) * 40
        elif age_cat == 'Group Ticket':
            price = int(count) * 150
        elif age_cat == 'Camera Ticket':
            price = int(count) * 25
        elif age_cat == 'Hand Held Video camera Ticket':
            price = int(count) * 100
        elif age_cat == 'Professional Video camera Ticket':
            price = int(count) * 1500
        else:
            price = 0  # Default fallback

        # Safely get max ticket_no
        max_ticket = Tbl_booking.objects.aggregate(Max('ticket_no'))['ticket_no__max']
        if max_ticket is None:
            ticket_no = 1
        else:
            ticket_no = max_ticket + 1

        # Save booking
        aa = Tbl_booking(
            price=price,
            count=count,
            name=name,
            email=email,
            date=date,
            time=time,
            age_cat=age_cat,
            status='pending',
            ticket_no=ticket_no
        )
        aa.save()

        # Send confirmation email
        subject = 'Welcome to Thrissur Zoo and Museum'
        message = f'Hi {name},\n\nThank you for your booking.\nYour Ticket Number is: TK{ticket_no}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

        return HttpResponseRedirect('/payment/')
    else:
        return render(request, 'booking.html')

def payment(request):
	if request.method=="POST":
		aa=Tbl_booking.objects.all().update(status='paid')
		pr=Tbl_booking.objects.all()
		for x in pr:
			b_id=x.id
			amount=x.price
		bookid=Tbl_booking.objects.get(id=b_id)
		# amount=request.POST['amount']
		obj=Tbl_payment(book_id=bookid,amount=amount)
		obj.save()
		return HttpResponseRedirect('/booking/')
	else:
		last=Tbl_booking.objects.all()
		for x in last:
			b_id=x.id
			print("=========",b_id)
		var=Tbl_booking.objects.all().filter(id=b_id)
		return render(request,'payment.html',{'var':var})
def view_booking(request):
	if request.method=="POST":
		email=request.POST['email']
		var=Tbl_booking.objects.all().filter(email=email).exclude(status='cancelled')
		return render(request,'booking.html',{'var':var})
	else:
		return render(request,'booking.html')
def cancel_booking(request):
	ii=request.GET['id']
	var=Tbl_booking.objects.all().filter(id=ii).update(status='cancelled')
	# var.delete()
	return HttpResponseRedirect('/view_booking/')

 
def download_as_pdf(request):
    ii=request.GET['id']
    print("ttttttttttttttt ii tttttttttttttttttttt",ii)
    var = Tbl_booking.objects.all().filter(id=ii)
  
    pdf = render_to_pdf('pdf.html', {'var': var})
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=zooTicket.pdf'
    return response


def register(request):
	if request.method=="POST":
		name=request.POST['name']
		city=request.POST['city']
		street=request.POST['street']
		phone=request.POST['phone']
		email=request.POST['email']
		pswd=request.POST['pswd']
		pin=request.POST['pin']
		var=Tbl_user(name=name,city=city,street=street,phone=phone,email=email,pswd=pswd,pin=pin,utype='user')
		var.save()
		txt="""<script>alert('Successfully registered..');window.location='/register/';</script>"""
		return HttpResponse(txt)
	else:
		return render(request,'reg.html')
def login(request):
	if request.method=='POST':
		email=request.POST['email']
		pswd=request.POST['pswd']
		chk=Tbl_user.objects.all().filter(email=email,pswd=pswd,utype='admin')
		chk2=Tbl_user.objects.all().filter(email=email,pswd=pswd,utype='staff')
		chk3=Tbl_user.objects.all().filter(email=email,pswd=pswd,utype='doctor')
		chk4=Tbl_user.objects.all().filter(email=email,pswd=pswd,utype='supplier')
		chk5=Tbl_user.objects.all().filter(email=email,pswd=pswd,utype='user')

		if chk:
			for x in chk:
				request.session['id']=x.id
				return render(request,'Admin/admin_home.html')
		elif chk2:
			for x in chk2:
				request.session['id']=x.id
				return render(request,'staff/staff_home.html')
		elif chk3:
			for x in chk3:
				request.session['id']=x.id
				return render(request,'doctor/doctor_home.html')
		elif chk4:
			for x in chk4:
				request.session['id']=x.id
				return render(request,'Food supplier/supplier_home.html')
		elif chk5:
			for x in chk5:
				request.session['id']=x.id
				return render(request,'User/user_home.html')
		else:
			return render(request,'login.html')
	else:
		return render(request,'login.html')
def logout(request):
	if request.session.has_key('id'):
		del request.session['id']
		logout(request)
		return HttpResponseRedirect('/login/')

# *************************Admin**********************************
def admin_home(request):
	return render(request,'Admin/admin_home.html')
def admin_booking_details(request):
	var=Tbl_booking.objects.all().exclude(status='cancelled')
	var2=Tbl_booking.objects.all().filter(status='cancelled')
	return render(request,'Admin/admin_booking_details.html',{'var':var,'var2':var2})
def admin_add_staff(request):
	if request.method=="POST":
		name=request.POST['name']
		street=request.POST['street']
		city=request.POST['city']
		pin=request.POST['pin']

		phone=request.POST['phone']
		email=request.POST['email']
		pswd=request.POST['pswd']
		aa=Tbl_user(name=name,street=street,city=city,pin=pin,phone=phone,email=email,pswd=pswd,utype='staff')
		aa.save()

		bb=Tbl_login(email=email,pswd=pswd,utype='staff')
		bb.save()
		txt="""<script>alert('successfully registerd..');window.location='/admin_add_staff/';</script>"""
		return HttpResponse(txt)
		# return render(request,'Admin/admin_add_staff.html')
	else:
		return render(request,'Admin/admin_add_staff.html')
def admin_view_staff(request):
	var=Tbl_user.objects.all().filter(utype='staff')
	return render(request,'Admin/admin_view_staff.html',{'var':var})
def admin_add_doctor(request):
	if request.method=="POST":
		name=request.POST['name']
		street=request.POST['street']
		city=request.POST['city']
		pin=request.POST['pin']
		phone=request.POST['phone']
		email=request.POST['email']
		pswd=request.POST['pswd']
		aa=Tbl_user(name=name,street=street,city=city,pin=pin,phone=phone,email=email,pswd=pswd,utype='doctor')
		aa.save()
		bb=Tbl_login(email=email,pswd=pswd,utype='doctor')
		bb.save()
		txt="""<script>alert('successfully registerd..');window.location='/admin_add_doctor/';</script>"""
		return HttpResponse(txt)
		# return render(request,'Admin/admin_add_doctor.html')
	else:
		return render(request,'Admin/admin_add_doctor.html')
def admin_view_doctor(request):
	var=Tbl_user.objects.all().filter(utype='doctor')
	return render(request,'Admin/admin_view_doctor.html',{'var':var})
def admin_add_supplier(request):
	if request.method=="POST":
		name=request.POST['name']
		street=request.POST['street']
		city=request.POST['city']
		pin=request.POST['pin']
		phone=request.POST['phone']
		email=request.POST['email']
		pswd=request.POST['pswd']
		aa=Tbl_user(name=name,street=street,city=city,pin=pin,phone=phone,email=email,pswd=pswd,utype='supplier')
		aa.save()
		bb=Tbl_login(email=email,pswd=pswd,utype='supplier')
		bb.save()
		txt="""<script>alert('successfully registerd..');window.location='/admin_add_supplier/';</script>"""
		return HttpResponse(txt)
		# return render(request,'Admin/admin_add_supplier.html')
	else:
		return render(request,'Admin/admin_add_supplier.html')
def admin_view_supplier(request):
	var=Tbl_user.objects.all().filter(utype='supplier')
	return render(request,'Admin/admin_view_supplier.html',{'var':var})
def admin_view_leaveRequest(request):
	var=Tbl_leave.objects.all()
	return render(request,'Admin/admin_view_leaveRequest.html',{'var':var})
def admin_approve_leave(request):
	ii=request.GET['id']
	var=Tbl_leave.objects.all().filter(id=ii).update(status='approved')
	return HttpResponseRedirect('/admin_view_leaveRequest/')
def admin_reject_leave(request):
	ii=request.GET['id']
	var=Tbl_leave.objects.all().filter(id=ii).update(status='rejected')
	return HttpResponseRedirect('/admin_view_leaveRequest/')
def admin_view_report(request):
	var=Tbl_report.objects.all()
	return render(request,'Admin/admin_view_report.html',{'var':var})
def admin_remove_booking(request):
	ii=request.GET['id']
	book=Tbl_booking.objects.all().filter(id=ii)
	book.delete()
	return HttpResponseRedirect('/admin_booking_details/')
def admin_checked_booking(request):
	ii=request.GET['id']
	book=Tbl_booking.objects.all().filter(id=ii).update(status='checked')
	return HttpResponseRedirect('/admin_booking_details/')
def admin_add_booking(request):
	return render(request,'Admin/admin_add_booking.html')
def admin_add_animal(request):
	if request.method=="POST":
		name=request.POST['name']
		category=request.POST['category']
		scientific_name=request.POST['scientific_name']
		life_span=request.POST['life_span']
		age=request.POST['age']
		food=request.POST['food']
		vaccination=request.POST['vaccination']
		medical_history=request.POST['medical_history']

		aa=Tbl_animal(name=name,category=category,scientific_name=scientific_name,life_span=life_span,age=age,food=food,vaccination=vaccination,medical_history=medical_history)
		aa.save()
		txt="""<script>alert('success..');window.location='/admin_add_animal/';</script>"""
		return HttpResponse(txt)
		# return render(request,'Admin/admin_add_animal.html')
	else:
		return render(request,'Admin/admin_add_animal.html')
def admin_view_animal(request):
	var=Tbl_animal.objects.all()
	return render(request,'Admin/admin_view_animal.html',{'var':var})

# *************************Staff**********************************
def staff_home(request):
	return render(request,'staff/staff_home.html')

def staff_profile(request):
	myid=request.session['id']
	var=Tbl_user.objects.all().filter(id=myid)
	# for x in log:
	# 	email=x.email
	# var=Tbl_user.objects.all().filter(email=email,utype='staff')
	return render(request,'staff/staff_profile.html',{'var':var})
def staff_edit_profile(request):
	myid=request.session['id']
	if request.method=="POST":
		city=request.POST['city']
		pin=request.POST['pin']
		street=request.POST['street']
		phone=request.POST['phone']
		email=request.POST['email']
		pswd=request.POST['pswd']
		aa=Tbl_user.objects.all().filter(id=myid).update(phone=phone,email=email,pswd=pswd,city=city,pin=pin,street=street)
		return HttpResponseRedirect('/staff_profile/')
	else:
		var=Tbl_user.objects.all().filter(id=myid)
		return render(request,'staff/edit_profile.html',{'var':var})
def staff_leave(request):
	myid=request.session['id']
	if request.method=="POST":
		reason=request.POST['reason']
		date=request.POST['date']
		uid=Tbl_user.objects.get(id=myid)
		aa=Tbl_leave(user_id=uid,reason=reason,date=date,status='pending')
		aa.save()
		return HttpResponseRedirect('/staff_leave/')
	else:
		var=Tbl_user.objects.all().filter(id=myid)
		return render(request,'staff/staff_leaveform.html',{'var':var})
def staff_leavestatus(request):
	myid=request.session['id']
	var=Tbl_leave.objects.all().filter(user_id=myid)
	return render(request,'staff/staff_leavestatus.html',{'var':var})
def staff_view_doctor(request):
	var=Tbl_user.objects.all().filter(utype='doctor')
	return render(request,'staff/staff_view_doctors.html',{'var':var})
def staff_doctor_appoinment(request):
	myid=request.session['id']
	if request.method=="POST":
		# name=request.POST['name']
		staff_email=request.POST['email']
		date=request.POST['date']
		time=request.POST['time']
		animal_id=request.POST['animal']
		an_id=Tbl_animal.objects.all().get(id=animal_id)
		ii=request.POST['id']
		uid=Tbl_user.objects.all().get(id=ii)
		aa=Tbl_appoinment(animal_id=an_id,staff_email=staff_email,date=date,time=time,doctor_id=uid,status='pending')
		aa.save()
		return HttpResponseRedirect('/staff_appoinment_status/')
	else:
		idd=request.GET['id']
		var=Tbl_user.objects.all().filter(id=myid)
		var2=Tbl_animal.objects.all()
		return render(request,'staff/doctor_appoinment.html',{'var':var,'idd':idd,'var2':var2})
def staff_appoinment_status(request):
	myid=request.session['id']
	user=Tbl_user.objects.all().filter(id=myid)
	for x in user:
		st_email=x.email
	var=Tbl_appoinment.objects.all().filter(staff_email=st_email)
	return render(request,'staff/staff_appoinment_status.html',{'var':var})
def staff_add_report(request):
	myid=request.session['id']
	var=Tbl_user.objects.all().filter(id=myid)
	if request.method=="POST":
		name=request.POST['name']
		email=request.POST['email']
		report=request.POST['report']
		date=request.POST['date']
		uid=Tbl_user.objects.all().get(id=myid)
		aa=Tbl_report(name=name,email=email,report=report,date=date,status='pending',staff_id=uid)
		aa.save()
		return HttpResponseRedirect('/staff_view_report/')
	else:
		return render(request,'staff/staff_add_report.html',{'var':var})
def staff_view_report(request):
	myid=request.session['id']
	var=Tbl_report.objects.all().filter(staff_id=myid)
	return render(request,'staff/staff_view_report.html',{'var':var})
def staff_remove_report(request):
	ii=request.GET['id']
	var=Tbl_report.objects.all().filter(id=ii)
	var.delete()
	return HttpResponseRedirect('/staff_view_report/')
def staff_view_notice(request):
	var=Tbl_notification.objects.all()
	return render(request,'staff/staff_view_notice.html',{'var':var})
def staff_send_needs(request):
	myid=request.session['id']
	if request.method=="POST":
		needs=request.POST['needs']
		qty=request.POST['qty']
		date=request.POST['date']
		f_id=request.POST['food']
		food_id=Tbl_foodstock.objects.get(id=f_id)
		stid=Tbl_user.objects.get(id=myid)
		aa=Tbl_needs(food_id=food_id,staff_id=stid,needs=needs,food_qty=qty,date=date,status='pending')
		aa.save()
		return HttpResponseRedirect('/staff_send_needs/')
	else:
		food=Tbl_foodstock.objects.all()
		return render(request,'staff/staff_send_needs.html',{'food':food})
def staff_view_needs(request):
	myid=request.session['id']
	var=Tbl_needs.objects.all().filter(staff_id=myid)
	return render(request,'staff/staff_view_needs.html',{'var':var})
def staff_view_fooddetails(request):
	var=Tbl_foodsupply.objects.all()
	return render(request,'staff/staff_view_fooddetails.html',{'var':var})
def staff_add_foodstock(request):
	myid=request.session['id']
	if request.method=="POST":
		name=request.POST['name']
		qty=request.POST['qty']
		cat=request.POST['cat']
		stock=request.POST['stock']
		date=request.POST['date']
		stid=Tbl_user.objects.get(id=myid)
		aa=Tbl_foodstock(staff_id=stid,food_name=name,food_qty=qty,food_category=cat,stock=stock,date=date,status='pending')
		aa.save()
		return HttpResponseRedirect('/staff_add_foodstock/')
	else:
		return render(request,'staff/staff_add_foodstock.html')
def staff_edit_foodstock(request):
	if request.method=="POST":
		qty=request.POST['qty']
		stock=request.POST['stock']
		date=request.POST['date']
		ii=request.POST['id']
		aa=Tbl_foodstock.objects.all().filter(id=ii).update(food_qty=qty,stock=stock,date=date)
		return HttpResponseRedirect('/staff_view_foodstock/')
	else:
		idd=request.GET['id']
		var=Tbl_foodstock.objects.all().filter(id=idd)
		return render(request,'staff/edit_foodstock.html',{'var':var,'idd':idd})

def staff_view_foodstock(request):
	myid=request.session['id']
	var=Tbl_foodstock.objects.all().filter(staff_id=myid)
	return render(request,'staff/staff_view_foodstock.html',{'var':var})
def staff_add_vaccine(request):
	myid=request.session['id']
	if request.method=="POST":
		v_name=request.POST['name']
		v_date=request.POST['date']
		discription=request.POST['discription']
		animalid=request.POST['animal']
		an_id=Tbl_animal.objects.get(id=animalid)
		stid=Tbl_user.objects.get(id=myid)
		aa=Tbl_vaccine(animal_id=an_id,staff_id=stid,v_name=v_name,v_date=v_date,discription=discription,status='pending')
		aa.save()
		return HttpResponseRedirect('/staff_add_vaccine/')
	else:
		anm=Tbl_animal.objects.all()
		return render(request,'staff/staff_add_vaccine.html',{'anm':anm})
def staff_view_vaccine(request):
	myid=request.session['id']
	var=Tbl_vaccine.objects.all().filter(staff_id=myid)
	return render(request,'staff/staff_view_vaccine.html',{'var':var})

# *************************Doctor**********************************
def doctor_home(request):
	return render(request,'doctor/doctor_home.html')
def doctor_profile(request):
	myid=request.session['id']
	var=Tbl_user.objects.all().filter(id=myid)
	return render(request,'doctor/doctor_profile.html',{'var':var})
def doctor_edit_profile(request):
    myid = request.session['id']
    if request.method == "POST":
        street = request.POST['street']
        city = request.POST['city']
        pin = request.POST['pin']
        phone = request.POST['phone']
        email = request.POST['email']
        pswd = request.POST['pswd']
        Tbl_user.objects.filter(id=myid).update(
            street=street, city=city, pin=pin,
            phone=phone, email=email, pswd=pswd
        )
        return HttpResponseRedirect('/doctor_profile/')
    else:
        var = Tbl_user.objects.filter(id=myid)
        return render(request, 'doctor/doctor_edit_profile.html', {'var': var})
def doctor_view_request(request):
	myid=request.session['id']
	var=Tbl_appoinment.objects.all().filter(doctor_id=myid,status='pending')
	return render(request,'doctor/doctor_view_request.html',{'var':var})
def doctor_accept_request(request):
	ii=request.GET['id']
	var=Tbl_appoinment.objects.all().filter(id=ii).update(status='accepted')
	return HttpResponseRedirect('/doctor_view_request/')
def doctor_reject_request(request):
	ii=request.GET['id']
	var=Tbl_appoinment.objects.all().filter(id=ii).update(status='rejected')
	return HttpResponseRedirect('/doctor_view_request/')
def doctor_view_acceptedlist(request):
	myid=request.session['id']
	var=Tbl_appoinment.objects.all().filter(doctor_id=myid,status='accepted')
	return render(request,'doctor/doctor_accepted_request.html',{'var':var})
def doctor_view_rejectedlist(request):
	myid=request.session['id']
	var=Tbl_appoinment.objects.all().filter(doctor_id=myid,status='rejected')
	return render(request,'doctor/doctor_rejected_request.html',{'var':var})
def doctor_add_notification(request):
	myid=request.session['id']
	var=Tbl_user.objects.all().filter(id=myid)
	if request.method=="POST":
		# name=request.POST['name']
		# email=request.POST['email']
		notice=request.POST['notice']
		date=request.POST['date']
		uid=Tbl_user.objects.all().get(id=myid)
		aa=Tbl_notification(notice=notice,date=date,status='pending',doctor_id=uid)
		aa.save()
		return HttpResponseRedirect('/doctor_add_notification/')
	else:
		return render(request,'doctor/doctor_add_notification.html',{'var':var})
def doctor_view_notice(request):
	myid=request.session['id']
	var=Tbl_notification.objects.all().filter(doctor_id=myid)
	return render(request,'doctor/doctor_view_notice.html',{'var':var})
def doctor_remove_notice(request):
	ii=request.GET['id']
	var=Tbl_notification.objects.all().filter(id=ii)
	var.delete()
	return HttpResponseRedirect('/doctor_view_notice/')
def doctor_view_vaccine(request):
	var=Tbl_vaccine.objects.all()
	return render(request,'doctor/doctor_view_vaccine.html',{'var':var})

# *************************Food Supplier**********************************
def supplier_home(request):
	return render(request,'Food supplier/supplier_home.html')
def supplier_profile(request):
	myid=request.session['id']
	var=Tbl_user.objects.all().filter(id=myid)
	return render(request,'Food supplier/supplier_profile.html',{'var':var})
def supplier_edit_profile(request):
    myid = request.session['id']
    if request.method == "POST":
        name = request.POST['name']
        street = request.POST['street']
        city = request.POST['city']
        pin = request.POST['pin']
        phone = request.POST['phone']
        email = request.POST['email']
        pswd = request.POST['pswd']

        Tbl_user.objects.filter(id=myid).update(
            name=name,
            street=street,
            city=city,
            pin=pin,
            phone=phone,
            email=email,
            pswd=pswd
        )
        return HttpResponseRedirect('/supplier_profile/')
    else:
        var = Tbl_user.objects.filter(id=myid)
        return render(request, 'Food supplier/supplier_edit_profile.html', {'var': var})

def supplier_add_food(request):
	myid=request.session['id']
	if request.method=="POST":
		food_name=request.POST['name']
		food_qty=request.POST['qty']
		price=request.POST['price']
		cat=request.POST['cat']
		date=request.POST['date']
		sup_id=Tbl_user.objects.all().get(id=myid)
		aa=Tbl_foodsupply(supplier_id=sup_id,food_name=food_name,food_qty=food_qty,food_category=cat,price=price,date=date,status='pending')
		aa.save()
		return HttpResponseRedirect('/supplier_add_food/')
	else:
		return render(request,'Food supplier/supplier_add_fooddetails.html')
def supplier_view_food(request):
	myid=request.session['id']
	var=Tbl_foodsupply.objects.all().filter(supplier_id=myid,status='pending')
	var2=Tbl_foodsupply.objects.all().filter(supplier_id=myid,status='Delivered')
	return render(request,'Food supplier/supplier_view_fooddetails.html',{'var':var,'var2':var2})
def supplier_view_request(request):
	var=Tbl_needs.objects.all()
	return render(request,'Food supplier/supplier_view_request.html',{'var':var})
def supplier_accept_request(request):
	ii=request.GET['id']
	var=Tbl_needs.objects.all().filter(id=ii).update(status='accepted')
	return HttpResponseRedirect('/supplier_view_request/')
def supplier_reject_request(request):
	ii=request.GET['id']
	var=Tbl_needs.objects.all().filter(id=ii).update(status='rejected')
	return HttpResponseRedirect('/supplier_view_request/')
def supplier_complete_fooddetail(request):
	ii=request.GET['id']
	var=Tbl_foodsupply.objects.all().filter(id=ii).update(status='Delivered')
	return HttpResponseRedirect('/supplier_view_food/')
#-------------------------------User---------------------------------
def user_home(request):
	return render(request,'User/user_home.html')
def user_profile(request):
	myid=request.session['id']
	var=Tbl_user.objects.all().filter(id=myid)
	return render(request,'User/user_profile.html',{'var':var})
	
	



