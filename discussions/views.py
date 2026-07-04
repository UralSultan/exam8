from django.shortcuts import render

def topic_list(request):
    return render(request, 'discussions/topic_list.html')
