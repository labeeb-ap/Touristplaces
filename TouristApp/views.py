from django.shortcuts import render,redirect
from rest_framework import generics,status
from .models import Places,Images
from .serializers import PlacesSerializer
from django.shortcuts import render
import requests
from django.contrib import messages
API_url = 'https://touristplaces-tk1m.onrender.com/api/create/api'

# Django REST framework core imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class Createapi(generics.ListCreateAPIView):
    queryset=Places.objects.prefetch_related('images')
    serializer_class=PlacesSerializer
    permission_classes=[AllowAny]
    



class Detailapi(generics.RetrieveAPIView):
    queryset=Places.objects.prefetch_related('images')
    serializer_class=PlacesSerializer
    
class Updateapi(generics.UpdateAPIView):
    queryset=Places.objects.prefetch_related('images')
    serializer_class=PlacesSerializer

class Deleteapi(generics.DestroyAPIView):
    queryset=Places.objects.prefetch_related('images')
    serializer_class=PlacesSerializer






def create_place(request):
    # API endpoint to interact with
    api_url = f'{API_url}/create'

    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'wheather': request.POST.get('wheather'),
            'state': request.POST.get('state'),
            'district': request.POST.get('district'),
            'googlemaplink': request.POST.get('googlemaplink'),
        }

        files = request.FILES.getlist('images')
        file_data = []
        for f in files:
            print("File:", f.name)
            file_data.append(('images', (f.name, f, f.content_type)))

        try:
            response = requests.post(api_url, data=data, files=file_data)
            if response.status_code == 201:
                messages.success(request, 'Place inserted successfully!')
                return redirect('create-place')
            else:
                messages.error(request, f'Error: {response.status_code} - {response.text}')
        except requests.exceptions.RequestException as e:
            messages.error(request, f'API error: {str(e)}')

    # Always fetch existing places to display
    try:
        places_response = requests.get(api_url)
        if places_response.status_code == 200:
            places = places_response.json()
        else:
            places = []
            messages.error(request, 'Failed to load places.')
    except requests.exceptions.RequestException as e:
        places = []
        messages.error(request, f'Error fetching places: {str(e)}')

    return render(request, 'create_place.html', {'places': places})






def update_place_view(request, pk):
    api_url = f'{API_url}/{pk}/update/'

    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'wheather': request.POST.get('wheather'),
            'state': request.POST.get('state'),
            'district': request.POST.get('district'),
            'googlemaplink': request.POST.get('googlemaplink'),
        }

        try:
            response = requests.put(api_url, data=data)
            if response.status_code == 200:
                messages.success(request, 'Place updated successfully!')
                return redirect('update-place-form', pk=pk)
            else:
                messages.error(request, f'Error: {response.status_code} - {response.text}')
        except requests.exceptions.RequestException as e:
            messages.error(request, f'API error: {str(e)}')

    # GET request to fetch place data
    try:
        get_resp = requests.get(f'{API_url}/{pk}/details/')
        if get_resp.status_code == 200:
            place = get_resp.json()
        else:
            place = {}
            messages.error(request, 'Place not found')
    except requests.exceptions.RequestException as e:
        place = {}
        messages.error(request, f'Error loading place: {str(e)}')

    return render(request, 'update_place.html', {'place': place})




def delete_place_view(request, pk):
    if request.method == 'POST':
        try:
            api_url = f'http://127.0.0.1:8000/api/{pk}/delete'
            response = requests.delete(api_url)
            if response.status_code == 204:
                messages.success(request, 'Place deleted successfully.')
            else:
                messages.error(request, f'Failed to delete: {response.status_code}')
        except requests.exceptions.RequestException as e:
            messages.error(request, f'API error: {str(e)}')

    return redirect('create-place') 
