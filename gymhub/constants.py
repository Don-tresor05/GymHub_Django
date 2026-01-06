# GymHub Constants and Enums for better maintainability

# User Roles
class UserRoles:
    MEMBER = 'MEMBER'
    TRAINER = 'TRAINER'
    GYM_OWNER = 'GYM_OWNER'
    STAFF = 'STAFF'
    ADMIN = 'ADMIN'
    
    CHOICES = (
        (MEMBER, 'Member'),
        (TRAINER, 'Trainer'),
        (GYM_OWNER, 'Gym Owner'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin'),
    )

# Membership Tiers
class MembershipTiers:
    BASIC = 'BASIC'
    PREMIUM = 'PREMIUM'
    CORPORATE = 'CORPORATE'
    
    CHOICES = (
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (CORPORATE, 'Corporate'),
    )

# Payment Status
class PaymentStatus:
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    REFUNDED = 'REFUNDED'
    
    CHOICES = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
        (REFUNDED, 'Refunded'),
    )

# Payment Methods
class PaymentMethods:
    CASH = 'CASH'
    MTN_MOMO = 'MTN_MOMO'
    AIRTEL_MONEY = 'AIRTEL_MONEY'
    BANK_TRANSFER = 'BANK_TRANSFER'
    CARD = 'CARD'
    
    CHOICES = (
        (CASH, 'Cash'),
        (MTN_MOMO, 'MTN Mobile Money'),
        (AIRTEL_MONEY, 'Airtel Money'),
        (BANK_TRANSFER, 'Bank Transfer'),
        (CARD, 'Credit/Debit Card'),
    )

# Equipment Status
class EquipmentStatus:
    WORKING = 'WORKING'
    MAINTENANCE = 'MAINTENANCE'
    BROKEN = 'BROKEN'
    RETIRED = 'RETIRED'
    
    CHOICES = (
        (WORKING, 'Working'),
        (MAINTENANCE, 'Under Maintenance'),
        (BROKEN, 'Broken'),
        (RETIRED, 'Retired'),
    )

# Class Types
class ClassTypes:
    YOGA = 'YOGA'
    AEROBICS = 'AEROBICS'
    WEIGHT_TRAINING = 'WEIGHT_TRAINING'
    CARDIO = 'CARDIO'
    DANCE = 'DANCE'
    MARTIAL_ARTS = 'MARTIAL_ARTS'
    SWIMMING = 'SWIMMING'
    CROSSFIT = 'CROSSFIT'
    
    CHOICES = (
        (YOGA, 'Yoga'),
        (AEROBICS, 'Aerobics'),
        (WEIGHT_TRAINING, 'Weight Training'),
        (CARDIO, 'Cardio'),
        (DANCE, 'Dance'),
        (MARTIAL_ARTS, 'Martial Arts'),
        (SWIMMING, 'Swimming'),
        (CROSSFIT, 'CrossFit'),
    )

# Facility Types
class FacilityTypes:
    CARDIO_AREA = 'CARDIO_AREA'
    WEIGHT_ROOM = 'WEIGHT_ROOM'
    POOL = 'POOL'
    SAUNA = 'SAUNA'
    LOCKER_ROOM = 'LOCKER_ROOM'
    PARKING = 'PARKING'
    CAFE = 'CAFE'
    MASSAGE = 'MASSAGE'
    
    CHOICES = (
        (CARDIO_AREA, 'Cardio Area'),
        (WEIGHT_ROOM, 'Weight Room'),
        (POOL, 'Swimming Pool'),
        (SAUNA, 'Sauna'),
        (LOCKER_ROOM, 'Locker Room'),
        (PARKING, 'Parking'),
        (CAFE, 'Cafe'),
        (MASSAGE, 'Massage Room'),
    )

# Booking Status
class BookingStatus:
    CONFIRMED = 'CONFIRMED'
    WAITLISTED = 'WAITLISTED'
    CANCELLED = 'CANCELLED'
    COMPLETED = 'COMPLETED'
    NO_SHOW = 'NO_SHOW'
    
    CHOICES = (
        (CONFIRMED, 'Confirmed'),
        (WAITLISTED, 'Waitlisted'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
        (NO_SHOW, 'No Show'),
    )

# Rwanda Phone Number Pattern
RWANDA_PHONE_PATTERN = r'^\+?250[0-9]{9}$'

# Default Values
DEFAULT_CLASS_CAPACITY = 20
DEFAULT_MEMBERSHIP_DURATION_DAYS = 30