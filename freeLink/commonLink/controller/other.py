from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def otherAjax(request):
    return render(request, 'commonLink/other.html')
