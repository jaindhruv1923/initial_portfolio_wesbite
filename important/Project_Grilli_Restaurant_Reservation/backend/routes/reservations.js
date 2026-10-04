const express = require('express');
const router = express.Router();
const Reservation = require('../models/Reservation');

// POST /api/reservations - create a new table reservation
router.post('/', async (req, res) => {
  try {
    const { name, phone, guests, date, time, message } = req.body;

    if (!name || !phone || !date || !time) {
      return res.status(400).json({
        message: 'Name, phone, date and time are required.',
      });
    }

    const reservation = await Reservation.create({
      name,
      phone,
      guests,
      date,
      time,
      message,
    });

    res.status(201).json({
      message: 'Reservation created successfully',
      reservation,
    });
  } catch (error) {
    console.error('Error creating reservation:', error.message);
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});

// GET /api/reservations - list all reservations (for admin/owner use)
router.get('/', async (req, res) => {
  try {
    const reservations = await Reservation.find().sort({ createdAt: -1 });
    res.json(reservations);
  } catch (error) {
    console.error('Error fetching reservations:', error.message);
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});

// GET /api/reservations/:id - get a single reservation
router.get('/:id', async (req, res) => {
  try {
    const reservation = await Reservation.findById(req.params.id);
    if (!reservation) {
      return res.status(404).json({ message: 'Reservation not found.' });
    }
    res.json(reservation);
  } catch (error) {
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});

// PATCH /api/reservations/:id - update reservation status (confirm/cancel)
router.patch('/:id', async (req, res) => {
  try {
    const { status } = req.body;
    const reservation = await Reservation.findByIdAndUpdate(
      req.params.id,
      { status },
      { new: true, runValidators: true }
    );
    if (!reservation) {
      return res.status(404).json({ message: 'Reservation not found.' });
    }
    res.json({ message: 'Reservation updated', reservation });
  } catch (error) {
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});

// DELETE /api/reservations/:id - delete a reservation
router.delete('/:id', async (req, res) => {
  try {
    const reservation = await Reservation.findByIdAndDelete(req.params.id);
    if (!reservation) {
      return res.status(404).json({ message: 'Reservation not found.' });
    }
    res.json({ message: 'Reservation deleted' });
  } catch (error) {
    res.status(500).json({ message: 'Server error. Please try again later.' });
  }
});

module.exports = router;
