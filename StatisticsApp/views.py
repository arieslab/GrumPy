from django.shortcuts import render

def statistics_index(request):
    return render(request, 'statisticsIndex.html')