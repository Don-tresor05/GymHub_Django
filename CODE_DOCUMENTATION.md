# GymHub Django - Complete Code Documentation

This document provides a comprehensive explanation of all code, files, and functionality in the GymHub Django project.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Settings Configuration](#settings-configuration)
4. [Accounts App (Authentication)](#accounts-app-authentication)
5. [Gyms App](#gyms-app)
6. [Members App](#members-app)
7. [Classes App](#classes-app)
8. [Payments App](#payments-app)
9. [Trainers App](#trainers-app)
10. [Analytics App](#analytics-app)
11. [Templates](#templates)
12. [URL Routing](#url-routing)
13. [Authentication System](#authentication-system)
14. [Signup/Registration System](#signupregistration-system)

---

## Project Overview

**GymHub Rwanda** is a Django-based gym management system designed for the Rwandan fitness industry. It supports multiple user roles (Gym Owner, Staff, Trainer, Member) and provides features for gym management, member tracking, class scheduling, payments, and analytics.

**Technology Stack:**
- Django 5.0
- Python 3.8+
- SQLite (development database)
- Bootstrap 5 (frontend)
- Font Awesome (icons)

---

## Project Structure

```
GymHub_Django/
├── accounts/          # User authentication & management
├── gyms/             # Gym management
├── members/          # Member & membership management
├── payments/          # Payment processing
├── classes/          # Class scheduling
├── trainers/         # Trainer management
├── analytics/        # Analytics & reporting
├── gymhub/           # Main project settings
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── media/             # User uploaded files
└── manage.py         # Django management script
```

---

## Settings Configuration

**File:** `gymhub/settings.py`

### Key Settings Explained:

```python
# Custom User Model
AUTH_USER_MODEL = 'accounts.User'
```
**Explanation:** Tells Django to use our custom User model instead of the default one. This allows us to add role and phone_number fields.

```python
# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrPhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```
**Explanation:** Allows users to login with username, email, OR phone number. The custom backend checks all three.

```python
# Timezone
TIME_ZONE = 'Africa/Kigali'
```
**Explanation:** Sets the timezone to Rwanda's timezone for proper date/time handling.

```python
# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
**Explanation:** Configures where uploaded files (gym images, profile photos) are stored and accessed.

```python
# Static Files
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```
**Explanation:** Configures CSS, JavaScript, and image files location.

---

## Accounts App (Authentication)

**Purpose:** Handles user registration, login, logout, and profile management.

### Models

**File:** `accounts/models.py`

```python
class User(AbstractUser):
    ROLE_CHOICES = (
        ('MEMBER', 'Member'),
        ('TRAINER', 'Trainer'),
        ('GYM_OWNER', 'Gym Owner'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    phone_number = models.CharField(max_length=15, blank=True)
```

**Explanation:**
- **Inherits from AbstractUser:** Gets all default Django user fields (username, email, password, etc.)
- **role field:** Determines what the user can do in the system
- **phone_number field:** Stores Rwandan phone numbers (+250 format)
- **get_role_display():** Django automatically creates this method to show "Gym Owner" instead of "GYM_OWNER"

### Views

**File:** `accounts/views.py`

#### 1. `home_view(request)`
```python
def home_view(request):
    """Home page view"""
    return render(request, 'home.html')
```
**Purpose:** Displays the landing page with features and registration options.

#### 2. `register_view(request)`
```python
def register_view(request):
    """General User/Member registration view"""
    gym_id = request.GET.get('gym_id')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        initial_data = {}
        if gym_id:
            initial_data['gym_id'] = gym_id
        form = CustomUserCreationForm(initial=initial_data)
    
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Member Registration'})
```

**Explanation:**
- **GET request:** Shows the registration form
- **POST request:** Processes the form submission
- **gym_id parameter:** If user comes from a gym page, automatically creates membership
- **form.save():** Creates the user account
- **login(request, user):** Automatically logs in the new user
- **messages.success():** Shows success notification

#### 3. `gym_owner_register_view(request)`
```python
def gym_owner_register_view(request):
    """Specialized Gym Owner registration view"""
    if request.method == 'POST':
        form = GymOwnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Gym and Owner account registered successfully!')
            return redirect('home')
    else:
        form = GymOwnerRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Register Your Gym', 'is_gym_owner': True})
```

**Explanation:**
- Similar to `register_view` but uses `GymOwnerRegistrationForm`
- Creates both the user account AND the gym in one step
- Sets `is_gym_owner=True` to show different form layout

#### 4. `profile_view(request)`
```python
def profile_view(request):
    """User profile view"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'accounts/profile.html', {'user': request.user})
```

**Explanation:**
- **@login_required equivalent:** Checks if user is logged in
- Shows user's profile information and memberships/gyms based on role

### Forms

**File:** `accounts/forms.py`

#### 1. `CustomUserCreationForm`
```python
class CustomUserCreationForm(UserCreationForm):
    gym_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'role')
```

**Explanation:**
- **Inherits from UserCreationForm:** Gets username, password1, password2 fields
- **gym_id field:** Hidden field to link member to a gym during registration
- **fields:** Adds email, phone_number, and role to the form

**Key Method - `save()`:**
```python
def save(self, commit=True):
    user = super().save(commit=commit)
    gym_id = self.cleaned_data.get('gym_id')
    if commit and gym_id:
        try:
            from members.models import Membership
            from gyms.models import Gym
            gym = Gym.objects.get(pk=gym_id)
            Membership.objects.get_or_create(user=user, gym=gym)
        except Gym.DoesNotExist:
            pass
    return user
```

**Explanation:**
- Creates the user first
- If `gym_id` is provided, automatically creates a Membership linking user to gym
- `get_or_create()`: Prevents duplicate memberships

#### 2. `GymOwnerRegistrationForm`
```python
class GymOwnerRegistrationForm(CustomUserCreationForm):
    gym_name = forms.CharField(max_length=200, label="Gym Name")
    gym_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Gym Address")
    gym_phone = forms.CharField(max_length=15, label="Gym Contact Phone")
    gym_image = forms.ImageField(required=False, label="Gym Logo/Image")
```

**Explanation:**
- **Inherits from CustomUserCreationForm:** Gets all user fields
- **Additional fields:** gym_name, gym_address, gym_phone, gym_image
- **role is hidden:** Automatically set to 'GYM_OWNER'

**Key Method - `save()`:**
```python
def save(self, commit=True):
    user = super().save(commit=commit)
    user.role = 'GYM_OWNER'
    if commit:
        user.save()
        Gym.objects.create(
            name=self.cleaned_data['gym_name'],
            address=self.cleaned_data['gym_address'],
            contact_phone=self.cleaned_data['gym_phone'],
            image=self.cleaned_data.get('gym_image'),
            owner=user
        )
    return user
```

**Explanation:**
- Creates user account
- Sets role to 'GYM_OWNER'
- Creates the Gym object and links it to the user as owner

### Authentication Backend

**File:** `accounts/backends.py`

```python
class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        try:
            # Check for email or phone number
            user = User.objects.get(Q(email=username) | Q(phone_number=username) | Q(username=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None
```

**Explanation:**
- **Custom authentication:** Allows login with username, email, OR phone number
- **Q objects:** Django's query builder for OR conditions
- **check_password():** Verifies the password is correct
- Returns the user if credentials are valid, None otherwise

### URLs

**File:** `accounts/urls.py`

```python
urlpatterns = [
    path('register/', register_view, name='register'),
    path('gym-owner/register/', gym_owner_register_view, name='gym_owner_register'),
    path('profile/', profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
```

**URL Patterns:**
- `/accounts/register/` - Member registration
- `/accounts/gym-owner/register/` - Gym owner registration
- `/accounts/profile/` - User profile page
- `/accounts/login/` - Login page
- `/accounts/logout/` - Logout (redirects to home)

---

## Gyms App

**Purpose:** Manages gym information, listings, and owner dashboards.

### Models

**File:** `gyms/models.py`

```python
class Gym(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_phone = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gym_images/', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gyms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Field Explanations:**
- **name:** Gym name (e.g., "FitZone Kigali")
- **address:** Full address of the gym
- **contact_phone:** Gym's contact phone number
- **description:** Optional gym description
- **image:** Gym logo/photo (stored in `media/gym_images/`)
- **owner:** Foreign key to User model (the gym owner)
- **created_at:** Automatically set when gym is created
- **updated_at:** Automatically updated on every save

**Relationships:**
- One User (owner) can have many Gyms (`related_name='gyms'`)
- One Gym can have many Memberships (`related_name='members'` in Membership model)
- One Gym can have many Classes (`related_name='classes'` in GymClass model)

### Views

**File:** `gyms/views.py`

#### 1. `gym_list(request)`
```python
def gym_list(request):
    """View to list all gyms"""
    gyms = Gym.objects.all()
    return render(request, 'gyms/gym_list.html', {'gyms': gyms})
```
**Purpose:** Shows all registered gyms. Anyone can view this (no login required).

#### 2. `gym_detail(request, pk)`
```python
def gym_detail(request, pk):
    """View to show details of a specific gym"""
    gym = get_object_or_404(Gym, pk=pk)
    return render(request, 'gyms/gym_detail.html', {'gym': gym})
```
**Purpose:** Shows detailed information about a specific gym. `get_object_or_404` returns 404 error if gym doesn't exist.

#### 3. `gym_owner_dashboard(request)`
```python
@login_required
def gym_owner_dashboard(request):
    """Dashboard view for Gym Owners"""
    if request.user.role != 'GYM_OWNER':
        return redirect('home')
    
    # Get the owner's primary gym (assuming one for now, or use list)
    my_gyms = Gym.objects.filter(owner=request.user)
    
    # Total Members across all owned gyms
    total_members = Membership.objects.filter(gym__in=my_gyms, is_active=True).count()
    
    # Total Revenue (Completed payments)
    total_revenue = Payment.objects.filter(gym__in=my_gyms, status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Upcoming Classes
    upcoming_classes = GymClass.objects.filter(gym__in=my_gyms, start_time__gte=timezone.now()).order_by('start_time')[:5]
    
    context = {
        'gyms': my_gyms,
        'total_members': total_members,
        'total_revenue': total_revenue,
        'upcoming_classes': upcoming_classes,
        'title': 'Gym Owner Dashboard'
    }
    
    return render(request, 'gyms/dashboard.html', context)
```

**Explanation:**
- **@login_required:** Decorator ensures user is logged in
- **Role check:** Only GYM_OWNER can access
- **Queries:**
  - `my_gyms`: All gyms owned by the user
  - `total_members`: Count of active memberships
  - `total_revenue`: Sum of all completed payments
  - `upcoming_classes`: Next 5 classes across all gyms
- **aggregate(Sum()):** Django's way to sum values
- **[:5]:** Limits to 5 results

### URLs

**File:** `gyms/urls.py`

```python
urlpatterns = [
    path('', gym_list, name='gym_list'),
    path('dashboard/', gym_owner_dashboard, name='gym_owner_dashboard'),
    path('<int:pk>/', gym_detail, name='gym_detail'),
]
```

**URL Patterns:**
- `/gyms/` - List all gyms
- `/gyms/dashboard/` - Gym owner dashboard
- `/gyms/1/` - Details of gym with ID 1

---

## Members App

**Purpose:** Manages member-gym relationships and membership tiers.

### Models

**File:** `members/models.py`

```python
class Membership(models.Model):
    TIER_CHOICES = (
        ('BASIC', 'Basic'),
        ('PREMIUM', 'Premium'),
        ('CORPORATE', 'Corporate'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='members')
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='BASIC')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
```

**Field Explanations:**
- **user:** The member (User model)
- **gym:** The gym they're a member of
- **tier:** Membership level (Basic, Premium, Corporate)
- **joined_at:** When they joined (auto-set)
- **is_active:** Whether membership is currently active

**Relationships:**
- One User can have many Memberships (can join multiple gyms)
- One Gym can have many Memberships (many members)

**Example Usage:**
```python
# Get all memberships for a user
user.memberships.all()

# Get all members of a gym
gym.members.all()

# Check if membership is active
membership.is_active
```

---

## Classes App

**Purpose:** Manages fitness classes and scheduling.

### Models

**File:** `classes/models.py`

```python
class GymClass(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='classes')
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_classes')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=20)
    
    class Meta:
        verbose_name_plural = "Gym Classes"
```

**Field Explanations:**
- **name:** Class name (e.g., "Morning Yoga", "Cardio Blast")
- **description:** Class description
- **gym:** Which gym the class is at
- **trainer:** The trainer teaching (can be null if not assigned)
- **start_time & end_time:** When the class happens
- **capacity:** Maximum number of participants

**Relationships:**
- One Gym can have many Classes
- One Trainer can have many Classes (`on_delete=models.SET_NULL` means if trainer is deleted, class remains but trainer is set to null)

### Views

**File:** `classes/views.py`

```python
def class_list(request):
    """View to list all classes"""
    return render(request, 'classes/class_list.html')
```

**Note:** Currently just renders template. You'll need to add logic to fetch and display classes.

---

## Payments App

**Purpose:** Tracks payments for memberships and services.

### Models

**File:** `payments/models.py`

```python
class Payment(models.Model):
    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
```

**Field Explanations:**
- **user:** Who made the payment
- **gym:** Which gym the payment is for
- **amount:** Payment amount (DecimalField for currency precision)
- **transaction_id:** Unique ID from payment provider (Mobile Money, etc.)
- **status:** Payment status (Pending, Completed, Failed)
- **created_at:** When payment was initiated

**Example Usage:**
```python
# Get all payments for a gym
gym.payments.all()

# Get total revenue
Payment.objects.filter(status='COMPLETED').aggregate(Sum('amount'))
```

---

## Trainers App

**Purpose:** Manages trainer information and assignments.

**Current Status:** Models are not yet implemented. This is where you'll add:
- Trainer profiles
- Certifications
- Specialties
- Availability schedules
- Commission tracking

---

## Analytics App

**Purpose:** Provides reporting and analytics features.

**Current Status:** Not yet implemented. This is where you'll add:
- Revenue reports
- Member retention metrics
- Class popularity analytics
- Attendance tracking
- Equipment usage statistics

---

## Templates

**Location:** `templates/` directory

### Base Template

**File:** `templates/base.html`

**Purpose:** Base template that all other templates extend. Contains:
- HTML structure
- Navigation bar
- Footer
- Bootstrap CSS/JS
- Font Awesome icons
- Message display system

**Key Features:**
```django
{% if user.is_authenticated %}
    <!-- Show user menu -->
{% else %}
    <!-- Show login/register links -->
{% endif %}
```

**Role-based Navigation:**
```django
{% if user.role == 'GYM_OWNER' %}
    <li><a href="{% url 'gym_owner_dashboard' %}">Dashboard</a></li>
{% elif user.role == 'TRAINER' %}
    <li><a href="#">Trainer Panel</a></li>
{% endif %}
```

### Registration Template

**File:** `templates/accounts/register.html`

**Purpose:** Handles both member and gym owner registration.

**Key Features:**
- **Conditional Layout:** Different form layout for gym owners (`{% if is_gym_owner %}`)
- **Form Rendering:** Loops through form fields
- **Error Display:** Shows validation errors
- **File Upload:** `enctype="multipart/form-data"` for gym images

**Form Structure:**
```django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <!-- Form fields -->
    <button type="submit">Register</button>
</form>
```

### Login Template

**File:** `templates/accounts/login.html`

**Purpose:** User login page.

**Features:**
- Accepts username, email, or phone number (thanks to custom backend)
- Password field
- Error message display
- Link to registration

### Profile Template

**File:** `templates/accounts/profile.html`

**Purpose:** Shows user profile information.

**Role-based Content:**
- **Members:** Shows their gym memberships
- **Gym Owners:** Shows their gyms
- **All Users:** Shows basic profile info (name, email, phone, join date)

---

## URL Routing

### Main URLs

**File:** `gymhub/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('gyms/', include('gyms.urls')),
    path('members/', include('members.urls')),
    path('payments/', include('payments.urls')),
    path('classes/', include('classes.urls')),
    path('trainers/', include('trainers.urls')),
    path('analytics/', include('analytics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Explanation:**
- **include():** Includes URL patterns from each app
- **name='home':** Allows using `{% url 'home' %}` in templates
- **static():** Serves uploaded files during development

**Complete URL Structure:**
- `/` - Home page
- `/admin/` - Django admin panel
- `/accounts/register/` - Member registration
- `/accounts/gym-owner/register/` - Gym owner registration
- `/accounts/login/` - Login
- `/accounts/profile/` - User profile
- `/gyms/` - Gym list
- `/gyms/dashboard/` - Gym owner dashboard
- `/gyms/1/` - Gym details
- `/classes/` - Class list

---

## Authentication System

### How Authentication Works

1. **User Registration:**
   - User fills form → `CustomUserCreationForm` validates → User created → Auto-login

2. **User Login:**
   - User enters username/email/phone + password
   - `EmailOrPhoneBackend` checks all three fields
   - If match found and password correct → User logged in
   - Session created → User can access protected pages

3. **Role-based Access:**
   - `request.user.role` contains user's role
   - Views check role to show/hide features
   - Templates use `{% if user.role == 'GYM_OWNER' %}` for conditional content

### Protecting Views

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    # Only logged-in users can access
    pass
```

### Checking User Role

```python
if request.user.role == 'GYM_OWNER':
    # Gym owner specific code
elif request.user.role == 'MEMBER':
    # Member specific code
```

---

## Signup/Registration System

### Member Registration Flow

1. **User visits:** `/accounts/register/`
2. **Form displayed:** `CustomUserCreationForm` with fields:
   - Username
   - Email
   - Phone Number
   - Password
   - Password Confirmation
   - Role (defaults to MEMBER)
3. **User submits form:**
   - Form validates (passwords match, email format, etc.)
   - `form.save()` creates User
   - If `gym_id` in URL, creates Membership automatically
   - User is auto-logged in
   - Redirected to home page

### Gym Owner Registration Flow

1. **User visits:** `/accounts/gym-owner/register/`
2. **Form displayed:** `GymOwnerRegistrationForm` with:
   - **Account Section:** Username, Email, Phone, Password fields
   - **Gym Section:** Gym Name, Address, Phone, Image
3. **User submits:**
   - `form.save()` creates:
     - User account with role='GYM_OWNER'
     - Gym object linked to user
   - User is auto-logged in
   - Redirected to home page

### Making Signup Necessary

**Current Status:** Signup is already functional and necessary for:
- Creating member accounts
- Creating gym owner accounts
- Accessing profile pages
- Accessing gym owner dashboard

**To make it more mandatory:**

1. **Protect more views:**
```python
from django.contrib.auth.decorators import login_required

@login_required
def gym_list(request):
    # Now only logged-in users can see gyms
    gyms = Gym.objects.all()
    return render(request, 'gyms/gym_list.html', {'gyms': gyms})
```

2. **Redirect anonymous users:**
```python
def some_view(request):
    if not request.user.is_authenticated:
        return redirect('register')
    # Rest of view
```

3. **Add middleware (advanced):**
Create middleware to redirect all anonymous users to registration.

### Registration Form Fields Explained

**CustomUserCreationForm fields:**
- `username` - Required, unique identifier
- `password1` - Password (validated for strength)
- `password2` - Password confirmation
- `email` - Optional but recommended
- `phone_number` - Optional, Rwandan format (+250...)
- `role` - Defaults to 'MEMBER', can be changed
- `gym_id` - Hidden field, set if coming from gym page

**GymOwnerRegistrationForm additional fields:**
- `gym_name` - Name of the gym
- `gym_address` - Full address
- `gym_phone` - Gym contact number
- `gym_image` - Optional gym logo/photo

---

## Database Relationships

### Entity Relationship Diagram

```
User (accounts.User)
  ├── One-to-Many → Gym (gyms.Gym) [as owner]
  ├── One-to-Many → Membership (members.Membership) [as user]
  ├── One-to-Many → Payment (payments.Payment) [as user]
  └── One-to-Many → GymClass (classes.GymClass) [as trainer]

Gym (gyms.Gym)
  ├── Many-to-One → User [owner]
  ├── One-to-Many → Membership [members]
  ├── One-to-Many → Payment [payments]
  └── One-to-Many → GymClass [classes]

Membership (members.Membership)
  ├── Many-to-One → User [user]
  └── Many-to-One → Gym [gym]

Payment (payments.Payment)
  ├── Many-to-One → User [user]
  └── Many-to-One → Gym [gym]

GymClass (classes.GymClass)
  ├── Many-to-One → Gym [gym]
  └── Many-to-One → User [trainer]
```

### Accessing Related Objects

```python
# Get all gyms owned by a user
user.gyms.all()

# Get all memberships of a user
user.memberships.all()

# Get all members of a gym
gym.members.all()

# Get all classes at a gym
gym.classes.all()

# Get all classes taught by a trainer
trainer.assigned_classes.all()
```

---

## Common Django Patterns Used

### 1. Model Methods
```python
def __str__(self):
    return f"{self.username} ({self.get_role_display()})"
```
**Purpose:** Defines how the object appears in admin and when printed.

### 2. Form Customization
```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields:
        self.fields[field].widget.attrs.update({'class': 'form-control'})
```
**Purpose:** Adds CSS classes to all form fields automatically.

### 3. Query Filtering
```python
Gym.objects.filter(owner=request.user)
```
**Purpose:** Gets only gyms owned by the current user.

### 4. Aggregations
```python
Payment.objects.filter(status='COMPLETED').aggregate(Sum('amount'))
```
**Purpose:** Calculates sum of all completed payments.

### 5. Template Tags
```django
{% if user.is_authenticated %}
    <!-- Show for logged-in users -->
{% endif %}
```
**Purpose:** Conditional content based on authentication status.

---

## Next Steps for Development

### 1. Complete Missing Features
- [ ] Trainer models and views
- [ ] Analytics models and views
- [ ] Class booking system
- [ ] Payment processing integration
- [ ] QR code generation for members
- [ ] Attendance tracking

### 2. Enhance Existing Features
- [ ] Add profile photo upload
- [ ] Add gym operating hours
- [ ] Add class booking functionality
- [ ] Add payment history view
- [ ] Add member dashboard

### 3. Security Improvements
- [ ] Add email verification
- [ ] Add password reset functionality
- [ ] Add phone number verification
- [ ] Implement proper permissions system

### 4. UI/UX Improvements
- [ ] Add more responsive design
- [ ] Add loading states
- [ ] Add better error messages
- [ ] Add success notifications

---

## Important Notes

1. **Custom User Model:** Once migrations are run, you CANNOT change the User model easily. Make sure it's correct before running migrations.

2. **Media Files:** In production, you'll need to configure proper media file serving (not using Django's development server).

3. **Secret Key:** Change `SECRET_KEY` in settings.py before deploying to production.

4. **Database:** SQLite is fine for development, but use PostgreSQL or MySQL for production.

5. **Static Files:** Run `python manage.py collectstatic` before deploying to collect all static files.

---

## Quick Reference

### Creating a User
```python
from accounts.models import User
user = User.objects.create_user(
    username='john',
    email='john@example.com',
    password='password123',
    role='MEMBER',
    phone_number='+250788123456'
)
```

### Creating a Gym
```python
from gyms.models import Gym
gym = Gym.objects.create(
    name='FitZone',
    address='Kigali, Rwanda',
    contact_phone='+250788123456',
    owner=user
)
```

### Creating a Membership
```python
from members.models import Membership
membership = Membership.objects.create(
    user=user,
    gym=gym,
    tier='PREMIUM',
    is_active=True
)
```

### Querying Data
```python
# Get all active members
active_members = Membership.objects.filter(is_active=True)

# Get gym owner's revenue
revenue = Payment.objects.filter(
    gym__owner=user,
    status='COMPLETED'
).aggregate(Sum('amount'))
```

---

## Conclusion

This documentation covers all the code in your GymHub Django project. Each component is explained with its purpose, how it works, and how it relates to other parts of the system.

**Key Takeaways:**
- The project uses a custom User model with roles
- Registration is fully functional for both members and gym owners
- The authentication system supports username, email, or phone login
- Models are properly related through ForeignKeys
- Views handle both GET (display) and POST (process) requests
- Templates use Django template language for dynamic content

If you need clarification on any part, refer back to the specific section in this document.

---

**Last Updated:** December 2025
**Django Version:** 5.0
**Python Version:** 3.8+



