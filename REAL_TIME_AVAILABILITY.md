# Real-Time Slot Availability System

## Overview

This system provides real-time slot availability tracking for the JCU Gym Management System with a maximum of 6 people per session. Users can see live availability, book slots, and get instant feedback on capacity.

## Features

### 🎯 Real-Time Availability
- **Live Updates**: See current booking status for each time slot
- **Capacity Tracking**: Maximum 6 people per 1-hour session
- **Visual Indicators**: Color-coded slots (Available, Limited, Full)
- **Progress Bars**: Visual representation of slot capacity
- **Percentage Display**: Shows how full each slot is

### 📊 Slot Status Types
- **🟢 Available**: 4-6 spots available
- **🟡 Limited**: 1-3 spots available  
- **🔴 Full**: 0 spots available (6/6 booked)

### 🔄 Real-Time Features
- **Auto-refresh**: Availability updates when date/user type changes
- **Manual refresh**: Refresh button to get latest data
- **Last updated timestamp**: Shows when data was last fetched
- **Instant booking**: Real-time booking with immediate feedback

## API Endpoints

### Get Slot Availability
```
GET /api/sessions/availability?date=YYYY-MM-DD&user_type=student|staff
```

**Response:**
```json
{
  "date": "2024-12-01",
  "user_type": "student",
  "slots": [
    {
      "time_slot": "09:00 - 10:00",
      "start_time": "09:00",
      "end_time": "10:00",
      "booked_count": 3,
      "available_spots": 3,
      "is_full": false,
      "percentage_full": 50.0
    }
  ],
  "total_slots": 14
}
```

### Book a Slot
```
POST /api/sessions/book
```

**Request Body:**
```json
{
  "date": "2024-12-01",
  "time_slot": "09:00 - 10:00",
  "member_id": "M001"
}
```

**Response:**
```json
{
  "message": "Booking successful",
  "booking_ref": "BK20241201123456",
  "date": "2024-12-01",
  "time_slot": "09:00 - 10:00"
}
```

## Database Schema

### Booking Table
```sql
CREATE TABLE booking (
    BOOKING_Ref VARCHAR(20) PRIMARY KEY,
    MEMBER_ID VARCHAR(10),
    SESSION_ID INT,
    BOOKING_Date DATE,
    BOOKING_Time TIME,
    BOOKING_Status VARCHAR(20)
);
```

## Setup Instructions

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python demo_slots.py  # Create sample data
python run.py  # Start the server
```

### 2. Frontend Setup
```bash
cd app/frontend
npm install
npm start
```

### 3. Test the System
1. Navigate to the Session Booking page
2. Select a date (today, tomorrow, or day after)
3. Choose user type (Student or Staff)
4. View real-time availability
5. Book available slots
6. See immediate updates

## Demo Data

The system includes demo data for testing:

- **Today**: Various booking levels (full, partial, empty slots)
- **Tomorrow**: Mixed availability
- **Day After**: Mostly empty slots

### Sample Scenarios
- **09:00 slot**: Full (6/6 booked) - Red indicator
- **10:00 slot**: Limited (3/6 booked) - Yellow indicator  
- **11:00 slot**: Available (5/6 booked) - Green indicator
- **Other slots**: Mostly available

## User Interface Features

### Visual Indicators
- **Capacity Bars**: Show percentage of slot filled
- **Color Coding**: Green (available), Yellow (limited), Red (full)
- **Status Text**: "X spots available", "X spots left", "Full"
- **Live Indicator**: Pulsing green dot showing real-time status

### Interactive Elements
- **Refresh Button**: Manual update of availability
- **Last Updated**: Timestamp of last data fetch
- **Loading States**: Spinner during data fetching
- **Error Handling**: Clear error messages for failed requests

### Booking Flow
1. Select user type (Student/Staff)
2. Choose date (minimum today)
3. View real-time availability
4. Select up to 2 slots per day
5. Confirm booking
6. Receive booking confirmation with references

## Business Rules

### Capacity Limits
- **Maximum 6 people per 1-hour session**
- **Maximum 2 slots per person per day**
- **Real-time validation** prevents overbooking

### Time Slots
- **Students**: 08:00-22:00 (Mon-Fri), 08:00-18:00 (Sat)
- **Staff**: 06:00-08:00, 12:00-14:00, 18:00-20:00 (Mon-Fri), 07:00-13:00 (Sat)

### Booking Rules
- **Advance booking required**
- **No same-day cancellations**
- **Maximum 2 slots per day per person**
- **Real-time availability check**

## Error Handling

### Common Errors
- **Slot Full**: "This slot is already full"
- **Daily Limit**: "You can only book up to 2 slots per day"
- **Network Error**: "Failed to load slot availability"
- **Booking Failed**: "Booking failed. Please try again"

### Error States
- **Loading**: Spinner with "Loading real-time availability..."
- **Error**: Red error box with specific message
- **No Slots**: "No available slots on this day"
- **Select Date**: "Please select a date to view available slots"

## Technical Implementation

### Backend (Python/Flask)
- **Real-time queries** to database
- **Capacity calculation** on each request
- **Booking validation** with race condition protection
- **Error handling** with proper HTTP status codes

### Frontend (React)
- **State management** for availability data
- **Real-time updates** via API calls
- **Visual feedback** with loading/error states
- **Responsive design** for mobile/desktop

### Database (MySQL)
- **Efficient queries** for availability calculation
- **Indexed fields** for fast lookups
- **Transaction support** for booking integrity

## Testing

### Manual Testing
1. **Create demo data**: `python demo_slots.py`
2. **Test booking flow**: Book slots and verify updates
3. **Test edge cases**: Try to book full slots, exceed daily limit
4. **Test refresh**: Use refresh button to update data

### API Testing
```bash
# Test availability endpoint
curl "http://localhost:5000/api/sessions/availability?date=2024-12-01&user_type=student"

# Test booking endpoint
curl -X POST "http://localhost:5000/api/sessions/book" \
  -H "Content-Type: application/json" \
  -d '{"date":"2024-12-01","time_slot":"09:00 - 10:00","member_id":"M001"}'
```

## Future Enhancements

### Planned Features
- **WebSocket support** for real-time updates
- **Email notifications** for booking confirmations
- **Calendar integration** for external bookings
- **Analytics dashboard** for booking trends
- **Mobile app** with push notifications

### Performance Optimizations
- **Caching** for frequently accessed data
- **Database indexing** for faster queries
- **CDN integration** for static assets
- **Load balancing** for high traffic

## Troubleshooting

### Common Issues
1. **Backend not running**: Check `python run.py` in backend directory
2. **Database connection**: Verify MySQL is running and config is correct
3. **CORS errors**: Ensure Flask-CORS is properly configured
4. **No data showing**: Run `python demo_slots.py` to create sample data

### Debug Mode
```bash
# Backend debug
export FLASK_ENV=development
python run.py

# Frontend debug
npm start
```

## Support

For technical support or feature requests, please contact the development team or create an issue in the project repository. 