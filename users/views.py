from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from sensors.models import Bin, Alert

User = get_user_model()

class RegisterView(View):
    template_name = 'users/register.html'
    
    def get(self, request):
        """Show registration form"""
        return render(request, self.template_name)
    
    def post(self, request):
        """Handle registration form submission"""
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        user_type = request.POST.get('user_type', 'resident')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if not all([first_name, last_name, email, username, password1, password2]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, self.template_name)
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, self.template_name)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, self.template_name)
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'A user with this username already exists.')
            return render(request, self.template_name)
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                user_type=user_type,
                address=address,
                city=city,
                state=state,
                postal_code=postal_code
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome to WasteWise, {user.first_name}! Your account has been created successfully.')
            return redirect('users:dashboard')
            
        except Exception as e:
            messages.error(request, f'An error occurred while creating your account: {str(e)}')
            return render(request, self.template_name)

class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(View):
    template_name = 'users/logout.html'
    
    def get(self, request):
        # Logout the user directly on GET request
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')
    
    def post(self, request):
        # Also handle POST requests for backward compatibility
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile_edit.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'

    def get_template_names(self):
        user = self.request.user
        if user.is_superuser or getattr(user, 'user_type', '') in ['admin', 'collector']:
            return ['users/dashboard_collector.html']
        return [self.template_name]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Resident context
        try:
            context['total_pickups'] = user.pickup_schedules.filter(status='completed').count()
            context['pending_pickups'] = user.pickup_schedules.filter(status='pending').count()
            context['recent_pickups'] = user.pickup_schedules.order_by('-created_at')[:5]
        except Exception:
            context['total_pickups'] = 0
            context['pending_pickups'] = 0
            context['recent_pickups'] = []

        # Collector/admin context
        context['total_bins'] = Bin.objects.filter(is_active=True).count()
        context['active_alerts'] = Alert.objects.filter(is_resolved=False).count()
        context['bins_needing_collection'] = Bin.objects.filter(is_active=True).count()  # placeholder
        
        return context


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been updated successfully.')
        return super().form_valid(form)


class DeleteAccountView(LoginRequiredMixin, View):
    template_name = 'users/confirm_delete.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted. We’re sorry to see you go!')
        return redirect('home')
