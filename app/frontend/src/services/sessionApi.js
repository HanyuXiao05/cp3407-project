// app/frontend/src/services/sessionApi.js

const API_BASE_URL = 'http://localhost:5000/api';

export const sessionApi = {
  // Get real-time slot availability for a specific date
  getSlotAvailability: async (date, userType) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/sessions/availability?date=${date}&user_type=${userType}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching slot availability:', error);
      throw error;
    }
  },

  // Book a time slot
  bookSlot: async (bookingData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions/book`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookingData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Booking failed');
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error booking slot:', error);
      throw error;
    }
  },

  // Get user's existing bookings for a date
  getUserBookings: async (date, memberId) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/booking?date=${date}&member_id=${memberId}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching user bookings:', error);
      throw error;
    }
  },
}; 