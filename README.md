# GymHub Rwanda - Django Gym Management System

### A comprehensive gym management system tailored for Rwanda's fitness industry.


## 1. Project Features Definition

### Core Features for MVP (Minimum Viable Product)

## A. Authentication & User Management
### Multi-role authentication (Owner, Staff, Member, Trainer)
   ==================================================================

- Phone number-based registration (Rwandan format: +2507xxxxxxx)

- Email and password authentication

- Role-based access control
 
- Profile management with photo upload

## B. Gym Management
### Create and manage multiple gym locations
==================================================

- Set gym operating hours

- Manage gym facilities and amenities
 
- Track equipment inventory and maintenance
 
- Branch management for chain gyms

## C. Member Management
### Digital member registration with required info (name, phone, emergency contact)
   ====================================================================================

- Membership tier system (Basic, Premium, Corporate)
 
- Family/group membership packages
 
- Membership status tracking (active, expired, suspended)
 
- Digital membership card with QR code

## D. Payment System
### Cash payment tracking
   ==============================

- Mobile Money payment integration (MTN & Airtel)
 
- Automated billing and payment reminders
 
- Payment history and receipt generation
 
- Membership renewal notifications via SMS

## E. Class & Scheduling
### Create fitness classes (yoga, aerobics, weight training, traditional dance)
   ===============================================================================

- Set class schedules with capacity limits
 
- Online class booking system
 
- Waitlist management
 
- Cancellation and rescheduling
 
- Special holiday schedules (Rwandan public holidays)

## F. Attendance System
### QR code check-in/check-out
   ===================================

- Session tracking and usage analytics
 
- Guest pass management
 
- Peak hour monitoring

## G. Trainer Management
Trainer profiles with certifications and specialties
==========================================================

- Trainer availability scheduling
 
- Client assignment and progress tracking
 
- Commission tracking for freelance trainers

## H. Rwandan-Specific Features
  ### Multi-language support (English, Kinyarwanda, French)
   =============================================================

- Public holiday auto-detection and schedule adjustment
 
- Integration with local payment methods
 
- Cultural workout categories (Traditional dance, etc.)

## I. Reporting & Analytics
### Member attendance reports
   =============================

- Revenue tracking and financial reports
 
- Class popularity analytics
 
- Member retention rates
 
- Equipment usage statistics


## Target User Groups
GymHub Rwanda – User Step-by-Step System Flow
1️⃣ Gym Owner

Role Summary: Manages gym branches, finances, staff, and overall operations.

Step-by-Step Actions:

Login / Authentication

Log in with phone/email and password.

Dashboard Access

View overview: total members, revenue, upcoming classes.

Manage Gym Branches

Add a new branch.

Update branch info (address, operating hours).

Remove a branch if needed.

Manage Facilities & Equipment

Add/update gym facilities and amenities.

Track equipment inventory and schedule maintenance.

Staff Management

Add new staff accounts.

Edit staff info or deactivate accounts.

Membership Tracking

Monitor member statistics (active, expired, suspended).

View membership tier distribution (Basic, Premium, Corporate).

Financial Reporting

Access revenue and payment reports.

Analyze trends for branches.

Attendance & Retention Analytics

View member check-in trends.

Track class popularity and retention metrics.

2️⃣ Gym Staff

Role Summary: Handles day-to-day gym operations, assists members, and processes payments.

Step-by-Step Actions:

Login

Phone/email + password.

Dashboard

Overview of members scheduled today, class bookings.

Member Check-in / Check-out

Scan member QR code or manual check-in.

Payment Processing

Record cash payments.

Optionally integrate mobile money payments.

Class Booking Management

Approve or cancel bookings.

Reschedule classes if necessary.

Track Attendance

Monitor member attendance for classes and gym sessions.

Monitor Gym Usage

Track peak hours and occupancy.

Assist Members

Answer inquiries, provide support for booking, membership, or facility use.

3️⃣ Member

Role Summary: Uses gym facilities, books classes, manages profile and payments.

Step-by-Step Actions:

Registration

Register with phone (+2507xxxxxxx), email, and emergency contact.

Login

Access account with phone/email and password.

Profile Management

Upload profile photo.

Update personal information.

View Gym & Class Schedule

Browse available gyms and classes.

Check class capacity and schedule.

Class Booking

Book desired fitness classes.

Join waitlist if full.

Attend Classes / Gym Sessions

Scan QR code for check-in/check-out.

Track attendance automatically.

Track Personal Progress

View class history, attendance, and performance.

Payments

Make payments for membership or classes.

Receive digital receipt.

Membership Renewal

Receive notifications for renewal.

4️⃣ Trainer

Role Summary: Manages schedule, clients, and performance tracking.

Step-by-Step Actions:

Login

Phone/email + password.

Profile Setup

Add certifications, specialties, and bio.

Schedule Management

Set availability for personal and class sessions.

Update schedule for public holidays.

Client Management

View assigned clients.

Track client progress.

Class Assignment

Manage classes they are assigned to teach.

Approve or reject class bookings if needed.

Commission Tracking

View earnings from freelance sessions.

Analytics

Monitor client engagement and session popularity.

5️⃣ Admin

Role Summary: Oversees system configuration, analytics, and security.

Step-by-Step Actions:

Login

Admin credentials.

System Configuration

Configure multi-language support (English, Kinyarwanda, French).

Configure public holiday schedules.

Set system-wide settings.

User Management

Add/edit/remove all users (Owner, Staff, Trainer, Member).

Assign roles and permissions.

Analytics Dashboard

Access reports on revenue, attendance, member retention.

Track system usage trends.

Monitor System Performance

Ensure uptime and correct data tracking.

Security & Access Control

Manage passwords, reset accounts, control access levels.

6️⃣ Optional: Guest / Visitor

Role Summary: Non-members exploring the gym.

Step-by-Step Actions:

Browse Gym Information

View available gym branches.

Check class schedules and amenities.

Limited Booking

Book a guest pass if available.

Learn Membership Options

See membership tiers (Basic, Premium, Corporate) and benefits.

Optional Registration

Register as a member to unlock full features.



## MVP Scope (Phase 1)
- Basic authentication with phone/email
 
- Member registration and profile management
 
- Gym and class management
 
- Booking system with capacity limits
 
- Payment tracking (cash only initially)
 
- Attendance system with QR codes
 
- Basic reporting dashboard



## 2. ERD Design

![GymHub ERD](ERD/GymHub%20ERD.png)
