const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ MongoDB connected successfully');
  } catch (error) {
    console.error('❌ MongoDB connection failed:', error.message);
    console.error('   Check that MONGODB_URI in your .env file is correct and MongoDB is running.');
    process.exit(1);
  }
};

module.exports = connectDB;
