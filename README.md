# GymHub Rwanda - Django Gym Management System

# A comprehensive gym management system tailored for Rwanda's fitness industry.


# 1. Project Features Definition

# Core Features for MVP (Minimum Viable Product)

# A. Authentication & User Management
Multi-role authentication (Owner, Staff, Member, Trainer)
==========================================================

- Phone number-based registration (Rwandan format: +2507xxxxxxx)

- Email and password authentication

- Role-based access control
 
- Profile management with photo upload

# B. Gym Management
Create and manage multiple gym locations
========================================

- Set gym operating hours

- Manage gym facilities and amenities
 
- Track equipment inventory and maintenance
 
- Branch management for chain gyms

# C. Member Management
Digital member registration with required info (name, phone, emergency contact)
===============================================================================

- Membership tier system (Basic, Premium, Corporate)
 
- Family/group membership packages
 
- Membership status tracking (active, expired, suspended)
 
- Digital membership card with QR code

# D. Payment System
Cash payment tracking
=====================

- Mobile Money payment integration (MTN & Airtel)
 
- Automated billing and payment reminders
 
- Payment history and receipt generation
 
- Membership renewal notifications via SMS

# E. Class & Scheduling
Create fitness classes (yoga, aerobics, weight training, traditional dance)
============================================================================

- Set class schedules with capacity limits
 
- Online class booking system
 
- Waitlist management
 
- Cancellation and rescheduling
 
- Special holiday schedules (Rwandan public holidays)

# F. Attendance System
QR code check-in/check-out
==========================

- Session tracking and usage analytics
 
- Guest pass management
 
- Peak hour monitoring

# G. Trainer Management
Trainer profiles with certifications and specialties
=====================================================

- Trainer availability scheduling
 
- Client assignment and progress tracking
 
- Commission tracking for freelance trainers

# H. Rwandan-Specific Features
Multi-language support (English, Kinyarwanda, French)
======================================================

- Public holiday auto-detection and schedule adjustment
 
- Integration with local payment methods
 
- Cultural workout categories (Traditional dance, etc.)

# I. Reporting & Analytics
Member attendance reports
==========================

- Revenue tracking and financial reports
 
- Class popularity analytics
 
- Member retention rates
 
- Equipment usage statistics


# Target User Groups
Role	    Primary Features
----        ----------------
Gym Owner:	Manage multiple branches, view financial reports, staff management
Gym Staff:	Check-in members, process payments, manage bookings
Member:	    Book classes, view schedule, track progress, make payments
Trainer:	    Manage schedule, view clients, track commissions
Admin:	    System configuration, user management, analytics



# MVP Scope (Phase 1)
- Basic authentication with phone/email
 
- Member registration and profile management
 
- Gym and class management
 
- Booking system with capacity limits
 
- Payment tracking (cash only initially)
 
- Attendance system with QR codes
 
- Basic reporting dashboard



# 2. ERD Design

![GymHub ERD](ERD/GymHub%20ERD.png)
