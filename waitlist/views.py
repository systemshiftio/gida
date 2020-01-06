from django.shortcuts import render
from waitlist.forms import WaitListForm
from waitlist.models import WaitList

# Create your views here.

def home(request):
    if request.method == 'GET':
        form = WaitListForm()
        return render(request, 'waitlist/index.html', {'form':form})
    else:
        form = WaitListForm()
        return render(request, 'waitlist/index.html',{'form':form})

def subscribe(request):
    if request.method == 'POST':
        message = ''
        form = WaitListForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            last_name = form.cleaned_data.get('lastname')
            first_name = form.cleaned_data.get('firstname')
            location = form.cleaned_data.get('location')
            WaitList.objects.create(email=email, lastname=last_name,
                                            firstname=first_name, location=location)
            message = "You have subscribed to the waiting list"
        else:
            message = "Something is missing in the form"
    else:
        form = WaitListForm()
    return render(request, 'waitlist/index.html', 
            {'form':form, 'message':message})