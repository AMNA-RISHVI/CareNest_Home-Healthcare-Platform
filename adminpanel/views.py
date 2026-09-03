from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from .models import User, Professional, Patient, Appointment, Payment, Feedback
from datetime import datetime
import pandas as pd
import io

# --- DASHBOARD OVERVIEW ---
def dashboard(request):
    # 1. Calculate KPI cards
    total_users = User.objects.filter(role='patient', status=True).count()
    active_pros = Professional.objects.filter(verify_status='approved').count()
    current_month = datetime.now().month
    monthly_appts = Appointment.objects.filter(scheduled_at__month=current_month).count()
    total_revenue = Payment.objects.filter(payment_status='completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # 2. Revenue Trend (Last 6 months)
    revenue_trend = {}
    for i in range(6, 0, -1):
        month = datetime.now().month - i
        if month <= 0: month += 12
        rev = Payment.objects.filter(payment_date__month=month, payment_status='completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        revenue_trend[f"Month {month}"] = float(rev)

    # 3. Top Services
    top_services = Appointment.objects.values('professional__specialization__description').annotate(count=Count('id')).order_by('-count')[:5]
    
    # 4. Recent Appointments
    recent_appts = Appointment.objects.select_related('patient', 'professional').order_by('-scheduled_at')[:5]

    # 5. Platform Health
    platform_health = {
        'uptime': 99.9,
        'active_sessions': 128,
        'pending_verifications': Professional.objects.filter(verify_status='pending').count(),
        'reported_issues': Feedback.objects.filter(status='pending').count()
    }

    context = {
        'total_users': total_users, 'active_pros': active_pros, 
        'monthly_appts': monthly_appts, 'total_revenue': f"Rs. {int(total_revenue/100000)}.{int((total_revenue%100000)/10000)}M",
        'revenue_trend': revenue_trend, 'top_services': top_services, 
        'recent_appts': recent_appts, 'platform_health': platform_health,
    }
    return render(request, 'adminpanel/dashboard.html', context)

# --- PROFESSIONALS LIST & EXPORT ---
def professionals_list(request):
    # Add Avg annotation to fetch average rating from ReviewRating table
    professionals = Professional.objects.select_related('user').annotate(
        avg_rating=Avg('reviewrating__rating')
    ).all()
    
    # Filter Logic (unchanged)
    district = request.GET.get('district')
    status = request.GET.get('status')
    if district:
        professionals = professionals.filter(professionalslocation__district=district)
    if status:
        professionals = professionals.filter(verify_status=status)

    # Export Logic (unchanged)
    if 'export' in request.GET:
        data = list(professionals.values('user__full_name', 'user__email', 'user__district', 'qualifications', 'consultation_fee', 'verify_status'))
        df = pd.DataFrame(data)
        df.rename(columns={'user__full_name':'Name', 'user__email':'Email', 'user__district':'District'}, inplace=True)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=professionals.xlsx'
        with io.BytesIO() as buffer:
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Professionals')
            response.write(buffer.getvalue())
        return response

    return render(request, 'adminpanel/professionals.html', {'professionals': professionals})

# --- PATIENTS LIST ---
def patients_list(request):
    patients = Patient.objects.select_related('user', 'user_subscription__plan').all()
    return render(request, 'adminpanel/patients.html', {'patients': patients})

# --- APPOINTMENTS LIST ---
def appointments_list(request):
    appts = Appointment.objects.select_related('patient', 'professional').all()
    return render(request, 'adminpanel/appointments.html', {'appointments': appts})

# --- REVENUE ANALYTICS ---
# --- REVENUE ANALYTICS ---
def revenue_analytics(request):
    # 1. Top Cards Data (Dynamically calculated)
    total_sum = Payment.objects.filter(payment_status='completed').aggregate(Sum('total_amount'))['total_amount__sum']
    total_sum = float(total_sum) if total_sum else 0.0
    
    avg_val = Payment.objects.filter(payment_status='completed').aggregate(Avg('total_amount'))['total_amount__avg']
    avg_val = float(avg_val) if avg_val else 0.0

    # 2. Monthly Revenue Breakdown (For Horizontal Bars)
    monthly_data = Payment.objects.filter(payment_status='completed').annotate(month=TruncMonth('payment_date')).values('month').annotate(total=Sum('total_amount'), count=Count('id')).order_by('month')
    
    # FIXED: Safely get the highest revenue month, default to 1 if empty
    max_month_total = 1
    if monthly_data:
        max_month_total = max(item['total'] for item in monthly_data)

    # 3. Revenue by District (For Bottom Cards)
    district_data = Payment.objects.filter(payment_status='completed').values('user_subscription__user__district').annotate(total=Sum('total_amount')).order_by('-total')
    
    # FIXED: Safely sum all district revenues, default to 1 if empty (to prevent division by zero)
    total_district_sum = 1
    if district_data:
        total_district_sum = sum(item['total'] for item in district_data)

    context = {
        'total_revenue': total_sum,                 # For the top "Monthly Revenue" card
        'platform_commission': total_sum * 0.15,    # For the top "Platform Commission" card
        'avg_value': avg_val,                       # For the top "Avg. Value" card
        'monthly_data': monthly_data,               # For the "Monthly Revenue Breakdown" chart
        'max_month_total': max_month_total,         # For calculating bar percentages
        'district_data': district_data,             # For the "Revenue by District" section
        'total_district_sum': total_district_sum,   # For calculating district percentages
    }
    return render(request, 'adminpanel/revenue.html', context)

# --- SETTINGS VIEW ---
def settings_page(request):
    if request.method == 'POST':
        user = request.user
        user.save()
    return render(request, 'adminpanel/settings.html')