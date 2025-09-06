from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from firebase_admin import firestore
import json

# Initialize Firestore client
db = firestore.client()

def admin_login(request):
    """Simple admin login with username/password check"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Simple hardcoded credentials check
        if username == 'viren_jain' and password == 'viren_sameo_123$':
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'warranty_app/admin_login.html')

def admin_logout(request):
    """Logout admin user"""
    request.session.pop('admin_logged_in', None)
    return redirect('admin_login')

def admin_dashboard(request):
    """Admin dashboard to view warranty form data"""
    # Check if admin is logged in
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    # Get search parameters
    search_query = request.GET.get('search', '').strip()
    
    try:
        # Get all warranty forms from Firebase
        warranty_forms = db.collection('warranty_forms').stream()
        
        # Convert to list of dictionaries
        forms_data = []
        for doc in warranty_forms:
            form_data = doc.to_dict()
            form_data['id'] = doc.id
            forms_data.append(form_data)
        
        # Apply search filter if provided
        if search_query:
            filtered_forms = []
            search_lower = search_query.lower()
            for form in forms_data:
                # Search in name, email, and phone
                name = form.get('name', '').lower()
                email = form.get('email', '').lower()
                phone = form.get('phone', '').lower()
                
                if (search_lower in name or 
                    search_lower in email or 
                    search_lower in phone):
                    filtered_forms.append(form)
            forms_data = filtered_forms
        
        # Pagination
        paginator = Paginator(forms_data, 10)  # 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
            'search_query': search_query,
            'total_forms': len(forms_data),
        }
        
        return render(request, 'warranty_app/admin_dashboard.html', context)
        
    except Exception as e:
        messages.error(request, f'Error fetching data: {str(e)}')
        return render(request, 'warranty_app/admin_dashboard.html', {
            'page_obj': None,
            'search_query': search_query,
            'total_forms': 0,
        })

def admin_form_detail(request, form_id):
    """View detailed information of a specific warranty form"""
    # Check if admin is logged in
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    try:
        # Get specific form from Firebase
        form_doc = db.collection('warranty_forms').document(form_id).get()
        
        if form_doc.exists:
            form_data = form_doc.to_dict()
            form_data['id'] = form_doc.id
            return render(request, 'warranty_app/admin_form_detail.html', {'form': form_data})
        else:
            messages.error(request, 'Form not found')
            return redirect('admin_dashboard')
            
    except Exception as e:
        messages.error(request, f'Error fetching form details: {str(e)}')
        return redirect('admin_dashboard')
