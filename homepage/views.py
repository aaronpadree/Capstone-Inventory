from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

class HomeView(View):
    template_name = "home.html"
    def get(self, request):        
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'data'      : data,
            'sales'     : sales,
            'purchases' : purchases
        }
        return render(request, self.template_name, context)

class AboutView(TemplateView):
    template_name = "about.html"

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Instantiate the form with POST data
        if form.is_valid():  # Check if the form is valid
            username = form.cleaned_data['admin']  # Get the username
            password = form.cleaned_data['admin123']  # Get the password
            user = authenticate(username=username, password=password)  # Authenticate the user
            if user is not None:  # If the user is authenticated
                login(request, user)  # Log in the user
                return redirect('home')  # Redirect to the home page
    else:
        form = AuthenticationForm()  # If GET request, instantiate an empty form
    return render(request, 'your_template.html', {'form': form})  # Render the login template
    