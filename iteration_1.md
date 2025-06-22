# Actual iteration-1 board, (see chapters 3 and 4), add your start and end dates 

Checklist:
1. github entry timestamps
2. User stories are correct: see p39

* Assumed Velocity: 0.7
* Number of developers: 4
* Total estimated amount of work: 18 (initial: 11) days

User stories or tasks (see chapter 4):
# Todo
1. Secure Storage, priority Low, 3 (initial: 3) days  
   - Create database schema with sample records, 1 day
   - Integrate database with Flask using Flask-SQLAlchemy, 2 day
2. Secure Online Registration, priority High, 6 (initial: 2) days  
   - Analyse form considerations (user roles, validation, compliance), 1 day
   - Backend registration logic (hashing, storage, CSRF protection), 2 days 
   - Backend registration logic (email), 1 day
   - Frontend form validation + accessibility, 1 day 
   - Testing (unit + functional for registration flow), 1 day 
3. Membership Payment Handling, priority Low, 4 (initial: 3) days
   - Backend online payment integration (mock transaction logic, success/failure states, storage), 1 day
   - Backend offline payment integration (storage), 0.5 day
   - Frontend form modification for online and offline payment (Includes alert to pay at counter for offline payment), 0.5 day
   - Backend membership activation logic (storage, status), 0.5 day
   - Frontend membership confirmation (status), 0.5 day
   - Testing (unit + functional for membership handling flow), 1 day
4. Session Booking, priority High, 5 (initial: 3) days
   - Backend booking logic (slot availability, booking action + status, storage), 1 day
   - Frontend display (calendar, slot availability, booking action + status), 1 day
   - Backend booking logic (confirmation email (DRY), reminder emails), 1 day
   - Integrated user authentication for session booking,1 day
   - Testing (unit + functional for booking flow), 1 day

# In progress:
* 

# Complete:
* Analyse form considerations (user roles, validation, compliance) (MTN), 22 June 2025

# Completed:
* Secure Storage
   - Create database schema with sample records (TQRN), 20 June 2025
   - Integrate database with Flask using Flask-SQLAlchemy (HX, YJ), 21 June 2025

### Burn Down for iteration-1 (see chapter 4):
Update this at least once per week
* 4 weeks left, 18 days of estimated amount of work 
* 2 weeks left, xx days
* 1 weeks left, xx days
* 0 weeks left, xx days
* Actual Velocity: ??
