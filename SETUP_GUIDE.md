# GymHub Django - Setup & Run Guide

This guide contains all the commands you need to set up and run the GymHub Django project.

---

## Quick Setup Commands

### 1. Navigate to Project Directory
```bash
cd "E:\VisualStudio Projects\GymHub_Django"
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
# Create migrations (if needed)
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

### 5. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 6. Run the Development Server
```bash
python manage.py runserver
```

The server will start on: **http://127.0.0.1:8000/**

---

## Access Points

Once the server is running, you can access:

- **Home Page:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Member Registration:** http://127.0.0.1:8000/accounts/register/
- **Gym Owner Registration:** http://127.0.0.1:8000/accounts/gym-owner/register/
- **Login Page:** http://127.0.0.1:8000/accounts/login/
- **User Profile:** http://127.0.0.1:8000/accounts/profile/
- **Gym List:** http://127.0.0.1:8000/gyms/
- **Gym Owner Dashboard:** http://127.0.0.1:8000/gyms/dashboard/
- **Class List:** http://127.0.0.1:8000/classes/

---

## Common Commands

### Check Migration Status
```bash
python manage.py showmigrations
```

### Create New Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Server on Different Port
```bash
python manage.py runserver 8080
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

### Access Django Shell
```bash
python manage.py shell
```

### Check for Issues
```bash
python manage.py check
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:** Activate your virtual environment first
```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: "No such table" or Database Errors
**Solution:** Run migrations
```bash
python manage.py migrate
```

### Issue: PowerShell Script Execution Policy
If you get an error activating virtual environment in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Port Already in Use
If port 8000 is already in use:
```bash
python manage.py runserver 8080
```

---

## Development Workflow

1. **Start Development:**
   ```bash
   # Activate venv
   .\venv\Scripts\Activate.ps1
   
   # Run server
   python manage.py runserver
   ```

2. **Make Changes:**
   - Edit your code
   - Save files
   - Server auto-reloads (Django development server)

3. **Create New Models:**
   ```bash
   # After creating models in models.py
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Stop Server:**
   - Press `Ctrl + C` in terminal

---

## First Time Setup Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Server running (`python manage.py runserver`)
- [ ] Can access home page at http://127.0.0.1:8000/
- [ ] Can login to admin at http://127.0.0.1:8000/admin/

---

## Next Steps After Setup

1. **Login to Admin Panel:**
   - Go to http://127.0.0.1:8000/admin/
   - Use your superuser credentials

2. **Register a Gym Owner:**
   - Go to http://127.0.0.1:8000/accounts/gym-owner/register/
   - Fill in the form to create a gym

3. **Register a Member:**
   - Go to http://127.0.0.1:8000/accounts/register/
   - Create a member account

4. **Test Login:**
   - Go to http://127.0.0.1:8000/accounts/login/
   - Login with username, email, or phone number

---

**Note:** This is a development setup. For production deployment, additional configuration is required (see CODE_DOCUMENTATION.md for details).



