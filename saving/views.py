from django.shortcuts import render, redirect
from .models import Source, Saving
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import datetime
import csv


@login_required(login_url='/accounts/login')
def index(request):
    sources = Source.objects.all()
    saving = Saving.objects.filter(owner=request.user)
    paginator = Paginator(saving, 5)
    page_num = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_num)

    context = {
        'saving': saving,
        'page_obj': page_obj
    }
    return render(request, 'saving/index.html', context)


@login_required(login_url='/accounts/login')
def add_saving(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'saving/add_saving.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'saving/add_saving.html', context)
        description = request.POST['description']
        date = request.POST['saving_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'saving/add_saving.html', context)

        if not date:
            messages.error(request, 'Savings date is required')
            return render(request, 'saving/add_saving.html', context)

        if not source:
            messages.error(request, 'Source is required')
            return render(request, 'saving/add_saving.html', context)

        Saving.objects.create(owner=request.user, amount=amount,
                               date=date, source=source, description=description)
        messages.success(request, 'Savings saved successfully')
        return redirect('saving')
