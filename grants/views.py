from django.shortcuts import render, get_object_or_404, redirect

from .forms import GrantSearchForm
from .models import Grant
from .search import search_grants

def home(request):
    form = GrantSearchForm()
    return render(request, 'grants/home.html', {'form': form})

def results(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        try:
            # Get relevant grant IDs from search
            grant_ids = search_grants(query)
            
            # Fetch grants in the same order as returned by search
            grants = [Grant.objects.get(id=id) for id in grant_ids]
            
            return render(request, 'grants/results.html', {
                'grants': grants,
                'query': query
            })
        except (ValueError, Exception) as e:
            # If any error occurs during search or grant fetching, show no results
            return render(request, 'grants/results.html', {
                'grants': [],
                'query': query
            })
    return redirect('home')

def detail(request, grant_id):
    grant = get_object_or_404(Grant, id=grant_id)
    return render(request, 'grants/detail.html', {'grant': grant})