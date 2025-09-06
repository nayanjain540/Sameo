from django.shortcuts import render
from django.http import HttpResponseRedirect
import firebase_admin
from firebase_admin import credentials, firestore, storage
import uuid
from datetime import datetime
cred = credentials.Certificate("warranty_app/firebase_config.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'sameo-8f004.firebasestorage.app'
})

db = firestore.client()
bucket = storage.bucket()

def category_selection_view(request):
    return render(request, 'warranty_app/category_selection.html')

# def form_view(request):
#     category = request.GET.get('category', '')

#     if request.method == "POST":
#         data = {
#             'category': request.POST.get('category'),
#             'video_type': request.POST.get('video_type'),
#             'model': request.POST.get('model'),
#             'name': request.POST.get('name'),
#             'email': request.POST.get('email'),
#             'phone': request.POST.get('phone'),
#             'platform': request.POST.get('platform'),
#             'shop_name': request.POST.get('shop_name'),
#             'site_name': request.POST.get('site_name'),
#             'serial_number': request.POST.get('serial_number'),
#             'date_of_purchase': request.POST.get('date_of_purchase'),
#             'timestamp': datetime.now()
#         }

#         # Upload invoice
#         file = request.FILES['invoice']
#         filename = f"invoices/{uuid.uuid4()}_{file.name}"
#         blob = bucket.blob(filename)
#         blob.upload_from_file(file)
        
#         # Generate a signed URL that's valid for 1 year (for viewing)
#         from datetime import timedelta
#         signed_url = blob.generate_signed_url(
#             expiration=datetime.now() + timedelta(days=365),
#             method='GET'
#         )
        
#         # Store both the filename and the signed URL
#         data['invoice_filename'] = filename
#         data['invoice_url'] = signed_url

#         db.collection('warranty_forms').add(data)
#         return render(request, 'warranty_app/form.html', {'category': category, 'submitted': True})

#     return render(request, 'warranty_app/form.html', {'category': category})


def form_view(request):
    category = request.GET.get('category', '')

    if request.method == "POST":
        data = {
            'category': request.POST.get('category'),
            'video_type': request.POST.get('video_type'),
            'model': request.POST.get('model'),
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'platform': request.POST.get('platform'),
            'shop_name': request.POST.get('shop_name'),
            'site_name': request.POST.get('site_name'),
            'serial_number': request.POST.get('serial_number'),
            'date_of_purchase': request.POST.get('date_of_purchase'),
            'timestamp': datetime.now()
        }

        # Upload invoice to Firebase Storage
        file = request.FILES['invoice']
        filename = f"invoices/{uuid.uuid4()}_{file.name}"
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_file(file, content_type=file.content_type)

        # Store only the filename (path inside bucket)
        data['invoice_filename'] = filename

        # Optional: generate a permanent public download URL
        # (works if your storage rules allow read access)
        download_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/{filename.replace('/', '%2F')}?alt=media"
        data['invoice_url'] = download_url

        # Save in Firestore
        db = firestore.client()
        db.collection('warranty_forms').add(data)

        return render(request, 'warranty_app/form.html', {
            'category': category,
            'submitted': True
        })

    return render(request, 'warranty_app/form.html', {'category': category})