import mongoose from 'mongoose';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config({ path: './server/.env' });

// Inline User schema (copy from your main User.js)
const userSchema = new mongoose.Schema({
  supabaseId: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  fullName: { type: String, required: true },
  avatar: String,
  bio: String,
  isAdmin: { type: Boolean, default: false },
  purchasedBooks: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Book' }],
  courseProgress: {
    type: Map,
    of: {
      status: {
        type: String,
        enum: ['not_started', 'in_progress', 'completed'],
        default: 'not_started',
      },
      progress: { type: Number, default: 0, min: 0, max: 100 },
      startedAt: Date,
      completedAt: Date,
    },
  },
  badges: [{
    name: String,
    icon: String,
    earnedAt: Date,
    type: { type: String, enum: ['course_completion', 'book_purchase', 'achievement'] },
  }],
  reviews: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Review' }],
}, { timestamps: true });

const User = mongoose.model('User', userSchema);

async function makeUserAdmin() {
  try {
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/writer-instructor');
    console.log('✅ Connected to MongoDB');

    const emailOrId = process.argv[2];
    if (!emailOrId) {
      console.log('Usage: node make-admin.js <email or supabaseId>');
      console.log('Example: node make-admin.js user@example.com');
      console.log('Example: node make-admin.js e2eda1c0-97fc-4f0e-a99a-ceebda5c3d79');
      const allUsers = await User.find().select('email fullName isAdmin supabaseId');
      console.log('\nExisting users:');
      allUsers.forEach(u => {
        console.log(`- ${u.email} (${u.fullName}) [${u.supabaseId}] ${u.isAdmin ? '[ADMIN]' : ''}`);
      });
      process.exit(1);
    }

    let user = await User.findOne({ email: emailOrId });
    if (!user) {
      user = await User.findOne({ supabaseId: emailOrId });
    }

    if (!user) {
      console.log(`❌ User "${emailOrId}" not found`);
      const allUsers = await User.find().select('email fullName isAdmin supabaseId');
      console.log('\nExisting users:');
      allUsers.forEach(u => {
        console.log(`- ${u.email} (${u.fullName}) [${u.supabaseId}] ${u.isAdmin ? '[ADMIN]' : ''}`);
      });
      process.exit(1);
    }

    user.isAdmin = true;
    await user.save();

    console.log(`✅ User "${user.fullName}" (${user.email}) is now an admin!`);
    console.log('\nUser details:', {
      id: user._id,
      supabaseId: user.supabaseId,
      email: user.email,
      fullName: user.fullName,
      isAdmin: user.isAdmin
    });

    process.exit(0);
  } catch (error) {
    console.error('❌ Error:', error);
    process.exit(1);
  }
}

makeUserAdmin();