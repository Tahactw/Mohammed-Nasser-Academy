# React Academy App

A modern, full-stack web application for an online academy platform with digital book sales, course management, and user engagement features.

## Features

- 📚 Digital book marketplace with cart and checkout
- 🎓 Course management system with progress tracking
- 👤 User profiles with messaging and reviews
- 🎁 Book gifting system
- 💳 Paymob payment integration
- 🌐 Multi-language support (English/Arabic with RTL)
- 🎨 Light/Dark theme support
- 🔐 Secure authentication with Supabase
- 👨‍💼 Comprehensive admin panel

## Tech Stack

- **Frontend**: React 18 with TypeScript, Material-UI
- **Backend**: Supabase (Database, Auth, Storage)
- **Payments**: Paymob
- **Deployment**: Vercel
- **Development**: GitHub Codespaces

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm
- Git
- GitHub account (for Codespaces)
- Vercel account (for deployment)
- Supabase project (already configured)

### Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd react-academy-app
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - The Supabase and Paymob credentials are already configured

4. Run the development server:
```bash
npm run dev
```

5. Open http://localhost:3000

### GitHub Codespaces Setup

1. Fork this repository to your GitHub account
2. Click the "Code" button and select "Open with Codespaces"
3. Create a new codespace
4. Once loaded, run:
```bash
npm install
npm run dev
```
5. The application will be available through the Codespaces port forwarding

### Supabase Setup

Run the SQL script provided in `supabase-setup.sql` in your Supabase SQL editor to create all necessary tables and policies.

### Deployment to Vercel

1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Configure environment variables in Vercel:
   - Add all variables from `.env`
4. Deploy!

## Development Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm test` - Run tests
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── assets/          # Images, icons, fonts
├── components/      # Reusable UI components
├── context/         # React Context providers
├── hooks/           # Custom React hooks
├── pages/           # Page components
├── services/        # API and external services
├── styles/          # Global styles and themes
├── types/           # TypeScript type definitions
├── utils/           # Utility functions
└── App.tsx          # Main application component
```

## Key Features Implementation

### Authentication
- Email/password authentication via Supabase
- Email verification required for purchases
- Secure session management

### Book Store
- Browse and search books
- Add to cart functionality
- Gift books to other users
- Paymob payment integration
- Unlimited downloads for purchased books

### Course System
- View available courses
- Track progress
- Download certificates upon completion
- Telegram integration for enrollment

### User Features
- Customizable profiles with avatars
- Messaging system
- Review and rating system
- Block/unblock other users
- Gift history tracking

### Admin Panel
- Manage books and courses
- User management and moderation
- Badge and certificate assignment
- Transaction monitoring
- Site-wide notifications

## Security Considerations

- All API calls are authenticated
- File uploads restricted by type and size
- XSS and CSRF protection implemented
- Secure payment handling with Paymob
- Row Level Security in Supabase

## Performance Optimizations

- Lazy loading for routes
- Optimized image loading
- Efficient state management
- Minimal re-renders with React.memo

## Accessibility

- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- RTL language support

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License

## Support

For issues or questions, please contact the development team.

---

**Note**: This application uses pre-configured Supabase and Paymob credentials. For production use, ensure you have proper security measures in place and use your own credentials.