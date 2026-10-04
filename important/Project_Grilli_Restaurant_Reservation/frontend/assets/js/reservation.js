'use strict';

/**
 * RESERVATION FORM
 *
 * Sends the "Book A Table" form data to the backend API,
 * which saves it to MongoDB, and shows a success/error message
 * to the user without reloading the page.
 */

const reservationForm = document.getElementById('reservation-form');
const reservationMsg = document.getElementById('reservation-msg');

const API_URL = window.location.origin + '/api/reservations';

if (reservationForm) {
  reservationForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(reservationForm);

    const payload = {
      name: formData.get('name'),
      phone: formData.get('phone'),
      guests: formData.get('person'),
      date: formData.get('reservation-date'),
      time: formData.get('time'),
      message: formData.get('message'),
    };

    if (!payload.name || !payload.phone || !payload.date || !payload.time) {
      reservationMsg.textContent = 'Please fill your name, phone, date and time.';
      reservationMsg.style.color = '#f44336';
      return;
    }

    reservationMsg.textContent = 'Booking your table...';
    reservationMsg.style.color = '#e0c08d';

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (response.ok) {
        reservationMsg.textContent = 'Table booked successfully! We will contact you shortly.';
        reservationMsg.style.color = '#4caf50';
        reservationForm.reset();
      } else {
        reservationMsg.textContent = result.message || 'Something went wrong. Please try again.';
        reservationMsg.style.color = '#f44336';
      }
    } catch (error) {
      reservationMsg.textContent = 'Could not connect to server. Please make sure the backend is running.';
      reservationMsg.style.color = '#f44336';
    }
  });
}
