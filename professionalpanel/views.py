from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date, parse_time
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta, date
import json
import logging
from adminpanel.models import Prescription, Professional, Appointment, Patient, Payment, Availability, ReviewRating

logger = logging.getLogger(__name__)

# SAFELY GET PROFESSIONAL - NO CRASHES
def get_professional_instance(request):
    if not request.user.is_authenticated:
        return None
    try:
        return Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        return None

def professional_dashboard(request):
    # Main page render
    pro = get_professional_instance(request)
    return render(request, 'professionalpanel/prof_dash.html', {'pro': pro})

def get_professional_data(request):
    pro = get_professional_instance(request)
    
    # IF USER IS NOT LOGGED IN OR NO PROFILE: Return EMPTY data (Real Zeros, No Fake Data)
    if not pro:
        return JsonResponse({
            'stats': {
                'total_appts': 0, 'total_patients': 0,
                'total_revenue': 0.0, 'avg_rating': 0.0,
                'this_month_appts': 0, 'this_month_rev': 0.0,
                'last_month_rev': 0.0
            },
            'appointments': [],
            'patients': [],
            'earnings': [],
            'availability': {}
        })

    # IF USER IS LOGGED IN: 1. Overview Stats
    total_appointments = Appointment.objects.filter(professional=pro, appointment_status='completed').count()
    total_patients = Patient.objects.filter(appointment__professional=pro, appointment__appointment_status='completed').distinct().count()
    total_revenue = Payment.objects.filter(invoice__appointment__professional=pro, payment_status='completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    avg_rating = ReviewRating.objects.filter(professional=pro).aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = ReviewRating.objects.filter(professional=pro).count()
    
    # 2. Monthly/Last Month Stats
    current_month = date.today().month
    current_year = date.today().year
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1
    
    this_month_appts = Appointment.objects.filter(professional=pro, scheduled_at__month=current_month, scheduled_at__year=current_year).count()
    this_month_rev = Payment.objects.filter(invoice__appointment__professional=pro, payment_status='completed', payment_date__month=current_month, payment_date__year=current_year).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    last_month_rev = Payment.objects.filter(invoice__appointment__professional=pro, payment_status='completed', payment_date__month=last_month, payment_date__year=last_month_year).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # 3. Appointments (Pending, Confirmed)
    appointments = Appointment.objects.filter(professional=pro).exclude(appointment_status='completed').order_by('scheduled_at')
    appt_data = []
    for apt in appointments:
        appt_data.append({
            'id': apt.appointment_id,
            'patient': apt.patient.patient_name,
            'datetime': apt.scheduled_at.strftime("%Y-%m-%d • %H:%M"),
            'note': apt.patient_note,
            'status': apt.appointment_status
        })

    # 4. Patients List with Last Visit
    patients = Patient.objects.filter(appointment__professional=pro, appointment__appointment_status='completed').distinct()
    patient_data = []
    for p in patients:
        last_visit = Appointment.objects.filter(professional=pro, patient=p, appointment_status='completed').order_by('-scheduled_at').first()
        patient_data.append({
            'name': p.patient_name,
            'last_visit': last_visit.scheduled_at.strftime("%b %d, %Y") if last_visit else "No visits yet"
        })

    # 5. Earnings Transactions (Latest)
    earnings = Payment.objects.filter(invoice__appointment__professional=pro, payment_status='completed').order_by('-payment_date')[:10]
    earning_data = []
    for e in earnings:
        earning_data.append({
            'patient': e.invoice.appointment.patient.patient_name,
            'date': e.payment_date.strftime("%Y-%m-%d"),
            'amount': float(e.total_amount)
        })

    # 6. Availability & Settings
    availability = Availability.objects.filter(professional=pro)
    avail_data = {}
    for a in availability:
        if a.is_available:
            day = a.day_of_week
            if day not in avail_data:
                avail_data[day] = [] 
            avail_data[day].append({
                'start': a.start_time.strftime("%H:%M"),
                'end': a.end_time.strftime("%H:%M")
            })

    return JsonResponse({
        'stats': {
            'total_appts': total_appointments, 'total_patients': total_patients,
            'total_revenue': float(total_revenue), 'avg_rating': round(avg_rating, 1),
            'this_month_appts': this_month_appts, 'this_month_rev': float(this_month_rev),
            'last_month_rev': float(last_month_rev),
            'total_reviews': total_reviews
        },
        'appointments': appt_data,
        'patients': patient_data,
        'earnings': earning_data,
        'availability': avail_data
    })

# --- AVAILABILITY ---
def update_availability_page(request):
    return render(request, 'professionalpanel/update_availability.html')

@csrf_exempt
def update_availability_api(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method. Use POST.'})
    
    pro = get_professional_instance(request)
    if not pro:
        return JsonResponse({'status': 'error', 'message': 'Professional profile not found.'})
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data received.'})
    
    Availability.objects.filter(professional=pro).delete()
    schedule = data.get('schedule', {})
    for day_str, sessions in schedule.items():
        day = int(day_str)
        if sessions:
            for slot in sessions:
                start = parse_time(slot.get('start'))
                end = parse_time(slot.get('end'))
                if start and end:
                    Availability.objects.create(
                        professional=pro, day_of_week=day, 
                        start_time=start, end_time=end, is_available=True
                    )

    return JsonResponse({'status': 'success', 'message': 'Availability updated successfully!'})

# --- APPOINTMENT STATUS ---
@csrf_exempt
def update_appointment_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        apt_id = data.get('id')
        new_status = data.get('status')
        apt = get_object_or_404(Appointment, appointment_id=apt_id)
        apt.appointment_status = new_status
        apt.save()
        return JsonResponse({'status': 'success', 'new_status': new_status})
    return JsonResponse({'status': 'error'})

# --- SETTINGS ---
@csrf_exempt
def save_settings(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        if user.is_authenticated:
            user.full_name = data.get('name', user.full_name)
            user.email = data.get('email', user.email)
            user.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

# --- PRESCRIPTIONS ---
@csrf_exempt
def upload_prescription(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    
    pro = get_professional_instance(request)
    if not pro:
        return JsonResponse({'status': 'error', 'message': 'Please log in as a Professional to upload prescriptions.'})
    
    patient_id = request.POST.get('patient_id')
    doc_name = request.POST.get('doc_name')
    special_note = request.POST.get('special_note')
    file = request.FILES.get('file')

    if file:
        ext = file.name.split('.')[-1].lower()
        if ext not in ['png', 'jpg', 'jpeg']:
            return JsonResponse({'status': 'error', 'message': 'Only PNG and JPG files are allowed.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded.'})
    
    patient = get_object_or_404(Patient, id=patient_id)
    prescription = Prescription.objects.create(
        professional=pro,
        patient=patient,
        document_name=doc_name if doc_name else file.name,
        notes=special_note,
        file_upload=file
    )
    
    return JsonResponse({'status': 'success', 'message': 'Prescription uploaded successfully!', 'id': prescription.id})

def get_recent_prescriptions(request):
    pro = get_professional_instance(request)
    if not pro:
        return JsonResponse([], safe=False)
    
    recent = Prescription.objects.filter(professional=pro).order_by('-uploaded_at')[:5]
    data = []
    for r in recent:
        data.append({
            'id': r.id,
            'patient': r.patient.patient_name,
            'doc_name': r.document_name or r.file_upload.name.split('/')[-1],
            'uploaded': r.uploaded_at.strftime("%b %d, %Y"),
            'file_url': f'/professionalpanel/view-prescription/{r.id}/'
        })
    return JsonResponse(data, safe=False)

def view_prescription(request, pk):
    prescription = get_object_or_404(Prescription, id=pk)
    # Security check
    if not request.user.is_authenticated or prescription.professional.user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    return FileResponse(prescription.file_upload.open(), content_type='image/jpeg')

# --- ANALYTICS ---
def analytics_view(request):
    pro = get_professional_instance(request)
    
    if not pro:
        return render(request, 'professionalpanel/analytics.html', {
            'total_patients': 0, 'total_revenue': 0, 'total_appts': 0, 'labels': [], 'values': []
        })
    
    total_patients = Patient.objects.filter(appointment__professional=pro, appointment__appointment_status='completed').distinct().count()
    total_revenue = Payment.objects.filter(invoice__appointment__professional=pro, payment_status='completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_appts = Appointment.objects.filter(professional=pro, appointment_status='completed').count()
    
    monthly_data = Payment.objects.filter(
        invoice__appointment__professional=pro, 
        payment_status='completed'
    ).annotate(month=TruncMonth('payment_date')).values('month').annotate(total=Sum('total_amount')).order_by('-month')[:6]
    
    labels = [d['month'].strftime('%b %Y') for d in monthly_data][::-1]
    values = [float(d['total']) for d in monthly_data][::-1]
    
    return render(request, 'professionalpanel/analytics.html', {
        'total_patients': total_patients,
        'total_revenue': total_revenue,
        'total_appts': total_appts,
        'labels': labels,
        'values': values
    })

def prescriptions_list(request):
    pro = get_professional_instance(request)
    if not pro:
        return render(request, 'professionalpanel/prescriptions.html', {'prescriptions': []})
    
    prescriptions = Prescription.objects.filter(professional=pro).order_by('-uploaded_at')
    return render(request, 'professionalpanel/prescriptions.html', {'prescriptions': prescriptions})