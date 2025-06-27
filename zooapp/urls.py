from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.index),
    path('about/',views.about),
    path('contact/',views.contact),
    path('register/',views.register),
    path('login/',views.login),
    path('booking/',views.booking),
    path('payment/',views.payment),
    path('view_booking/',views.view_booking),
    path('cancel_booking/',views.cancel_booking),
    path('logout/',views.logout),
    path('gallery/',views.gallery),
    path('download_as_pdf/',views.download_as_pdf),
    
    # Admin
    path('admin_home/',views.admin_home),
    path('admin_booking_details/',views.admin_booking_details),
    path('admin_add_staff/',views.admin_add_staff),
    path('admin_view_staff/',views.admin_view_staff),
    path('admin_add_doctor/',views.admin_add_doctor),
    path('admin_view_doctor/',views.admin_view_doctor),
    path('admin_add_supplier/',views.admin_add_supplier),
    path('admin_view_supplier/',views.admin_view_supplier),
    path('admin_view_leaveRequest/',views.admin_view_leaveRequest),
    path('admin_view_report/',views.admin_view_report),
    path('admin_approve_leave/',views.admin_approve_leave),
    path('admin_reject_leave/',views.admin_reject_leave),
    path('admin_remove_booking/',views.admin_remove_booking),
    path('admin_add_booking/',views.admin_add_booking),
    path('admin_checked_booking/',views.admin_checked_booking),
    path('admin_add_animal/',views.admin_add_animal),
    path('admin_view_animal/',views.admin_view_animal),
    

    # Staff
    path('staff_home/',views.staff_home),
    path('staff_profile/',views.staff_profile),
    path('staff_edit_profile/',views.staff_edit_profile),
    path('staff_leave/',views.staff_leave),
    path('staff_leavestatus/',views.staff_leavestatus),
    path('staff_view_doctor/',views.staff_view_doctor),
    path('staff_doctor_appoinment/',views.staff_doctor_appoinment),
    path('staff_appoinment_status/',views.staff_appoinment_status),
    path('staff_add_report/',views.staff_add_report),
    path('staff_view_report/',views.staff_view_report),
    path('staff_remove_report/',views.staff_remove_report),
    path('staff_view_notice/',views.staff_view_notice),
    path('staff_send_needs/',views.staff_send_needs),
    path('staff_view_needs/',views.staff_view_needs),
    path('staff_view_fooddetails/',views.staff_view_fooddetails),
    path('staff_add_foodstock/',views.staff_add_foodstock),
    path('staff_view_foodstock/',views.staff_view_foodstock),
    path('staff_add_vaccine/',views.staff_add_vaccine),
    path('staff_view_vaccine/',views.staff_view_vaccine),
    path('staff_edit_foodstock/',views.staff_edit_foodstock),

    # Doctor
    path('doctor_home/',views.doctor_home),
    path('doctor_profile/',views.doctor_profile),
    path('doctor_edit_profile/',views.doctor_edit_profile),
    path('doctor_view_request/',views.doctor_view_request),
    path('doctor_accept_request/',views.doctor_accept_request),
    path('doctor_reject_request/',views.doctor_reject_request),
    path('doctor_view_acceptedlist/',views.doctor_view_acceptedlist),
    path('doctor_view_rejectedlist/',views.doctor_view_rejectedlist),
    path('doctor_add_notification/',views.doctor_add_notification),
    path('doctor_view_notice/',views.doctor_view_notice),
    path('doctor_remove_notice/',views.doctor_remove_notice),
    path('doctor_view_vaccine/',views.doctor_view_vaccine),


    # Food Supplier
    path('supplier_home/',views.supplier_home),
    path('supplier_profile/',views.supplier_profile),
    path('supplier_edit_profile/',views.supplier_edit_profile),
    path('supplier_add_food/',views.supplier_add_food),
    path('supplier_view_food/',views.supplier_view_food),
    path('supplier_view_request/',views.supplier_view_request),
    path('supplier_accept_request/',views.supplier_accept_request),
    path('supplier_reject_request/',views.supplier_reject_request),
    path('supplier_complete_fooddetail/',views.supplier_complete_fooddetail),

    #User
    path('user_home/',views.user_home),
    path('user_profile/',views.user_profile),
    

    

]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)