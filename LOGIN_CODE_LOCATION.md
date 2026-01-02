# Login Code Location Guide

This document shows you exactly where all the login-related code is located in the GymHub project.

---

## Login Code Locations

### 1. Login View (URL Configuration)
**File:** `accounts/urls.py`
**Lines:** 9

```python
path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
```

**Explanation:** This is the URL route that handles login. It uses Django's built-in `LoginView` class-based view.

**URL:** `/accounts/login/`

---

### 2. Login Template (HTML Form)
**File:** `templates/accounts/login.html`
**Lines:** 1-76

**Key Parts:**
- **Form:** Lines 13-38
- **Username Field:** Lines 15-20 (accepts username, email, or phone)
- **Password Field:** Lines 21-25
- **Submit Button:** Lines 27-31
- **Error Display:** Lines 33-37

**Important:** The form field is named `username` but accepts username, email, OR phone number thanks to the custom authentication backend.

---

### 3. Authentication Backend (Login Logic)
**File:** `accounts/backends.py`
**Lines:** 1-20

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
- This is the **core login logic**
- It checks if the input matches username, email, OR phone number
- Uses Django's `Q` objects for OR queries
- Verifies password with `check_password()`
- Returns the user if credentials are valid, None otherwise

---

### 4. Authentication Backend Configuration
**File:** `gymhub/settings.py`
**Lines:** 113-116

```python
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrPhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

**Explanation:** Tells Django to use our custom authentication backend. The order matters - it tries our custom backend first, then falls back to Django's default.

---

### 5. Login Redirect Settings
**File:** `gymhub/settings.py`
**Lines:** 118-120

```python
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

**Explanation:** 
- After successful login, redirects to home page
- After logout, also redirects to home page

---

### 6. Logout View
**File:** `accounts/urls.py`
**Line:** 10

```python
path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
```

**Explanation:** Handles user logout. Uses Django's built-in `LogoutView`.

**URL:** `/accounts/logout/`

---

## How Login Works (Step by Step)

1. **User visits:** `/accounts/login/`
   - URL is defined in `accounts/urls.py` line 9

2. **Login form displayed:**
   - Template: `templates/accounts/login.html`
   - Form has `username` and `password` fields

3. **User submits form:**
   - Form POSTs to `/accounts/login/`
   - Django's `LoginView` processes the request

4. **Authentication happens:**
   - Django calls `EmailOrPhoneBackend.authenticate()`
   - Backend checks username, email, OR phone number
   - Backend verifies password
   - Returns user object if valid

5. **Session created:**
   - Django creates a session for the user
   - User is logged in

6. **Redirect:**
   - User is redirected to home page (configured in `settings.py`)

---

## Login Form Fields

**In:** `templates/accounts/login.html`

```html
<!-- Username field (accepts username, email, or phone) -->
<input type="text" name="username" class="form-control" id="id_username"
    placeholder="Enter your credentials" required>

<!-- Password field -->
<input type="password" name="password" class="form-control" id="id_password"
    placeholder="••••••••" required>
```

**Important Notes:**
- Field name is `username` but accepts username, email, OR phone
- Both fields are `required`
- Form uses `method="post"` and includes `{% csrf_token %}`

---

## Testing Login

### Test with Username:
```
Username: john
Password: yourpassword
```

### Test with Email:
```
Username: john@example.com
Password: yourpassword
```

### Test with Phone:
```
Username: +250788123456
Password: yourpassword
```

All three should work thanks to `EmailOrPhoneBackend`!

---

## Related Files

### Files That Handle Login:
1. ✅ `accounts/urls.py` - Login URL route
2. ✅ `accounts/backends.py` - Login authentication logic
3. ✅ `templates/accounts/login.html` - Login form template
4. ✅ `gymhub/settings.py` - Backend configuration

### Files That Use Login:
1. `templates/base.html` - Shows login/logout links in navigation
2. `accounts/views.py` - Some views check `request.user.is_authenticated`
3. `gyms/views.py` - `gym_owner_dashboard` uses `@login_required`

---

## Quick Reference

**Login URL:** `/accounts/login/`  
**Login View:** `auth_views.LoginView` (Django built-in)  
**Authentication:** `accounts.backends.EmailOrPhoneBackend`  
**Template:** `templates/accounts/login.html`  
**Redirect After Login:** Home page (`/`)  
**Redirect After Logout:** Home page (`/`)

---

## Summary

**Main Login Code Files:**
- 🔐 **Authentication Logic:** `accounts/backends.py`
- 🌐 **URL Route:** `accounts/urls.py` (line 9)
- 🎨 **Login Form:** `templates/accounts/login.html`
- ⚙️ **Configuration:** `gymhub/settings.py` (lines 113-120)

The login system allows users to login with **username, email, OR phone number** - all handled by the custom `EmailOrPhoneBackend` class.



