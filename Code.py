import os
import json
import base64

def create_file(path, content):
    """Create a file with the given content."""
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_project():
    """Create the complete React academy project structure."""
    
    # Package.json
    create_file('package.json', '''{
  "name": "react-academy-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "jest",
    "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.14.19",
    "@mui/material": "^5.14.20",
    "@mui/x-date-pickers": "^6.18.3",
    "@supabase/supabase-js": "^2.39.0",
    "axios": "^1.6.2",
    "date-fns": "^2.30.0",
    "i18next": "^23.7.6",
    "i18next-browser-languagedetector": "^7.2.0",
    "i18next-http-backend": "^2.4.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-i18next": "^13.5.0",
    "react-router-dom": "^6.20.1",
    "uuid": "^9.0.1"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/react": "^14.1.2",
    "@testing-library/user-event": "^14.5.1",
    "@types/jest": "^29.5.11",
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@types/uuid": "^9.0.7",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "ts-jest": "^29.1.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }
}''')

    # tsconfig.json
    create_file('tsconfig.json', '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}''')

    # tsconfig.node.json
    create_file('tsconfig.node.json', '''{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}''')

    # vite.config.ts
    create_file('vite.config.ts', '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 3000,
    host: true
  }
})''')

    # .env
    create_file('.env', '''VITE_SUPABASE_URL=https://qkfgvniqkwbrvolkedsv.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrZmd2bmlxa3dicnZvbGtlZHN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI3NzUwODMsImV4cCI6MjA2ODM1MTA4M30.GJdUPpUcaZwdv4fau2PelnrfjWNL7wH8qgtvQtnwElE
VITE_API_URL=auto
VITE_PAYMOB_API_KEY=ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TVRBMk1URXlOeXdpYm1GdFpTSTZJbWx1YVhScFlXd2lmUS5NckRTanoyeXZpVE5zdE1MX2w0cC1XNF84dzRZM2NMM2o4Z0FxN1BFMWppczlEaVhQN2EwRFVQMFQ5amlSQVVxTE9KUHM1bXQwODltY2dvNnV1a191UQ====
VITE_PAYMOB_IFRAME_ID=940881''')

    # .gitignore
    create_file('.gitignore', '''node_modules
dist
dist-ssr
*.local
.env
.env.local
.env.production
.DS_Store
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.vscode
.idea
*.swp
*.swo
coverage''')

    # README.md
    create_file('README.md', '''# React Academy App

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

**Note**: This application uses pre-configured Supabase and Paymob credentials. For production use, ensure you have proper security measures in place and use your own credentials.''')

    # index.html
    create_file('index.html', '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Online Academy - Learn and grow with our digital books and courses" />
    <title>React Academy</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>''')

    # Create public directory files
    create_file('public/favicon.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="4" fill="#1976d2"/>
  <path d="M8 10h16v2H8zm0 4h16v2H8zm0 4h12v2H8z" fill="white"/>
</svg>''')

    create_file('public/manifest.json', '''{
  "short_name": "Academy",
  "name": "React Academy App",
  "icons": [
    {
      "src": "favicon.svg",
      "sizes": "any",
      "type": "image/svg+xml"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#1976d2",
  "background_color": "#ffffff"
}''')

    # src/main.tsx
    create_file('src/main.tsx', '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)''')

    # src/App.tsx
    create_file('src/App.tsx', '''import React, { Suspense, lazy } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { CssBaseline, CircularProgress, Box } from '@mui/material'
import { LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import './i18n'

// Contexts
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import { NotificationProvider } from './context/NotificationContext'
import { CartProvider } from './context/CartContext'
import { LanguageProvider } from './context/LanguageContext'

// Layout
import Layout from './components/Layout'

// Lazy load pages
const HomePage = lazy(() => import('./pages/Home'))
const BooksPage = lazy(() => import('./pages/Books'))
const BookDetailPage = lazy(() => import('./pages/BookDetail'))
const CoursesPage = lazy(() => import('./pages/Courses'))
const ProfilePage = lazy(() => import('./pages/Profile'))
const AdminPage = lazy(() => import('./pages/Admin'))
const RegisterPage = lazy(() => import('./pages/Register'))
const LoginPage = lazy(() => import('./pages/Login'))
const CartPage = lazy(() => import('./pages/Cart'))
const NotFoundPage = lazy(() => import('./pages/NotFound'))

// Loading component
const Loading = () => (
  <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
    <CircularProgress />
  </Box>
)

function App() {
  return (
    <BrowserRouter>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <LanguageProvider>
          <ThemeProvider>
            <AuthProvider>
              <NotificationProvider>
                <CartProvider>
                  <CssBaseline />
                  <Layout>
                    <Suspense fallback={<Loading />}>
                      <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/books" element={<BooksPage />} />
                        <Route path="/books/:id" element={<BookDetailPage />} />
                        <Route path="/courses" element={<CoursesPage />} />
                        <Route path="/profile/:userId?" element={<ProfilePage />} />
                        <Route path="/admin/*" element={<AdminPage />} />
                        <Route path="/register" element={<RegisterPage />} />
                        <Route path="/login" element={<LoginPage />} />
                        <Route path="/cart" element={<CartPage />} />
                        <Route path="/404" element={<NotFoundPage />} />
                        <Route path="*" element={<Navigate to="/404" replace />} />
                      </Routes>
                    </Suspense>
                  </Layout>
                </CartProvider>
              </NotificationProvider>
            </AuthProvider>
          </ThemeProvider>
        </LanguageProvider>
      </LocalizationProvider>
    </BrowserRouter>
  )
}

export default App''')

    # src/i18n.ts
    create_file('src/i18n.ts', '''import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

const resources = {
  en: {
    translation: {
      // Common
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
      cancel: 'Cancel',
      save: 'Save',
      delete: 'Delete',
      edit: 'Edit',
      submit: 'Submit',
      search: 'Search',
      filter: 'Filter',
      sort: 'Sort',
      back: 'Back',
      next: 'Next',
      previous: 'Previous',
      close: 'Close',
      confirm: 'Confirm',
      yes: 'Yes',
      no: 'No',
      
      // Navigation
      home: 'Home',
      books: 'Books',
      courses: 'Courses',
      profile: 'Profile',
      admin: 'Admin',
      login: 'Login',
      register: 'Register',
      logout: 'Logout',
      cart: 'Cart',
      
      // Auth
      email: 'Email',
      password: 'Password',
      confirmPassword: 'Confirm Password',
      username: 'Username',
      forgotPassword: 'Forgot Password?',
      alreadyHaveAccount: 'Already have an account?',
      dontHaveAccount: "Don't have an account?",
      signIn: 'Sign In',
      signUp: 'Sign Up',
      
      // Books
      addToCart: 'Add to Cart',
      gift: 'Gift',
      download: 'Download',
      price: 'Price',
      description: 'Description',
      whoOwnsThis: 'Who owns this book',
      reviews: 'Reviews',
      writeReview: 'Write a review',
      rating: 'Rating',
      reply: 'Reply',
      like: 'Like',
      
      // Courses
      notStarted: 'Not Started',
      inProgress: 'In Progress',
      completed: 'Completed',
      enrollNow: 'Enroll Now',
      joinTelegram: 'Join Telegram Group',
      downloadCertificate: 'Download Certificate',
      startDate: 'Start Date',
      endDate: 'End Date',
      
      // Profile
      bio: 'Bio',
      avatar: 'Avatar',
      badges: 'Badges',
      certificates: 'Certificates',
      messages: 'Messages',
      notifications: 'Notifications',
      settings: 'Settings',
      privacy: 'Privacy',
      bookOwnership: 'Book Ownership',
      courseHistory: 'Course History',
      giftHistory: 'Gift History',
      blockedUsers: 'Blocked Users',
      block: 'Block',
      unblock: 'Unblock',
      
      // Cart & Checkout
      emptyCart: 'Your cart is empty',
      subtotal: 'Subtotal',
      total: 'Total',
      checkout: 'Checkout',
      remove: 'Remove',
      proceedToPayment: 'Proceed to Payment',
      
      // Admin
      dashboard: 'Dashboard',
      manageBooks: 'Manage Books',
      manageCourses: 'Manage Courses',
      manageUsers: 'Manage Users',
      transactions: 'Transactions',
      siteSettings: 'Site Settings',
      
      // Notifications
      giftReceived: 'You received a gift!',
      newMessage: 'New message',
      courseCompleted: 'Course completed',
      certificateIssued: 'Certificate issued',
      profileVisit: 'Someone visited your profile',
      
      // Errors
      invalidEmail: 'Invalid email address',
      passwordTooShort: 'Password must be at least 8 characters',
      passwordsDontMatch: 'Passwords do not match',
      usernameTaken: 'Username already taken',
      loginFailed: 'Login failed',
      registrationFailed: 'Registration failed',
      
      // Success messages
      loginSuccess: 'Successfully logged in',
      registrationSuccess: 'Registration successful',
      bookAddedToCart: 'Book added to cart',
      giftSent: 'Gift sent successfully',
      reviewPosted: 'Review posted',
      profileUpdated: 'Profile updated',
      
      // Misc
      pageNotFound: 'Page not found',
      backToHome: 'Back to home',
      theme: 'Theme',
      language: 'Language',
      light: 'Light',
      dark: 'Dark',
      english: 'English',
      arabic: 'العربية'
    }
  },
  ar: {
    translation: {
      // Common
      loading: 'جاري التحميل...',
      error: 'خطأ',
      success: 'نجاح',
      cancel: 'إلغاء',
      save: 'حفظ',
      delete: 'حذف',
      edit: 'تعديل',
      submit: 'إرسال',
      search: 'بحث',
      filter: 'تصفية',
      sort: 'ترتيب',
      back: 'رجوع',
      next: 'التالي',
      previous: 'السابق',
      close: 'إغلاق',
      confirm: 'تأكيد',
      yes: 'نعم',
      no: 'لا',
      
      // Navigation
      home: 'الرئيسية',
      books: 'الكتب',
      courses: 'الدورات',
      profile: 'الملف الشخصي',
      admin: 'الإدارة',
      login: 'تسجيل الدخول',
      register: 'التسجيل',
      logout: 'تسجيل الخروج',
      cart: 'السلة',
      
      // Auth
      email: 'البريد الإلكتروني',
      password: 'كلمة المرور',
      confirmPassword: 'تأكيد كلمة المرور',
      username: 'اسم المستخدم',
      forgotPassword: 'نسيت كلمة المرور؟',
      alreadyHaveAccount: 'لديك حساب بالفعل؟',
      dontHaveAccount: 'ليس لديك حساب؟',
      signIn: 'تسجيل الدخول',
      signUp: 'إنشاء حساب',
      
      // Books
      addToCart: 'أضف إلى السلة',
      gift: 'إهداء',
      download: 'تحميل',
      price: 'السعر',
      description: 'الوصف',
      whoOwnsThis: 'من يملك هذا الكتاب',
      reviews: 'المراجعات',
      writeReview: 'اكتب مراجعة',
      rating: 'التقييم',
      reply: 'رد',
      like: 'إعجاب',
      
      // Courses
      notStarted: 'لم تبدأ',
      inProgress: 'قيد التقدم',
      completed: 'مكتملة',
      enrollNow: 'سجل الآن',
      joinTelegram: 'انضم لمجموعة التليجرام',
      downloadCertificate: 'تحميل الشهادة',
      startDate: 'تاريخ البداية',
      endDate: 'تاريخ النهاية',
      
      // Profile
      bio: 'نبذة',
      avatar: 'الصورة الشخصية',
      badges: 'الشارات',
      certificates: 'الشهادات',
      messages: 'الرسائل',
      notifications: 'الإشعارات',
      settings: 'الإعدادات',
      privacy: 'الخصوصية',
      bookOwnership: 'ملكية الكتب',
      courseHistory: 'سجل الدورات',
      giftHistory: 'سجل الهدايا',
      blockedUsers: 'المستخدمون المحظورون',
      block: 'حظر',
      unblock: 'إلغاء الحظر',
      
      // Cart & Checkout
      emptyCart: 'سلتك فارغة',
      subtotal: 'المجموع الفرعي',
      total: 'المجموع',
      checkout: 'الدفع',
      remove: 'إزالة',
      proceedToPayment: 'المتابعة للدفع',
      
      // Admin
      dashboard: 'لوحة التحكم',
      manageBooks: 'إدارة الكتب',
      manageCourses: 'إدارة الدورات',
      manageUsers: 'إدارة المستخدمين',
      transactions: 'المعاملات',
      siteSettings: 'إعدادات الموقع',
      
      // Notifications
      giftReceived: 'لقد تلقيت هدية!',
      newMessage: 'رسالة جديدة',
      courseCompleted: 'اكتملت الدورة',
      certificateIssued: 'تم إصدار الشهادة',
      profileVisit: 'قام شخص بزيارة ملفك الشخصي',
      
      // Errors
      invalidEmail: 'عنوان بريد إلكتروني غير صالح',
      passwordTooShort: 'يجب أن تكون كلمة المرور 8 أحرف على الأقل',
      passwordsDontMatch: 'كلمات المرور غير متطابقة',
      usernameTaken: 'اسم المستخدم مأخوذ بالفعل',
      loginFailed: 'فشل تسجيل الدخول',
      registrationFailed: 'فشل التسجيل',
      
      // Success messages
      loginSuccess: 'تم تسجيل الدخول بنجاح',
      registrationSuccess: 'تم التسجيل بنجاح',
      bookAddedToCart: 'تمت إضافة الكتاب إلى السلة',
      giftSent: 'تم إرسال الهدية بنجاح',
      reviewPosted: 'تم نشر المراجعة',
      profileUpdated: 'تم تحديث الملف الشخصي',
      
      // Misc
      pageNotFound: 'الصفحة غير موجودة',
      backToHome: 'العودة للرئيسية',
      theme: 'المظهر',
      language: 'اللغة',
      light: 'فاتح',
      dark: 'داكن',
      english: 'English',
      arabic: 'العربية'
    }
  }
}

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    debug: false,
    interpolation: {
      escapeValue: false
    },
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage']
    }
  })

export default i18n''')

    # Create types
    create_file('src/types/index.ts', '''export interface User {
  id: string
  email: string
  username: string
  avatar_url?: string
  bio?: string
  is_admin: boolean
  is_banned: boolean
  email_verified: boolean
  created_at: string
  updated_at: string
  course_progress_public: boolean
}

export interface Book {
  id: string
  title: string
  description: string
  cover_url: string
  file_url: string
  price: number
  created_at: string
  updated_at: string
}

export interface Course {
  id: string
  title: string
  description: string
  image_url: string
  start_date: string
  end_date: string
  telegram_link?: string
  created_at: string
  updated_at: string
}

export interface Review {
  id: string
  book_id: string
  user_id: string
  rating: number
  content?: string
  created_at: string
  updated_at: string
  user?: User
  likes_count: number
  user_has_liked?: boolean
  replies?: ReviewReply[]
}

export interface ReviewReply {
  id: string
  review_id: string
  user_id: string
  content: string
  created_at: string
  user?: User
}

export interface BookOwnership {
  id: string
  book_id: string
  user_id: string
  purchase_date: string
  transaction_id?: string
  is_gift: boolean
  gifted_by?: string
  gift_message?: string
  book?: Book
  user?: User
  gifter?: User
}

export interface CourseEnrollment {
  id: string
  course_id: string
  user_id: string
  status: 'not_started' | 'in_progress' | 'completed'
  progress: number
  enrolled_at: string
  completed_at?: string
  certificate_url?: string
  course?: Course
  user?: User
}

export interface Badge {
  id: string
  name: string
  description: string
  icon_url: string
  created_at: string
}

export interface UserBadge {
  id: string
  user_id: string
  badge_id: string
  assigned_at: string
  assigned_by: string
  badge?: Badge
}

export interface Certificate {
  id: string
  user_id: string
  course_id: string
  certificate_url: string
  issued_at: string
  issued_by: string
  course?: Course
  user?: User
}

export interface Message {
  id: string
  sender_id: string
  recipient_id: string
  content: string
  created_at: string
  read_at?: string
  sender?: User
  recipient?: User
}

export interface Notification {
  id: string
  user_id: string
  type: 'gift' | 'message' | 'review_like' | 'review_reply' | 'profile_visit' | 'course_complete' | 'certificate' | 'custom'
  title: string
  content: string
  data?: any
  read_at?: string
  created_at: string
}

export interface Transaction {
  id: string
  user_id: string
  amount: number
  currency: string
  status: 'pending' | 'completed' | 'failed'
  paymob_transaction_id?: string
  items: TransactionItem[]
  created_at: string
  completed_at?: string
  user?: User
}

export interface TransactionItem {
  book_id: string
  quantity: number
  price: number
  is_gift: boolean
  recipient_id?: string
  gift_message?: string
}

export interface BlockedUser {
  id: string
  blocker_id: string
  blocked_id: string
  created_at: string
  blocked_user?: User
}

export interface CartItem {
  book: Book
  quantity: number
  recipients?: Array<{
    userId: string
    message: string
  }>
}

export interface AdminLog {
  id: string
  admin_id: string
  action: string
  entity_type: string
  entity_id: string
  details?: any
  created_at: string
  admin?: User
}''')

    # Create styles
    create_file('src/styles/global.css', '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}

/* RTL Support */
[dir="rtl"] {
  font-family: 'Inter', 'Tajawal', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Arial', sans-serif;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Dark mode scrollbar */
[data-theme="dark"] ::-webkit-scrollbar-track {
  background: #1e1e1e;
}

[data-theme="dark"] ::-webkit-scrollbar-thumb {
  background: #4a4a4a;
}

[data-theme="dark"] ::-webkit-scrollbar-thumb:hover {
  background: #6a6a6a;
}''')

    # Create theme configuration
    create_file('src/styles/theme.ts', '''import { createTheme, ThemeOptions } from '@mui/material/styles'

const baseTheme: ThemeOptions = {
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 8,
  },
}

export const lightTheme = createTheme({
  ...baseTheme,
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#e33371',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
    text: {
      primary: 'rgba(0, 0, 0, 0.87)',
      secondary: 'rgba(0, 0, 0, 0.6)',
    },
  },
})

export const darkTheme = createTheme({
  ...baseTheme,
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
      light: '#bbdefb',
      dark: '#64b5f6',
    },
    secondary: {
      main: '#f48fb1',
      light: '#f6a5c0',
      dark: '#ec407a',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
    text: {
      primary: '#ffffff',
      secondary: 'rgba(255, 255, 255, 0.7)',
    },
  },
})

export const rtlTheme = (theme: typeof lightTheme) => createTheme({
  ...theme,
  direction: 'rtl',
  typography: {
    ...theme.typography,
    fontFamily: '"Inter", "Tajawal", -apple-system, BlinkMacSystemFont, "Arial", sans-serif',
  },
})''')

    # Services
    create_file('src/services/supabase.ts', '''import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
})

// Helper functions
export const getCurrentUser = async () => {
  const { data: { user } } = await supabase.auth.getUser()
  return user
}

export const signUp = async (email: string, password: string, username: string) => {
  // First create auth user
  const { data: authData, error: authError } = await supabase.auth.signUp({
    email,
    password,
  })

  if (authError) throw authError

  // Then create profile
  if (authData.user) {
    const { error: profileError } = await supabase
      .from('users')
      .insert({
        id: authData.user.id,
        email,
        username,
        email_verified: false,
        is_admin: false,
        is_banned: false,
        course_progress_public: true
      })

    if (profileError) throw profileError
  }

  return authData
}

export const signIn = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })

  if (error) throw error
  return data
}

export const signOut = async () => {
  const { error } = await supabase.auth.signOut()
  if (error) throw error
}

export const resetPassword = async (email: string) => {
  const { error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: `${window.location.origin}/reset-password`,
  })
  if (error) throw error
}

export const updatePassword = async (newPassword: string) => {
  const { error } = await supabase.auth.updateUser({
    password: newPassword
  })
  if (error) throw error
}

// Storage helpers
export const uploadFile = async (bucket: string, path: string, file: File) => {
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(path, file, {
      cacheControl: '3600',
      upsert: true
    })

  if (error) throw error
  return data
}

export const getPublicUrl = (bucket: string, path: string) => {
  const { data } = supabase.storage
    .from(bucket)
    .getPublicUrl(path)
  
  return data.publicUrl
}

export const deleteFile = async (bucket: string, path: string) => {
  const { error } = await supabase.storage
    .from(bucket)
    .remove([path])

  if (error) throw error
}''')

    # API services
    create_file('src/services/api/books.ts', '''import { supabase } from '../supabase'
import { Book, BookOwnership } from '@/types'

export const booksApi = {
  // Get all books
  async getAll() {
    const { data, error } = await supabase
      .from('books')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as Book[]
  },

  // Get single book
  async getById(id: string) {
    const { data, error } = await supabase
      .from('books')
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data as Book
  },

  // Search books
  async search(query: string) {
    const { data, error } = await supabase
      .from('books')
      .select('*')
      .or(`title.ilike.%${query}%,description.ilike.%${query}%`)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as Book[]
  },

  // Get book owners
  async getOwners(bookId: string) {
    const { data, error } = await supabase
      .from('book_ownership')
      .select(`
        *,
        user:users(id, username, avatar_url)
      `)
      .eq('book_id', bookId)
      .order('purchase_date', { ascending: false })

    if (error) throw error
    return data as BookOwnership[]
  },

  // Check if user owns book
  async checkOwnership(bookId: string, userId: string) {
    const { data, error } = await supabase
      .from('book_ownership')
      .select('id')
      .eq('book_id', bookId)
      .eq('user_id', userId)
      .single()

    if (error && error.code !== 'PGRST116') throw error
    return !!data
  },

  // Get user's books
  async getUserBooks(userId: string) {
    const { data, error } = await supabase
      .from('book_ownership')
      .select(`
        *,
        book:books(*)
      `)
      .eq('user_id', userId)
      .order('purchase_date', { ascending: false })

    if (error) throw error
    return data as BookOwnership[]
  },

  // Create book (admin)
  async create(book: Omit<Book, 'id' | 'created_at' | 'updated_at'>) {
    const { data, error } = await supabase
      .from('books')
      .insert(book)
      .select()
      .single()

    if (error) throw error
    return data as Book
  },

  // Update book (admin)
  async update(id: string, updates: Partial<Book>) {
    const { data, error } = await supabase
      .from('books')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as Book
  },

  // Delete book (admin)
  async delete(id: string) {
    const { error } = await supabase
      .from('books')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Gift book
  async gift(bookId: string, recipientId: string, message: string, gifterId: string) {
    // Check if recipient already owns the book
    const ownership = await this.checkOwnership(bookId, recipientId)
    if (ownership) {
      throw new Error('Recipient already owns this book')
    }

    const { data, error } = await supabase
      .from('book_ownership')
      .insert({
        book_id: bookId,
        user_id: recipientId,
        is_gift: true,
        gifted_by: gifterId,
        gift_message: message,
        purchase_date: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data as BookOwnership
  }
}''')

    create_file('src/services/api/courses.ts', '''import { supabase } from '../supabase'
import { Course, CourseEnrollment } from '@/types'

export const coursesApi = {
  // Get all courses
  async getAll() {
    const { data, error } = await supabase
      .from('courses')
      .select('*')
      .order('start_date', { ascending: false })

    if (error) throw error
    return data as Course[]
  },

  // Get single course
  async getById(id: string) {
    const { data, error } = await supabase
      .from('courses')
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data as Course
  },

  // Get user's enrollments
  async getUserEnrollments(userId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .select(`
        *,
        course:courses(*)
      `)
      .eq('user_id', userId)
      .order('enrolled_at', { ascending: false })

    if (error) throw error
    return data as CourseEnrollment[]
  },

  // Get course enrollments
  async getCourseEnrollments(courseId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .select(`
        *,
        user:users(id, username, avatar_url)
      `)
      .eq('course_id', courseId)
      .order('enrolled_at', { ascending: false })

    if (error) throw error
    return data as CourseEnrollment[]
  },

  // Check enrollment
  async checkEnrollment(courseId: string, userId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .select('*')
      .eq('course_id', courseId)
      .eq('user_id', userId)
      .single()

    if (error && error.code !== 'PGRST116') throw error
    return data as CourseEnrollment | null
  },

  // Create course (admin)
  async create(course: Omit<Course, 'id' | 'created_at' | 'updated_at'>) {
    const { data, error } = await supabase
      .from('courses')
      .insert(course)
      .select()
      .single()

    if (error) throw error
    return data as Course
  },

  // Update course (admin)
  async update(id: string, updates: Partial<Course>) {
    const { data, error } = await supabase
      .from('courses')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as Course
  },

  // Delete course (admin)
  async delete(id: string) {
    const { error } = await supabase
      .from('courses')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Enroll user (admin)
  async enrollUser(courseId: string, userId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .insert({
        course_id: courseId,
        user_id: userId,
        status: 'not_started',
        progress: 0,
        enrolled_at: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data as CourseEnrollment
  },

  // Update enrollment (admin)
  async updateEnrollment(id: string, updates: Partial<CourseEnrollment>) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as CourseEnrollment
  },

  // Remove enrollment (admin)
  async removeEnrollment(courseId: string, userId: string) {
    const { error } = await supabase
      .from('course_enrollments')
      .delete()
      .eq('course_id', courseId)
      .eq('user_id', userId)

    if (error) throw error
  }
}''')

    create_file('src/services/api/users.ts', '''import { supabase } from '../supabase'
import { User, Badge, UserBadge, Certificate, BlockedUser } from '@/types'

export const usersApi = {
  // Get user profile
  async getProfile(userId: string) {
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .eq('id', userId)
      .single()

    if (error) throw error
    return data as User
  },

  // Get user by username
  async getByUsername(username: string) {
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .eq('username', username)
      .single()

    if (error) throw error
    return data as User
  },

  // Update profile
  async updateProfile(userId: string, updates: Partial<User>) {
    const { data, error } = await supabase
      .from('users')
      .update(updates)
      .eq('id', userId)
      .select()
      .single()

    if (error) throw error
    return data as User
  },

  // Check username availability
  async checkUsername(username: string, currentUserId?: string) {
    let query = supabase
      .from('users')
      .select('id')
      .eq('username', username)

    if (currentUserId) {
      query = query.neq('id', currentUserId)
    }

    const { data, error } = await query.single()

    if (error && error.code !== 'PGRST116') throw error
    return !data
  },

  // Get user's badges
  async getUserBadges(userId: string) {
    const { data, error } = await supabase
      .from('user_badges')
      .select(`
        *,
        badge:badges(*)
      `)
      .eq('user_id', userId)
      .order('assigned_at', { ascending: false })

    if (error) throw error
    return data as UserBadge[]
  },

  // Get user's certificates
  async getUserCertificates(userId: string) {
    const { data, error } = await supabase
      .from('certificates')
      .select(`
        *,
        course:courses(*)
      `)
      .eq('user_id', userId)
      .order('issued_at', { ascending: false })

    if (error) throw error
    return data as Certificate[]
  },

  // Get blocked users
  async getBlockedUsers(userId: string) {
    const { data, error } = await supabase
      .from('blocked_users')
      .select(`
        *,
        blocked_user:users!blocked_users_blocked_id_fkey(id, username, avatar_url)
      `)
      .eq('blocker_id', userId)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as BlockedUser[]
  },

  // Check if blocked
  async isBlocked(blockerId: string, blockedId: string) {
    const { data, error } = await supabase
      .from('blocked_users')
      .select('id')
      .eq('blocker_id', blockerId)
      .eq('blocked_id', blockedId)
      .single()

    if (error && error.code !== 'PGRST116') throw error
    return !!data
  },

  // Block user
  async blockUser(blockerId: string, blockedId: string) {
    const { data, error } = await supabase
      .from('blocked_users')
      .insert({
        blocker_id: blockerId,
        blocked_id: blockedId
      })
      .select()
      .single()

    if (error) throw error
    return data as BlockedUser
  },

  // Unblock user
  async unblockUser(blockerId: string, blockedId: string) {
    const { error } = await supabase
      .from('blocked_users')
      .delete()
      .eq('blocker_id', blockerId)
      .eq('blocked_id', blockedId)

    if (error) throw error
  },

  // Delete account
  async deleteAccount(userId: string) {
    // This should cascade delete all user data
    const { error } = await supabase
      .from('users')
      .delete()
      .eq('id', userId)

    if (error) throw error

    // Also delete auth user
    const { error: authError } = await supabase.auth.admin.deleteUser(userId)
    if (authError) throw authError
  },

  // Admin: Get all users
  async getAllUsers() {
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as User[]
  },

  // Admin: Ban user
  async banUser(userId: string) {
    const { data, error } = await supabase
      .from('users')
      .update({ is_banned: true })
      .eq('id', userId)
      .select()
      .single()

    if (error) throw error
    return data as User
  },

  // Admin: Unban user
  async unbanUser(userId: string) {
    const { data, error } = await supabase
      .from('users')
      .update({ is_banned: false })
      .eq('id', userId)
      .select()
      .single()

    if (error) throw error
    return data as User
  }
}''')

    create_file('src/services/api/reviews.ts', '''import { supabase } from '../supabase'
import { Review, ReviewReply } from '@/types'

export const reviewsApi = {
  // Get book reviews
  async getBookReviews(bookId: string) {
    const { data, error } = await supabase
      .from('reviews')
      .select(`
        *,
        user:users!reviews_user_id_fkey(id, username, avatar_url, is_banned),
        likes:review_likes(user_id)
      `)
      .eq('book_id', bookId)
      .order('created_at', { ascending: false })

    if (error) throw error
    
    // Filter out reviews from banned users
    const filteredData = (data || []).filter(review => !review.user?.is_banned)
    
    // Add likes count and user_has_liked
    const currentUser = await supabase.auth.getUser()
    const userId = currentUser.data.user?.id

    return filteredData.map(review => ({
      ...review,
      likes_count: review.likes?.length || 0,
      user_has_liked: userId ? review.likes?.some(like => like.user_id === userId) : false
    })) as Review[]
  },

  // Get review replies
  async getReviewReplies(reviewId: string) {
    const { data, error } = await supabase
      .from('review_replies')
      .select(`
        *,
        user:users(id, username, avatar_url)
      `)
      .eq('review_id', reviewId)
      .order('created_at', { ascending: true })

    if (error) throw error
    return data as ReviewReply[]
  },

  // Create review
  async createReview(review: Omit<Review, 'id' | 'created_at' | 'updated_at' | 'likes_count' | 'user_has_liked'>) {
    const { data, error } = await supabase
      .from('reviews')
      .insert(review)
      .select()
      .single()

    if (error) throw error
    return data as Review
  },

  // Update review
  async updateReview(id: string, updates: Partial<Review>) {
    const { data, error } = await supabase
      .from('reviews')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as Review
  },

  // Delete review
  async deleteReview(id: string) {
    const { error } = await supabase
      .from('reviews')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Like review
  async likeReview(reviewId: string, userId: string) {
    const { error } = await supabase
      .from('review_likes')
      .insert({
        review_id: reviewId,
        user_id: userId
      })

    if (error) throw error
  },

  // Unlike review
  async unlikeReview(reviewId: string, userId: string) {
    const { error } = await supabase
      .from('review_likes')
      .delete()
      .eq('review_id', reviewId)
      .eq('user_id', userId)

    if (error) throw error
  },

  // Create reply
  async createReply(reply: Omit<ReviewReply, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('review_replies')
      .insert(reply)
      .select()
      .single()

    if (error) throw error
    return data as ReviewReply
  },

  // Delete reply
  async deleteReply(id: string) {
    const { error } = await supabase
      .from('review_replies')
      .delete()
      .eq('id', id)

    if (error) throw error
  }
}''')

    create_file('src/services/api/messages.ts', '''import { supabase } from '../supabase'
import { Message } from '@/types'

export const messagesApi = {
  // Get user's messages
  async getUserMessages(userId: string) {
    const { data, error } = await supabase
      .from('messages')
      .select(`
        *,
        sender:users!messages_sender_id_fkey(id, username, avatar_url),
        recipient:users!messages_recipient_id_fkey(id, username, avatar_url)
      `)
      .or(`sender_id.eq.${userId},recipient_id.eq.${userId}`)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as Message[]
  },

  // Get conversation
  async getConversation(userId1: string, userId2: string) {
    const { data, error } = await supabase
      .from('messages')
      .select(`
        *,
        sender:users!messages_sender_id_fkey(id, username, avatar_url),
        recipient:users!messages_recipient_id_fkey(id, username, avatar_url)
      `)
      .or(`and(sender_id.eq.${userId1},recipient_id.eq.${userId2}),and(sender_id.eq.${userId2},recipient_id.eq.${userId1})`)
      .order('created_at', { ascending: true })

    if (error) throw error
    return data as Message[]
  },

  // Send message
  async sendMessage(senderId: string, recipientId: string, content: string) {
    // Check if blocked
    const { data: blockData } = await supabase
      .from('blocked_users')
      .select('id')
      .or(`and(blocker_id.eq.${recipientId},blocked_id.eq.${senderId}),and(blocker_id.eq.${senderId},blocked_id.eq.${recipientId})`)
      .single()

    if (blockData) {
      throw new Error('Cannot send message to blocked user')
    }

    const { data, error } = await supabase
      .from('messages')
      .insert({
        sender_id: senderId,
        recipient_id: recipientId,
        content
      })
      .select()
      .single()

    if (error) throw error
    return data as Message
  },

  // Mark as read
  async markAsRead(messageId: string) {
    const { data, error } = await supabase
      .from('messages')
      .update({ read_at: new Date().toISOString() })
      .eq('id', messageId)
      .select()
      .single()

    if (error) throw error
    return data as Message
  },

  // Delete message
  async deleteMessage(messageId: string) {
    const { error } = await supabase
      .from('messages')
      .delete()
      .eq('id', messageId)

    if (error) throw error
  },

  // Get unread count
  async getUnreadCount(userId: string) {
    const { count, error } = await supabase
      .from('messages')
      .select('*', { count: 'exact', head: true })
      .eq('recipient_id', userId)
      .is('read_at', null)

    if (error) throw error
    return count || 0
  }
}''')

    create_file('src/services/api/notifications.ts', '''import { supabase } from '../supabase'
import { Notification } from '@/types'

export const notificationsApi = {
  // Get user notifications
  async getUserNotifications(userId: string) {
    const { data, error } = await supabase
      .from('notifications')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(50)

    if (error) throw error
    return data as Notification[]
  },

  // Create notification
  async create(notification: Omit<Notification, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('notifications')
      .insert(notification)
      .select()
      .single()

    if (error) throw error
    return data as Notification
  },

  // Mark as read
  async markAsRead(notificationId: string) {
    const { data, error } = await supabase
      .from('notifications')
      .update({ read_at: new Date().toISOString() })
      .eq('id', notificationId)
      .select()
      .single()

    if (error) throw error
    return data as Notification
  },

  // Mark all as read
  async markAllAsRead(userId: string) {
    const { error } = await supabase
      .from('notifications')
      .update({ read_at: new Date().toISOString() })
      .eq('user_id', userId)
      .is('read_at', null)

    if (error) throw error
  },

  // Delete notification
  async delete(notificationId: string) {
    const { error } = await supabase
      .from('notifications')
      .delete()
      .eq('id', notificationId)

    if (error) throw error
  },

  // Get unread count
  async getUnreadCount(userId: string) {
    const { count, error } = await supabase
      .from('notifications')
      .select('*', { count: 'exact', head: true })
      .eq('user_id', userId)
      .is('read_at', null)

    if (error) throw error
    return count || 0
  },

  // Create notification helpers
  async notifyGiftReceived(recipientId: string, gifterId: string, bookTitle: string) {
    return this.create({
      user_id: recipientId,
      type: 'gift',
      title: 'Gift Received',
      content: `You received "${bookTitle}" as a gift`,
      data: { gifterId, bookTitle }
    })
  },

  async notifyNewMessage(recipientId: string, senderId: string, senderName: string) {
    return this.create({
      user_id: recipientId,
      type: 'message',
      title: 'New Message',
      content: `${senderName} sent you a message`,
      data: { senderId }
    })
  },

  async notifyReviewLike(reviewerId: string, likerId: string, likerName: string) {
    return this.create({
      user_id: reviewerId,
      type: 'review_like',
      title: 'Review Liked',
      content: `${likerName} liked your review`,
      data: { likerId }
    })
  },

  async notifyReviewReply(reviewerId: string, replierId: string, replierName: string) {
    return this.create({
      user_id: reviewerId,
      type: 'review_reply',
      title: 'New Reply',
      content: `${replierName} replied to your review`,
      data: { replierId }
    })
  },

  async notifyProfileVisit(profileUserId: string, visitorId: string, visitorName: string) {
    return this.create({
      user_id: profileUserId,
      type: 'profile_visit',
      title: 'Profile Visit',
      content: `${visitorName} visited your profile`,
      data: { visitorId }
    })
  },

  async notifyCourseComplete(userId: string, courseTitle: string) {
    return this.create({
      user_id: userId,
      type: 'course_complete',
      title: 'Course Completed',
      content: `Congratulations! You completed "${courseTitle}"`,
      data: { courseTitle }
    })
  },

  async notifyCertificateIssued(userId: string, courseTitle: string) {
    return this.create({
      user_id: userId,
      type: 'certificate',
      title: 'Certificate Issued',
      content: `Your certificate for "${courseTitle}" is ready`,
      data: { courseTitle }
    })
  }
}''')

    create_file('src/services/api/admin.ts', '''import { supabase } from '../supabase'
import { AdminLog } from '@/types'

export const adminApi = {
  // Log admin action
  async logAction(adminId: string, action: string, entityType: string, entityId: string, details?: any) {
    const { data, error } = await supabase
      .from('admin_logs')
      .insert({
        admin_id: adminId,
        action,
        entity_type: entityType,
        entity_id: entityId,
        details
      })
      .select()
      .single()

    if (error) throw error
    return data as AdminLog
  },

  // Get admin logs
  async getLogs(limit = 100) {
    const { data, error } = await supabase
      .from('admin_logs')
      .select(`
        *,
        admin:users(id, username)
      `)
      .order('created_at', { ascending: false })
      .limit(limit)

    if (error) throw error
    return data as AdminLog[]
  },

  // Get dashboard stats
  async getDashboardStats() {
    const [
      { count: usersCount },
      { count: booksCount },
      { count: coursesCount },
      { count: transactionsCount }
    ] = await Promise.all([
      supabase.from('users').select('*', { count: 'exact', head: true }),
      supabase.from('books').select('*', { count: 'exact', head: true }),
      supabase.from('courses').select('*', { count: 'exact', head: true }),
      supabase.from('transactions').select('*', { count: 'exact', head: true })
    ])

    return {
      users: usersCount || 0,
      books: booksCount || 0,
      courses: coursesCount || 0,
      transactions: transactionsCount || 0
    }
  },

  // Badges management
  async getAllBadges() {
    const { data, error } = await supabase
      .from('badges')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data
  },

  async createBadge(badge: any) {
    const { data, error } = await supabase
      .from('badges')
      .insert(badge)
      .select()
      .single()

    if (error) throw error
    return data
  },

  async assignBadge(userId: string, badgeId: string, adminId: string) {
    const { data, error } = await supabase
      .from('user_badges')
      .insert({
        user_id: userId,
        badge_id: badgeId,
        assigned_by: adminId
      })
      .select()
      .single()

    if (error) throw error
    return data
  },

  async revokeBadge(userId: string, badgeId: string) {
    const { error } = await supabase
      .from('user_badges')
      .delete()
      .eq('user_id', userId)
      .eq('badge_id', badgeId)

    if (error) throw error
  },

  // Certificates management
  async issueCertificate(userId: string, courseId: string, certificateUrl: string, adminId: string) {
    const { data, error } = await supabase
      .from('certificates')
      .insert({
        user_id: userId,
        course_id: courseId,
        certificate_url: certificateUrl,
        issued_by: adminId
      })
      .select()
      .single()

    if (error) throw error
    return data
  },

  // Site settings
  async getSiteSettings() {
    const { data, error } = await supabase
      .from('site_settings')
      .select('*')
      .single()

    if (error && error.code !== 'PGRST116') throw error
    return data || {}
  },

  async updateSiteSettings(settings: any) {
    const { data, error } = await supabase
      .from('site_settings')
      .upsert(settings)
      .select()
      .single()

    if (error) throw error
    return data
  }
}''')

    create_file('src/services/paymob.ts', '''import axios from 'axios'
import { TransactionItem } from '@/types'

const PAYMOB_API_URL = 'https://accept.paymob.com/api'
const PAYMOB_API_KEY = import.meta.env.VITE_PAYMOB_API_KEY
const PAYMOB_IFRAME_ID = import.meta.env.VITE_PAYMOB_IFRAME_ID

interface PaymobAuthResponse {
  token: string
}

interface PaymobOrderResponse {
  id: number
}

interface PaymobPaymentKeyResponse {
  token: string
}

export class PaymobService {
  private apiKey: string
  private iframeId: string

  constructor() {
    this.apiKey = PAYMOB_API_KEY
    this.iframeId = PAYMOB_IFRAME_ID

    if (!this.apiKey || !this.iframeId) {
      throw new Error('Paymob configuration missing')
    }
  }

  // Step 1: Authentication
  private async authenticate(): Promise<string> {
    try {
      const response = await axios.post<PaymobAuthResponse>(
        `${PAYMOB_API_URL}/auth/tokens`,
        {
          api_key: this.apiKey
        }
      )
      return response.data.token
    } catch (error) {
      console.error('Paymob authentication failed:', error)
      throw new Error('Payment authentication failed')
    }
  }

  // Step 2: Create order
  private async createOrder(
    authToken: string,
    amount: number,
    items: TransactionItem[]
  ): Promise<number> {
    try {
      const response = await axios.post<PaymobOrderResponse>(
        `${PAYMOB_API_URL}/ecommerce/orders`,
        {
          auth_token: authToken,
          delivery_needed: false,
          amount_cents: Math.round(amount * 100), // Convert to cents
          currency: 'USD',
          items: items.map(item => ({
            name: item.book_id,
            amount_cents: Math.round(item.price * 100),
            quantity: item.quantity
          }))
        }
      )
      return response.data.id
    } catch (error) {
      console.error('Paymob order creation failed:', error)
      throw new Error('Order creation failed')
    }
  }

  // Step 3: Get payment key
  private async getPaymentKey(
    authToken: string,
    orderId: number,
    amount: number,
    billingData: any
  ): Promise<string> {
    try {
      const response = await axios.post<PaymobPaymentKeyResponse>(
        `${PAYMOB_API_URL}/acceptance/payment_keys`,
        {
          auth_token: authToken,
          amount_cents: Math.round(amount * 100),
          expiration: 600, // 10 minutes
          order_id: orderId,
          billing_data: billingData,
          currency: 'USD',
          integration_id: this.iframeId
        }
      )
      return response.data.token
    } catch (error) {
      console.error('Paymob payment key generation failed:', error)
      throw new Error('Payment key generation failed')
    }
  }

  // Main checkout function
  async initiateCheckout(
    amount: number,
    items: TransactionItem[],
    userEmail: string,
    userId: string
  ): Promise<string> {
    try {
      // Step 1: Authenticate
      const authToken = await this.authenticate()

      // Step 2: Create order
      const orderId = await this.createOrder(authToken, amount, items)

      // Step 3: Get payment key
      const billingData = {
        email: userEmail,
        first_name: 'User',
        last_name: userId,
        phone_number: '+201234567890', // Required by Paymob
        country: 'US',
        city: 'N/A',
        street: 'N/A',
        building: 'N/A',
        floor: 'N/A',
        apartment: 'N/A'
      }

      const paymentKey = await this.getPaymentKey(
        authToken,
        orderId,
        amount,
        billingData
      )

      // Return iframe URL
      return `https://accept.paymob.com/api/acceptance/iframes/${this.iframeId}?payment_token=${paymentKey}`
    } catch (error) {
      console.error('Checkout initiation failed:', error)
      throw error
    }
  }

  // Verify transaction (for webhook)
  async verifyTransaction(transactionId: string): Promise<boolean> {
    try {
      const authToken = await this.authenticate()
      
      const response = await axios.get(
        `${PAYMOB_API_URL}/acceptance/transactions/${transactionId}`,
        {
          headers: {
            Authorization: `Bearer ${authToken}`
          }
        }
      )

      return response.data.success === true
    } catch (error) {
      console.error('Transaction verification failed:', error)
      return false
    }
  }

  // Calculate HMAC for webhook verification
  calculateHMAC(data: any, secret: string): string {
    // Implementation depends on Paymob's specific HMAC calculation
    // This is a placeholder - implement according to Paymob docs
    const crypto = require('crypto')
    const hmac = crypto.createHmac('sha512', secret)
    hmac.update(JSON.stringify(data))
    return hmac.digest('hex')
  }
}

export const paymobService = new PaymobService()''')

    # Context providers
    create_file('src/context/AuthContext.tsx', '''import React, { createContext, useContext, useState, useEffect } from 'react'
import { User as SupabaseUser } from '@supabase/supabase-js'
import { supabase, getCurrentUser } from '@/services/supabase'
import { usersApi } from '@/services/api/users'
import { User } from '@/types'

interface AuthContextType {
  user: SupabaseUser | null
  profile: User | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string, username: string) => Promise<void>
  signOut: () => Promise<void>
  updateProfile: (updates: Partial<User>) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<SupabaseUser | null>(null)
  const [profile, setProfile] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check active sessions and sets the user
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      if (session?.user) {
        loadProfile(session.user.id)
      }
      setLoading(false)
    })

    // Listen for changes on auth state
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
      if (session?.user) {
        loadProfile(session.user.id)
      } else {
        setProfile(null)
      }
    })

    return () => subscription.unsubscribe()
  }, [])

  const loadProfile = async (userId: string) => {
    try {
      const profile = await usersApi.getProfile(userId)
      setProfile(profile)
    } catch (error) {
      console.error('Error loading profile:', error)
    }
  }

  const signIn = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    if (error) throw error
    if (data.user) {
      await loadProfile(data.user.id)
    }
  }

  const signUp = async (email: string, password: string, username: string) => {
    // Check username availability
    const isAvailable = await usersApi.checkUsername(username)
    if (!isAvailable) {
      throw new Error('Username already taken')
    }

    // Create auth user
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    })

    if (error) throw error

    // Create user profile
    if (data.user) {
      const { error: profileError } = await supabase
        .from('users')
        .insert({
          id: data.user.id,
          email,
          username,
          email_verified: false,
          is_admin: false,
          is_banned: false,
          course_progress_public: true
        })

      if (profileError) throw profileError
      await loadProfile(data.user.id)
    }
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
    setProfile(null)
  }

  const updateProfile = async (updates: Partial<User>) => {
    if (!user) throw new Error('No user logged in')
    
    const updatedProfile = await usersApi.updateProfile(user.id, updates)
    setProfile(updatedProfile)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        signIn,
        signUp,
        signOut,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}''')

    create_file('src/context/ThemeContext.tsx', '''import React, { createContext, useContext, useState, useEffect } from 'react'
import { ThemeProvider as MuiThemeProvider } from '@mui/material/styles'
import { lightTheme, darkTheme, rtlTheme } from '@/styles/theme'
import { useLanguage } from './LanguageContext'

interface ThemeContextType {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const saved = localStorage.getItem('theme')
    return (saved as 'light' | 'dark') || 'light'
  })
  
  const { language } = useLanguage()
  const isRTL = language === 'ar'

  useEffect(() => {
    localStorage.setItem('theme', theme)
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))
  }

  const muiTheme = theme === 'light' ? lightTheme : darkTheme
  const finalTheme = isRTL ? rtlTheme(muiTheme) : muiTheme

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <MuiThemeProvider theme={finalTheme}>
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  )
}''')

    create_file('src/context/LanguageContext.tsx', '''import React, { createContext, useContext, useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'

interface LanguageContextType {
  language: string
  changeLanguage: (lang: string) => void
  isRTL: boolean
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export const useLanguage = () => {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
}

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { i18n } = useTranslation()
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('language') || 'en'
  })

  const isRTL = language === 'ar'

  useEffect(() => {
    i18n.changeLanguage(language)
    localStorage.setItem('language', language)
    document.documentElement.lang = language
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr'
  }, [language, isRTL, i18n])

  const changeLanguage = (lang: string) => {
    setLanguage(lang)
  }

  return (
    <LanguageContext.Provider value={{ language, changeLanguage, isRTL }}>
      {children}
    </LanguageContext.Provider>
  )
}''')

    create_file('src/context/NotificationContext.tsx', '''import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { Snackbar, Alert, AlertColor } from '@mui/material'
import { notificationsApi } from '@/services/api/notifications'
import { Notification } from '@/types'
import { useAuth } from './AuthContext'

interface NotificationContextType {
  notifications: Notification[]
  unreadCount: number
  showNotification: (message: string, type?: AlertColor) => void
  markAsRead: (id: string) => Promise<void>
  markAllAsRead: () => Promise<void>
  deleteNotification: (id: string) => Promise<void>
  refreshNotifications: () => Promise<void>
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined)

export const useNotification = () => {
  const context = useContext(NotificationContext)
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider')
  }
  return context
}

export const NotificationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth()
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [snackbar, setSnackbar] = useState<{
    open: boolean
    message: string
    type: AlertColor
  }>({
    open: false,
    message: '',
    type: 'info'
  })

  const fetchNotifications = useCallback(async () => {
    if (!user) return

    try {
      const [notifs, count] = await Promise.all([
        notificationsApi.getUserNotifications(user.id),
        notificationsApi.getUnreadCount(user.id)
      ])
      setNotifications(notifs)
      setUnreadCount(count)
    } catch (error) {
      console.error('Error fetching notifications:', error)
    }
  }, [user])

  useEffect(() => {
    fetchNotifications()
    
    // Set up realtime subscription
    if (user) {
      const subscription = supabase
        .channel('notifications')
        .on(
          'postgres_changes',
          {
            event: 'INSERT',
            schema: 'public',
            table: 'notifications',
            filter: `user_id=eq.${user.id}`
          },
          (payload) => {
            setNotifications(prev => [payload.new as Notification, ...prev])
            setUnreadCount(prev => prev + 1)
            showNotification(payload.new.content, 'info')
          }
        )
        .subscribe()

      return () => {
        subscription.unsubscribe()
      }
    }
  }, [user, fetchNotifications])

  const showNotification = (message: string, type: AlertColor = 'info') => {
    setSnackbar({ open: true, message, type })
  }

  const markAsRead = async (id: string) => {
    await notificationsApi.markAsRead(id)
    setNotifications(prev =>
      prev.map(n => (n.id === id ? { ...n, read_at: new Date().toISOString() } : n))
    )
    setUnreadCount(prev => Math.max(0, prev - 1))
  }

  const markAllAsRead = async () => {
    if (!user) return
    await notificationsApi.markAllAsRead(user.id)
    setNotifications(prev =>
      prev.map(n => ({ ...n, read_at: n.read_at || new Date().toISOString() }))
    )
    setUnreadCount(0)
  }

  const deleteNotification = async (id: string) => {
    await notificationsApi.delete(id)
    setNotifications(prev => prev.filter(n => n.id !== id))
  }

  const refreshNotifications = async () => {
    await fetchNotifications()
  }

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        unreadCount,
        showNotification,
        markAsRead,
        markAllAsRead,
        deleteNotification,
        refreshNotifications
      }}
    >
      {children}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
      >
        <Alert
          onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
          severity={snackbar.type}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </NotificationContext.Provider>
  )
}''')

    create_file('src/context/CartContext.tsx', '''import React, { createContext, useContext, useState, useEffect } from 'react'
import { CartItem, Book } from '@/types'

interface CartContextType {
  items: CartItem[]
  itemCount: number
  total: number
  addToCart: (book: Book, quantity?: number) => void
  removeFromCart: (bookId: string) => void
  updateQuantity: (bookId: string, quantity: number) => void
  addGiftRecipient: (bookId: string, userId: string, message: string) => void
  removeGiftRecipient: (bookId: string, userId: string) => void
  clearCart: () => void
  isInCart: (bookId: string) => boolean
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}

const CART_STORAGE_KEY = 'academy_cart'

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>(() => {
    const saved = localStorage.getItem(CART_STORAGE_KEY)
    return saved ? JSON.parse(saved) : []
  })

  useEffect(() => {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items))
  }, [items])

  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0)
  const total = items.reduce((sum, item) => sum + (item.book.price * item.quantity), 0)

  const addToCart = (book: Book, quantity = 1) => {
    setItems(prev => {
      const existing = prev.find(item => item.book.id === book.id)
      if (existing) {
        return prev.map(item =>
          item.book.id === book.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        )
      }
      return [...prev, { book, quantity, recipients: [] }]
    })
  }

  const removeFromCart = (bookId: string) => {
    setItems(prev => prev.filter(item => item.book.id !== bookId))
  }

  const updateQuantity = (bookId: string, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(bookId)
    } else {
      setItems(prev =>
        prev.map(item =>
          item.book.id === bookId ? { ...item, quantity } : item
        )
      )
    }
  }

  const addGiftRecipient = (bookId: string, userId: string, message: string) => {
    setItems(prev =>
      prev.map(item => {
        if (item.book.id === bookId) {
          const recipients = item.recipients || []
          const existingIndex = recipients.findIndex(r => r.userId === userId)
          
          if (existingIndex >= 0) {
            // Update existing recipient
            recipients[existingIndex] = { userId, message }
          } else {
            // Add new recipient
            recipients.push({ userId, message })
          }
          
          return { ...item, recipients }
        }
        return item
      })
    )
  }

  const removeGiftRecipient = (bookId: string, userId: string) => {
    setItems(prev =>
      prev.map(item => {
        if (item.book.id === bookId) {
          const recipients = (item.recipients || []).filter(r => r.userId !== userId)
          return { ...item, recipients }
        }
        return item
      })
    )
  }

  const clearCart = () => {
    setItems([])
  }

  const isInCart = (bookId: string) => {
    return items.some(item => item.book.id === bookId)
  }

  return (
    <CartContext.Provider
      value={{
        items,
        itemCount,
        total,
        addToCart,
        removeFromCart,
        updateQuantity,
        addGiftRecipient,
        removeGiftRecipient,
        clearCart,
        isInCart
      }}
    >
      {children}
    </CartContext.Provider>
  )
}''')

    # Components
    create_file('src/components/Layout.tsx', '''import React from 'react'
import { Box, Container } from '@mui/material'
import Header from './Header'
import Footer from './Footer'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header />
      <Box component="main" sx={{ flex: 1, py: 4 }}>
        <Container maxWidth="lg">
          {children}
        </Container>
      </Box>
      <Footer />
    </Box>
  )
}

export default Layout''')

    create_file('src/components/Header.tsx', '''import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Badge,
  Menu,
  MenuItem,
  Box,
  Avatar,
  Divider,
  useTheme,
  useMediaQuery
} from '@mui/material'
import {
  ShoppingCart,
  Brightness4,
  Brightness7,
  Language,
  AccountCircle,
  Notifications,
  AdminPanelSettings,
  Logout
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/context/AuthContext'
import { useCart } from '@/context/CartContext'
import { useTheme as useAppTheme } from '@/context/ThemeContext'
import { useLanguage } from '@/context/LanguageContext'
import { useNotification } from '@/context/NotificationContext'

const Header: React.FC = () => {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { profile, signOut } = useAuth()
  const { itemCount } = useCart()
  const { theme: appTheme, toggleTheme } = useAppTheme()
  const { language, changeLanguage } = useLanguage()
  const { unreadCount } = useNotification()

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [langAnchorEl, setLangAnchorEl] = useState<null | HTMLElement>(null)

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleProfileMenuClose = () => {
    setAnchorEl(null)
  }

  const handleLanguageMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setLangAnchorEl(event.currentTarget)
  }

  const handleLanguageMenuClose = () => {
    setLangAnchorEl(null)
  }

  const handleSignOut = async () => {
    await signOut()
    navigate('/')
    handleProfileMenuClose()
  }

  const handleLanguageChange = (lang: string) => {
    changeLanguage(lang)
    handleLanguageMenuClose()
  }

  return (
    <AppBar position="sticky">
      <Toolbar>
        <Typography
          variant="h6"
          component={Link}
          to="/"
          sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}
        >
          {t('home')}
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Button color="inherit" component={Link} to="/books">
            {t('books')}
          </Button>
          <Button color="inherit" component={Link} to="/courses">
            {t('courses')}
          </Button>

          <IconButton color="inherit" onClick={toggleTheme}>
            {appTheme === 'dark' ? <Brightness7 /> : <Brightness4 />}
          </IconButton>

          <IconButton color="inherit" onClick={handleLanguageMenuOpen}>
            <Language />
          </IconButton>

          <Menu
            anchorEl={langAnchorEl}
            open={Boolean(langAnchorEl)}
            onClose={handleLanguageMenuClose}
          >
            <MenuItem
              onClick={() => handleLanguageChange('en')}
              selected={language === 'en'}
            >
              English
            </MenuItem>
            <MenuItem
              onClick={() => handleLanguageChange('ar')}
              selected={language === 'ar'}
            >
              العربية
            </MenuItem>
          </Menu>

          <IconButton color="inherit" component={Link} to="/cart">
            <Badge badgeContent={itemCount} color="secondary">
              <ShoppingCart />
            </Badge>
          </IconButton>

          {profile ? (
            <>
              <IconButton color="inherit" component={Link} to="/notifications">
                <Badge badgeContent={unreadCount} color="secondary">
                  <Notifications />
                </Badge>
              </IconButton>

              <IconButton
                edge="end"
                onClick={handleProfileMenuOpen}
                color="inherit"
              >
                {profile.avatar_url ? (
                  <Avatar src={profile.avatar_url} sx={{ width: 32, height: 32 }} />
                ) : (
                  <AccountCircle />
                )}
              </IconButton>

              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleProfileMenuClose}
              >
                <MenuItem
                  onClick={() => {
                    navigate(`/profile/${profile.id}`)
                    handleProfileMenuClose()
                  }}
                >
                  {t('profile')}
                </MenuItem>
                {profile.is_admin && (
                  <MenuItem
                    onClick={() => {
                      navigate('/admin')
                      handleProfileMenuClose()
                    }}
                  >
                    <AdminPanelSettings sx={{ mr: 1 }} />
                    {t('admin')}
                  </MenuItem>
                )}
                <Divider />
                <MenuItem onClick={handleSignOut}>
                  <Logout sx={{ mr: 1 }} />
                  {t('logout')}
                </MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button color="inherit" component={Link} to="/login">
                {t('login')}
              </Button>
              {!isMobile && (
                <Button
                  color="inherit"
                  component={Link}
                  to="/register"
                  variant="outlined"
                  sx={{ ml: 1 }}
                >
                  {t('register')}
                </Button>
              )}
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Header''')

    create_file('src/components/Footer.tsx', '''import React from 'react'
import { Box, Container, Typography, Link, Grid } from '@mui/material'
import { useTranslation } from 'react-i18next'

const Footer: React.FC = () => {
  const { t } = useTranslation()
  const currentYear = new Date().getFullYear()

  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) =>
          theme.palette.mode === 'light'
            ? theme.palette.grey[200]
            : theme.palette.grey[800],
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              React Academy
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Your journey to knowledge starts here.
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Links
            </Typography>
            <Link href="#" color="inherit" display="block">
              About Us
            </Link>
            <Link href="#" color="inherit" display="block">
              Contact
            </Link>
            <Link href="#" color="inherit" display="block">
              Terms of Service
            </Link>
            <Link href="#" color="inherit" display="block">
              Privacy Policy
            </Link>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Follow Us
            </Typography>
            <Link href="#" color="inherit" display="block">
              Facebook
            </Link>
            <Link href="#" color="inherit" display="block">
              Twitter
            </Link>
            <Link href="#" color="inherit" display="block">
              LinkedIn
            </Link>
            <Link href="#" color="inherit" display="block">
              Instagram
            </Link>
          </Grid>
        </Grid>
        <Box mt={3}>
          <Typography variant="body2" color="text.secondary" align="center">
            © {currentYear} React Academy. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </Box>
  )
}

export default Footer''')

    # Create remaining components
    create_file('src/components/BookCard.tsx', '''import React from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Chip
} from '@mui/material'
import { ShoppingCart, CardGiftcard, Download } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Book } from '@/types'
import { useCart } from '@/context/CartContext'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'
import { booksApi } from '@/services/api/books'
import GiftModal from './GiftModal'

interface BookCardProps {
  book: Book
  owned?: boolean
}

const BookCard: React.FC<BookCardProps> = ({ book, owned = false }) => {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { addToCart } = useCart()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [giftModalOpen, setGiftModalOpen] = React.useState(false)
  const [isOwned, setIsOwned] = React.useState(owned)

  React.useEffect(() => {
    const checkOwnership = async () => {
      if (profile) {
        const owns = await booksApi.checkOwnership(book.id, profile.id)
        setIsOwned(owns)
      }
    }
    checkOwnership()
  }, [book.id, profile])

  const handleAddToCart = () => {
    addToCart(book)
    showNotification(t('bookAddedToCart'), 'success')
  }

  const handleDownload = () => {
    window.open(book.file_url, '_blank')
  }

  return (
    <>
      <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <CardMedia
          component="img"
          height="300"
          image={book.cover_url}
          alt={book.title}
          sx={{ cursor: 'pointer' }}
          onClick={() => navigate(`/books/${book.id}`)}
        />
        <CardContent sx={{ flexGrow: 1 }}>
          <Typography gutterBottom variant="h6" component="h2">
            {book.title}
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              display: '-webkit-box',
              WebkitLineClamp: 3,
              WebkitBoxOrient: 'vertical',
            }}
          >
            {book.description}
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Chip
              label={`$${book.price}`}
              color="primary"
              size="small"
              sx={{ fontWeight: 'bold' }}
            />
          </Box>
        </CardContent>
        <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
          {isOwned ? (
            <Button
              fullWidth
              variant="contained"
              startIcon={<Download />}
              onClick={handleDownload}
            >
              {t('download')}
            </Button>
          ) : (
            <>
              <Button
                variant="contained"
                startIcon={<ShoppingCart />}
                onClick={handleAddToCart}
                sx={{ flex: 1, mr: 1 }}
              >
                {t('addToCart')}
              </Button>
              <Button
                variant="outlined"
                startIcon={<CardGiftcard />}
                onClick={() => setGiftModalOpen(true)}
              >
                {t('gift')}
              </Button>
            </>
          )}
        </CardActions>
      </Card>

      <GiftModal
        open={giftModalOpen}
        onClose={() => setGiftModalOpen(false)}
        book={book}
      />
    </>
  )
}

export default BookCard''')

    create_file('src/components/CourseCard.tsx', '''import React from 'react'
import {
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  LinearProgress,
  Chip
} from '@mui/material'
import {
  Telegram,
  School,
  EmojiEvents,
  CalendarToday
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
import { Course, CourseEnrollment } from '@/types'
import { coursesApi } from '@/services/api/courses'
import { useAuth } from '@/context/AuthContext'

interface CourseCardProps {
  course: Course
  enrollment?: CourseEnrollment | null
}

const CourseCard: React.FC<CourseCardProps> = ({ course, enrollment: initialEnrollment }) => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const [enrollment, setEnrollment] = React.useState(initialEnrollment)

  React.useEffect(() => {
    const checkEnrollment = async () => {
      if (profile && !initialEnrollment) {
        const enrolled = await coursesApi.checkEnrollment(course.id, profile.id)
        setEnrollment(enrolled)
      }
    }
    checkEnrollment()
  }, [course.id, profile, initialEnrollment])

  const getStatusColor = () => {
    if (!enrollment) return 'default'
    switch (enrollment.status) {
      case 'completed':
        return 'success'
      case 'in_progress':
        return 'primary'
      default:
        return 'default'
    }
  }

  const getStatusText = () => {
    if (!enrollment) return t('enrollNow')
    switch (enrollment.status) {
      case 'completed':
        return t('completed')
      case 'in_progress':
        return t('inProgress')
      default:
        return t('notStarted')
    }
  }

  const handleEnrollClick = () => {
    window.open('https://t.me/your_admin_contact', '_blank')
  }

  const handleTelegramClick = () => {
    if (course.telegram_link) {
      window.open(course.telegram_link, '_blank')
    }
  }

  const handleCertificateDownload = () => {
    if (enrollment?.certificate_url) {
      window.open(enrollment.certificate_url, '_blank')
    }
  }

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardMedia
        component="img"
        height="200"
        image={course.image_url}
        alt={course.title}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography gutterBottom variant="h6" component="h2">
          {course.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          {course.description}
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <CalendarToday sx={{ fontSize: 16, mr: 1 }} />
            <Typography variant="caption">
              {format(new Date(course.start_date), 'MMM dd, yyyy')} -{' '}
              {format(new Date(course.end_date), 'MMM dd, yyyy')}
            </Typography>
          </Box>

          {enrollment && (
            <>
              <Chip
                label={getStatusText()}
                color={getStatusColor()}
                size="small"
                sx={{ mb: 1 }}
              />
              <LinearProgress
                variant="determinate"
                value={enrollment.progress}
                sx={{ height: 8, borderRadius: 4 }}
              />
              <Typography variant="caption" color="text.secondary">
                {enrollment.progress}% {t('completed')}
              </Typography>
            </>
          )}
        </Box>
      </CardContent>

      <CardActions>
        {!enrollment ? (
          <Button
            fullWidth
            variant="contained"
            startIcon={<School />}
            onClick={handleEnrollClick}
          >
            {t('enrollNow')}
          </Button>
        ) : enrollment.status === 'completed' && enrollment.certificate_url ? (
          <Button
            fullWidth
            variant="contained"
            color="success"
            startIcon={<EmojiEvents />}
            onClick={handleCertificateDownload}
          >
            {t('downloadCertificate')}
          </Button>
        ) : course.telegram_link ? (
          <Button
            fullWidth
            variant="contained"
            startIcon={<Telegram />}
            onClick={handleTelegramClick}
          >
            {t('joinTelegram')}
          </Button>
        ) : null}
      </CardActions>
    </Card>
  )
}

export default CourseCard''')

    create_file('src/components/GiftModal.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Autocomplete,
  Box,
  Typography,
  Alert
} from '@mui/material'
import { useTranslation } from 'react-i18next'
import { Book, User } from '@/types'
import { usersApi } from '@/services/api/users'
import { booksApi } from '@/services/api/books'
import { notificationsApi } from '@/services/api/notifications'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

interface GiftModalProps {
  open: boolean
  onClose: () => void
  book: Book
}

const GiftModal: React.FC<GiftModalProps> = ({ open, onClose, book }) => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [users, setUsers] = useState<User[]>([])
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const allUsers = await usersApi.getAllUsers()
        // Filter out current user and banned users
        const filteredUsers = allUsers.filter(
          u => u.id !== profile?.id && !u.is_banned
        )
        setUsers(filteredUsers)
      } catch (err) {
        console.error('Error fetching users:', err)
      }
    }

    if (open) {
      fetchUsers()
    }
  }, [open, profile])

  const handleSend = async () => {
    if (!selectedUser || !profile) return

    setLoading(true)
    setError(null)

    try {
      // Check if recipient already owns the book
      const alreadyOwns = await booksApi.checkOwnership(book.id, selectedUser.id)
      if (alreadyOwns) {
        setError('This user already owns this book')
        setLoading(false)
        return
      }

      // Check if blocked
      const isBlocked = await usersApi.isBlocked(selectedUser.id, profile.id)
      if (isBlocked) {
        setError('You cannot send gifts to this user')
        setLoading(false)
        return
      }

      // Send gift
      await booksApi.gift(book.id, selectedUser.id, message, profile.id)

      // Send notification
      await notificationsApi.notifyGiftReceived(
        selectedUser.id,
        profile.id,
        book.title
      )

      showNotification(t('giftSent'), 'success')
      onClose()
      setSelectedUser(null)
      setMessage('')
    } catch (err: any) {
      setError(err.message || 'Failed to send gift')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{t('gift')} - {book.title}</DialogTitle>
      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box sx={{ mt: 2 }}>
          <Autocomplete
            options={users}
            getOptionLabel={(option) => option.username}
            value={selectedUser}
            onChange={(_, value) => setSelectedUser(value)}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Select recipient"
                required
                fullWidth
              />
            )}
            renderOption={(props, option) => (
              <Box component="li" {...props}>
                <Typography>{option.username}</Typography>
              </Box>
            )}
          />

          <TextField
            label="Gift message (optional)"
            multiline
            rows={4}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            fullWidth
            sx={{ mt: 2 }}
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>{t('cancel')}</Button>
        <Button
          onClick={handleSend}
          variant="contained"
          disabled={!selectedUser || loading}
        >
          {loading ? 'Sending...' : 'Send Gift'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default GiftModal''')

    create_file('src/components/ReviewSection.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Rating,
  TextField,
  Button,
  Paper,
  Avatar,
  IconButton,
  Divider,
  Stack,
  Collapse
} from '@mui/material'
import {
  ThumbUp,
  ThumbUpOutlined,
  Reply,
  Edit,
  Delete,
  Send
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
import { Review, ReviewReply } from '@/types'
import { reviewsApi } from '@/services/api/reviews'
import { notificationsApi } from '@/services/api/notifications'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

interface ReviewSectionProps {
  bookId: string
}

const ReviewSection: React.FC<ReviewSectionProps> = ({ bookId }) => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [reviews, setReviews] = useState<Review[]>([])
  const [userReview, setUserReview] = useState<Review | null>(null)
  const [rating, setRating] = useState(0)
  const [reviewContent, setReviewContent] = useState('')
  const [editingReview, setEditingReview] = useState<string | null>(null)
  const [replyingTo, setReplyingTo] = useState<string | null>(null)
  const [replyContent, setReplyContent] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchReviews()
  }, [bookId])

  const fetchReviews = async () => {
    try {
      const data = await reviewsApi.getBookReviews(bookId)
      setReviews(data)
      
      // Find user's review
      if (profile) {
        const userRev = data.find(r => r.user_id === profile.id)
        if (userRev) {
          setUserReview(userRev)
          setRating(userRev.rating)
          setReviewContent(userRev.content || '')
        }
      }
    } catch (error) {
      console.error('Error fetching reviews:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitReview = async () => {
    if (!profile || rating === 0) return

    try {
      if (userReview) {
        // Update existing review
        await reviewsApi.updateReview(userReview.id, {
          rating,
          content: reviewContent
        })
      } else {
        // Create new review
        await reviewsApi.createReview({
          book_id: bookId,
          user_id: profile.id,
          rating,
          content: reviewContent
        })
      }
      
      showNotification(t('reviewPosted'), 'success')
      await fetchReviews()
    } catch (error) {
      showNotification('Failed to post review', 'error')
    }
  }

  const handleDeleteReview = async (reviewId: string) => {
    try {
      await reviewsApi.deleteReview(reviewId)
      showNotification('Review deleted', 'success')
      await fetchReviews()
    } catch (error) {
      showNotification('Failed to delete review', 'error')
    }
  }

  const handleLikeReview = async (review: Review) => {
    if (!profile) return

    try {
      if (review.user_has_liked) {
        await reviewsApi.unlikeReview(review.id, profile.id)
      } else {
        await reviewsApi.likeReview(review.id, profile.id)
        
        // Notify review author
        if (review.user_id !== profile.id) {
          await notificationsApi.notifyReviewLike(
            review.user_id,
            profile.id,
            profile.username
          )
        }
      }
      await fetchReviews()
    } catch (error) {
      console.error('Error liking review:', error)
    }
  }

  const handleSubmitReply = async (reviewId: string) => {
    if (!profile || !replyContent.trim()) return

    try {
      await reviewsApi.createReply({
        review_id: reviewId,
        user_id: profile.id,
        content: replyContent
      })

      // Notify review author
      const review = reviews.find(r => r.id === reviewId)
      if (review && review.user_id !== profile.id) {
        await notificationsApi.notifyReviewReply(
          review.user_id,
          profile.id,
          profile.username
        )
      }

      setReplyContent('')
      setReplyingTo(null)
      showNotification('Reply posted', 'success')
      await fetchReviews()
    } catch (error) {
      showNotification('Failed to post reply', 'error')
    }
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t('reviews')}
      </Typography>

      {/* Write/Edit Review Section */}
      {profile && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            {userReview ? 'Edit your review' : t('writeReview')}
          </Typography>
          <Box sx={{ mb: 2 }}>
            <Typography component="legend">{t('rating')}</Typography>
            <Rating
              value={rating}
              onChange={(_, value) => setRating(value || 0)}
              size="large"
            />
          </Box>
          <TextField
            fullWidth
            multiline
            rows={4}
            value={reviewContent}
            onChange={(e) => setReviewContent(e.target.value)}
            placeholder="Share your thoughts about this book..."
            sx={{ mb: 2 }}
          />
          <Button
            variant="contained"
            onClick={handleSubmitReview}
            disabled={rating === 0}
          >
            {userReview ? 'Update Review' : 'Post Review'}
          </Button>
        </Paper>
      )}

      {/* Reviews List */}
      <Stack spacing={2}>
        {reviews.map((review) => (
          <Paper key={review.id} sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 1 }}>
              <Avatar
                src={review.user?.avatar_url}
                sx={{ mr: 2 }}
              >
                {review.user?.username[0].toUpperCase()}
              </Avatar>
              <Box sx={{ flex: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {review.user?.username}
                  </Typography>
                  <Rating value={review.rating} readOnly size="small" />
                  <Typography variant="caption" color="text.secondary">
                    {format(new Date(review.created_at), 'MMM dd, yyyy')}
                  </Typography>
                </Box>

                {editingReview === review.id ? (
                  <Box sx={{ mt: 1 }}>
                    <TextField
                      fullWidth
                      multiline
                      rows={3}
                      value={reviewContent}
                      onChange={(e) => setReviewContent(e.target.value)}
                      sx={{ mb: 1 }}
                    />
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Button
                        size="small"
                        variant="contained"
                        onClick={handleSubmitReview}
                      >
                        Save
                      </Button>
                      <Button
                        size="small"
                        onClick={() => {
                          setEditingReview(null)
                          setReviewContent(userReview?.content || '')
                        }}
                      >
                        Cancel
                      </Button>
                    </Box>
                  </Box>
                ) : (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    {review.content}
                  </Typography>
                )}

                {/* Review Actions */}
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1, gap: 1 }}>
                  <IconButton
                    size="small"
                    onClick={() => handleLikeReview(review)}
                  >
                    {review.user_has_liked ? <ThumbUp /> : <ThumbUpOutlined />}
                  </IconButton>
                  <Typography variant="caption">
                    {review.likes_count}
                  </Typography>
                  
                  {profile && (
                    <IconButton
                      size="small"
                      onClick={() => setReplyingTo(review.id)}
                    >
                      <Reply />
                    </IconButton>
                  )}

                  {profile?.id === review.user_id && (
                    <>
                      <IconButton
                        size="small"
                        onClick={() => {
                          setEditingReview(review.id)
                          setReviewContent(review.content || '')
                        }}
                      >
                        <Edit />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleDeleteReview(review.id)}
                      >
                        <Delete />
                      </IconButton>
                    </>
                  )}
                </Box>

                {/* Reply Section */}
                <Collapse in={replyingTo === review.id}>
                  <Box sx={{ mt: 2, ml: 4 }}>
                    <TextField
                      fullWidth
                      size="small"
                      placeholder="Write a reply..."
                      value={replyContent}
                      onChange={(e) => setReplyContent(e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault()
                          handleSubmitReply(review.id)
                        }
                      }}
                      InputProps={{
                        endAdornment: (
                          <IconButton
                            size="small"
                            onClick={() => handleSubmitReply(review.id)}
                            disabled={!replyContent.trim()}
                          >
                            <Send />
                          </IconButton>
                        )
                      }}
                    />
                  </Box>
                </Collapse>

                {/* Replies */}
                {review.replies && review.replies.length > 0 && (
                  <Box sx={{ mt: 2, ml: 4 }}>
                    <Divider sx={{ mb: 1 }} />
                    {review.replies.map((reply) => (
                      <Box key={reply.id} sx={{ mb: 1 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Avatar
                            src={reply.user?.avatar_url}
                            sx={{ width: 24, height: 24 }}
                          >
                            {reply.user?.username[0].toUpperCase()}
                          </Avatar>
                          <Typography variant="subtitle2">
                            {reply.user?.username}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {format(new Date(reply.created_at), 'MMM dd, yyyy')}
                          </Typography>
                        </Box>
                        <Typography variant="body2" sx={{ ml: 4 }}>
                          {reply.content}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                )}
              </Box>
            </Box>
          </Paper>
        ))}
      </Stack>

      {reviews.length === 0 && !loading && (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography color="text.secondary">
            No reviews yet. Be the first to review this book!
          </Typography>
        </Paper>
      )}
    </Box>
  )
}

export default ReviewSection''')

    # Create pages
    create_file('src/pages/Home.tsx', '''import React from 'react'
import { Link as RouterLink } from 'react-router-dom'
import {
  Box,
  Typography,
  Button,
  Grid,
  Container,
  Paper,
  useTheme
} from '@mui/material'
import {
  MenuBook,
  School,
  PersonAdd,
  Login as LoginIcon
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/context/AuthContext'

const HomePage: React.FC = () => {
  const { t } = useTranslation()
  const theme = useTheme()
  const { profile } = useAuth()

  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          minHeight: '80vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
          py: 8,
        }}
      >
        <Typography
          component="h1"
          variant="h2"
          gutterBottom
          sx={{
            fontWeight: 700,
            background: `linear-gradient(45deg, ${theme.palette.primary.main} 30%, ${theme.palette.secondary.main} 90%)`,
            backgroundClip: 'text',
            textFillColor: 'transparent',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          React Academy
        </Typography>

        <Typography
          variant="h5"
          color="text.secondary"
          paragraph
          sx={{ maxWidth: 600, mb: 4 }}
        >
          Your journey to knowledge starts here. Explore our collection of digital books
          and courses designed to help you grow.
        </Typography>

        <Grid container spacing={3} justifyContent="center" sx={{ mb: 6 }}>
          <Grid item>
            <Button
              component={RouterLink}
              to="/books"
              variant="contained"
              size="large"
              startIcon={<MenuBook />}
              sx={{ px: 4, py: 1.5 }}
            >
              {t('books')}
            </Button>
          </Grid>
          <Grid item>
            <Button
              component={RouterLink}
              to="/courses"
              variant="outlined"
              size="large"
              startIcon={<School />}
              sx={{ px: 4, py: 1.5 }}
            >
              {t('courses')}
            </Button>
          </Grid>
          {!profile && (
            <>
              <Grid item>
                <Button
                  component={RouterLink}
                  to="/register"
                  variant="contained"
                  color="secondary"
                  size="large"
                  startIcon={<PersonAdd />}
                  sx={{ px: 4, py: 1.5 }}
                >
                  {t('register')}
                </Button>
              </Grid>
              <Grid item>
                <Button
                  component={RouterLink}
                  to="/login"
                  variant="text"
                  size="large"
                  startIcon={<LoginIcon />}
                  sx={{ px: 4, py: 1.5 }}
                >
                  {t('login')}
                </Button>
              </Grid>
            </>
          )}
        </Grid>

        <Grid container spacing={4} sx={{ mt: 4 }}>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={0}
              sx={{
                p: 3,
                height: '100%',
                backgroundColor: theme.palette.background.default,
              }}
            >
              <MenuBook sx={{ fontSize: 48, color: theme.palette.primary.main, mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Digital Library
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Access a curated collection of books on various topics. Purchase once,
                download forever.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={0}
              sx={{
                p: 3,
                height: '100%',
                backgroundColor: theme.palette.background.default,
              }}
            >
              <School sx={{ fontSize: 48, color: theme.palette.secondary.main, mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Expert-Led Courses
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Join structured courses with expert instructors. Track your progress
                and earn certificates.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={0}
              sx={{
                p: 3,
                height: '100%',
                backgroundColor: theme.palette.background.default,
              }}
            >
              <PersonAdd sx={{ fontSize: 48, color: theme.palette.success.main, mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Community Learning
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Connect with fellow learners, share reviews, and gift books to
                friends and colleagues.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  )
}

export default HomePage''')

    create_file('src/pages/Books.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  TextField,
  InputAdornment,
  Typography,
  CircularProgress,
  Paper
} from '@mui/material'
import { Search } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Book } from '@/types'
import { booksApi } from '@/services/api/books'
import BookCard from '@/components/BookCard'

const BooksPage: React.FC = () => {
  const { t } = useTranslation()
  const [books, setBooks] = useState<Book[]>([])
  const [filteredBooks, setFilteredBooks] = useState<Book[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBooks()
  }, [])

  useEffect(() => {
    if (searchQuery) {
      const filtered = books.filter(
        book =>
          book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          book.description.toLowerCase().includes(searchQuery.toLowerCase())
      )
      setFilteredBooks(filtered)
    } else {
      setFilteredBooks(books)
    }
  }, [searchQuery, books])

  const fetchBooks = async () => {
    try {
      const data = await booksApi.getAll()
      setBooks(data)
      setFilteredBooks(data)
    } catch (error) {
      console.error('Error fetching books:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('books')}
      </Typography>

      <Paper sx={{ p: 2, mb: 4 }}>
        <TextField
          fullWidth
          placeholder={t('search')}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
      </Paper>

      <Grid container spacing={3}>
        {filteredBooks.map((book) => (
          <Grid item key={book.id} xs={12} sm={6} md={4} lg={3}>
            <BookCard book={book} />
          </Grid>
        ))}
      </Grid>

      {filteredBooks.length === 0 && (
        <Box textAlign="center" py={8}>
          <Typography variant="h6" color="text.secondary">
            {searchQuery ? 'No books found matching your search.' : 'No books available.'}
          </Typography>
        </Box>
      )}
    </Box>
  )
}

export default BooksPage''')

    create_file('src/pages/BookDetail.tsx', '''import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Grid,
  Typography,
  Button,
  Paper,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  CircularProgress,
  Divider,
  IconButton
} from '@mui/material'
import {
  ShoppingCart,
  CardGiftcard,
  Download,
  ArrowBack,
  Block
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
import { Book, BookOwnership } from '@/types'
import { booksApi } from '@/services/api/books'
import { usersApi } from '@/services/api/users'
import { useAuth } from '@/context/AuthContext'
import { useCart } from '@/context/CartContext'
import { useNotification } from '@/context/NotificationContext'
import GiftModal from '@/components/GiftModal'
import ReviewSection from '@/components/ReviewSection'

const BookDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { addToCart } = useCart()
  const { showNotification } = useNotification()
  
  const [book, setBook] = useState<Book | null>(null)
  const [owners, setOwners] = useState<BookOwnership[]>([])
  const [isOwned, setIsOwned] = useState(false)
  const [loading, setLoading] = useState(true)
  const [giftModalOpen, setGiftModalOpen] = useState(false)
  const [blockedUsers, setBlockedUsers] = useState<string[]>([])

  useEffect(() => {
    if (id) {
      fetchBookDetails()
    }
  }, [id])

  useEffect(() => {
    if (profile) {
      fetchBlockedUsers()
    }
  }, [profile])

  const fetchBookDetails = async () => {
    try {
      const [bookData, ownersData] = await Promise.all([
        booksApi.getById(id!),
        booksApi.getOwners(id!)
      ])
      
      setBook(bookData)
      setOwners(ownersData)
      
      if (profile) {
        const owns = await booksApi.checkOwnership(id!, profile.id)
        setIsOwned(owns)
      }
    } catch (error) {
      console.error('Error fetching book details:', error)
      navigate('/404')
    } finally {
      setLoading(false)
    }
  }

  const fetchBlockedUsers = async () => {
    if (!profile) return
    try {
      const blocked = await usersApi.getBlockedUsers(profile.id)
      setBlockedUsers(blocked.map(b => b.blocked_id))
    } catch (error) {
      console.error('Error fetching blocked users:', error)
    }
  }

  const handleAddToCart = () => {
    if (book) {
      addToCart(book)
      showNotification(t('bookAddedToCart'), 'success')
    }
  }

  const handleDownload = () => {
    if (book) {
      window.open(book.file_url, '_blank')
    }
  }

  const handleBlockUser = async (userId: string) => {
    if (!profile) return
    
    try {
      const isBlocked = blockedUsers.includes(userId)
      if (isBlocked) {
        await usersApi.unblockUser(profile.id, userId)
        setBlockedUsers(prev => prev.filter(id => id !== userId))
        showNotification('User unblocked', 'success')
      } else {
        await usersApi.blockUser(profile.id, userId)
        setBlockedUsers(prev => [...prev, userId])
        showNotification('User blocked', 'success')
      }
    } catch (error) {
      showNotification('Failed to update block status', 'error')
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  if (!book) {
    return null
  }

  return (
    <Box>
      <Button
        startIcon={<ArrowBack />}
        onClick={() => navigate('/books')}
        sx={{ mb: 2 }}
      >
        Back to Books
      </Button>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <img
              src={book.cover_url}
              alt={book.title}
              style={{ width: '100%', height: 'auto', borderRadius: 8 }}
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Typography variant="h4" gutterBottom>
            {book.title}
          </Typography>

          <Box sx={{ mb: 3 }}>
            <Chip
              label={`$${book.price}`}
              color="primary"
              size="large"
              sx={{ fontWeight: 'bold', fontSize: '1.2rem' }}
            />
          </Box>

          <Typography variant="body1" paragraph>
            {book.description}
          </Typography>

          <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
            {isOwned ? (
              <Button
                variant="contained"
                size="large"
                startIcon={<Download />}
                onClick={handleDownload}
                fullWidth
              >
                {t('download')}
              </Button>
            ) : (
              <>
                <Button
                  variant="contained"
                  size="large"
                  startIcon={<ShoppingCart />}
                  onClick={handleAddToCart}
                  sx={{ flex: 1 }}
                >
                  {t('addToCart')}
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<CardGiftcard />}
                  onClick={() => setGiftModalOpen(true)}
                >
                  {t('gift')}
                </Button>
              </>
            )}
          </Box>

          {/* Who owns this book */}
          <Paper sx={{ p: 3, mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              {t('whoOwnsThis')}
            </Typography>
            <List>
              {owners.map((ownership) => (
                <ListItem
                  key={ownership.id}
                  secondaryAction={
                    profile && profile.id !== ownership.user_id && (
                      <IconButton
                        edge="end"
                        onClick={() => handleBlockUser(ownership.user_id)}
                        color={blockedUsers.includes(ownership.user_id) ? 'error' : 'default'}
                      >
                        <Block />
                      </IconButton>
                    )
                  }
                >
                  <ListItemAvatar>
                    <Avatar
                      src={ownership.user?.avatar_url}
                      onClick={() => navigate(`/profile/${ownership.user_id}`)}
                      sx={{ cursor: 'pointer' }}
                    >
                      {ownership.user?.username[0].toUpperCase()}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={ownership.user?.username}
                    secondary={
                      <>
                        {format(new Date(ownership.purchase_date), 'MMM dd, yyyy')}
                        {ownership.is_gift && ' • Received as gift'}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
            {owners.length === 0 && (
              <Typography color="text.secondary">
                No one owns this book yet.
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>

      <Divider sx={{ my: 4 }} />

      {/* Reviews Section */}
      <ReviewSection bookId={book.id} />

      {/* Gift Modal */}
      <GiftModal
        open={giftModalOpen}
        onClose={() => setGiftModalOpen(false)}
        book={book}
      />
    </Box>
  )
}

export default BookDetailPage''')

    create_file('src/pages/Courses.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Typography,
  CircularProgress
} from '@mui/material'
import { useTranslation } from 'react-i18next'
import { Course, CourseEnrollment } from '@/types'
import { coursesApi } from '@/services/api/courses'
import { useAuth } from '@/context/AuthContext'
import CourseCard from '@/components/CourseCard'

const CoursesPage: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const [courses, setCourses] = useState<Course[]>([])
  const [enrollments, setEnrollments] = useState<CourseEnrollment[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCourses()
  }, [profile])

  const fetchCourses = async () => {
    try {
      const coursesData = await coursesApi.getAll()
      setCourses(coursesData)

      if (profile) {
        const enrollmentsData = await coursesApi.getUserEnrollments(profile.id)
        setEnrollments(enrollmentsData)
      }
    } catch (error) {
      console.error('Error fetching courses:', error)
    } finally {
      setLoading(false)
    }
  }

  const getEnrollment = (courseId: string) => {
    return enrollments.find(e => e.course_id === courseId) || null
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('courses')}
      </Typography>

      <Grid container spacing={3}>
        {courses.map((course) => (
          <Grid item key={course.id} xs={12} md={6} lg={4}>
            <CourseCard
              course={course}
              enrollment={getEnrollment(course.id)}
            />
          </Grid>
        ))}
      </Grid>

      {courses.length === 0 && (
        <Box textAlign="center" py={8}>
          <Typography variant="h6" color="text.secondary">
            No courses available at the moment.
          </Typography>
        </Box>
      )}
    </Box>
  )
}

export default CoursesPage''')

    create_file('src/pages/Profile.tsx', '''import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Paper,
  Avatar,
  Button,
  Grid,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Switch,
  FormControlLabel,
  TextField,
  CircularProgress,
  Divider,
  Badge as MuiBadge
} from '@mui/material'
import {
  Edit,
  Delete,
  Download,
  Message,
  Block,
  CardGiftcard,
  School,
  MenuBook,
  EmojiEvents,
  Settings,
  Notifications
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
import { User, BookOwnership, CourseEnrollment, UserBadge, Certificate, Message as MessageType } from '@/types'
import { usersApi } from '@/services/api/users'
import { messagesApi } from '@/services/api/messages'
import { notificationsApi } from '@/services/api/notifications'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index, ...other }) => {
  return (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  )
}

const ProfilePage: React.FC = () => {
  const { userId } = useParams<{ userId?: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { profile: currentUser, updateProfile } = useAuth()
  const { showNotification } = useNotification()
  
  const [user, setUser] = useState<User | null>(null)
  const [tabValue, setTabValue] = useState(0)
  const [loading, setLoading] = useState(true)
  const [editingBio, setEditingBio] = useState(false)
  const [bio, setBio] = useState('')
  const [courseProgressPublic, setCourseProgressPublic] = useState(true)
  const [books, setBooks] = useState<BookOwnership[]>([])
  const [courses, setCourses] = useState<CourseEnrollment[]>([])
  const [badges, setBadges] = useState<UserBadge[]>([])
  const [certificates, setCertificates] = useState<Certificate[]>([])
  const [messages, setMessages] = useState<MessageType[]>([])
  const [giftHistory, setGiftHistory] = useState<BookOwnership[]>([])
  const [isBlocked, setIsBlocked] = useState(false)

  const isOwnProfile = !userId || userId === currentUser?.id
  const profileId = userId || currentUser?.id

  useEffect(() => {
    if (profileId) {
      fetchProfile()
      
      // Track profile visit
      if (!isOwnProfile && currentUser) {
        notificationsApi.notifyProfileVisit(profileId, currentUser.id, currentUser.username)
      }
    }
  }, [profileId])

  const fetchProfile = async () => {
    try {
      const userData = await usersApi.getProfile(profileId!)
      setUser(userData)
      setBio(userData.bio || '')
      setCourseProgressPublic(userData.course_progress_public)

      // Fetch related data
      const [
        booksData,
        coursesData,
        badgesData,
        certificatesData
      ] = await Promise.all([
        booksApi.getUserBooks(profileId!),
        coursesApi.getUserEnrollments(profileId!),
        usersApi.getUserBadges(profileId!),
        usersApi.getUserCertificates(profileId!)
      ])

      setBooks(booksData)
      setCourses(coursesData)
      setBadges(badgesData)
      setCertificates(certificatesData)

      // Fetch additional data for own profile
      if (isOwnProfile) {
        const messagesData = await messagesApi.getUserMessages(profileId!)
        setMessages(messagesData)
        
        // Filter gift history
        const giftsReceived = booksData.filter(b => b.is_gift)
        setGiftHistory(giftsReceived)
      }

      // Check if blocked
      if (currentUser && !isOwnProfile) {
        const blocked = await usersApi.isBlocked(currentUser.id, profileId!)
        setIsBlocked(blocked)
      }
    } catch (error) {
      console.error('Error fetching profile:', error)
      navigate('/404')
    } finally {
      setLoading(false)
    }
  }

  const handleSaveBio = async () => {
    try {
      await updateProfile({ bio })
      setEditingBio(false)
      showNotification('Bio updated', 'success')
    } catch (error) {
      showNotification('Failed to update bio', 'error')
    }
  }

  const handleToggleCoursePrivacy = async () => {
    try {
      await updateProfile({ course_progress_public: !courseProgressPublic })
      setCourseProgressPublic(!courseProgressPublic)
      showNotification('Privacy settings updated', 'success')
    } catch (error) {
      showNotification('Failed to update privacy settings', 'error')
    }
  }

  const handleBlockUser = async () => {
    if (!currentUser || !user) return
    
    try {
      if (isBlocked) {
        await usersApi.unblockUser(currentUser.id, user.id)
        setIsBlocked(false)
        showNotification('User unblocked', 'success')
      } else {
        await usersApi.blockUser(currentUser.id, user.id)
        setIsBlocked(true)
        showNotification('User blocked', 'success')
      }
    } catch (error) {
      showNotification('Failed to update block status', 'error')
    }
  }

  const handleDeleteAccount = async () => {
    if (!window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      return
    }

    try {
      await usersApi.deleteAccount(currentUser!.id)
      navigate('/')
    } catch (error) {
      showNotification('Failed to delete account', 'error')
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  if (!user) {
    return null
  }

  return (
    <Box>
      {/* Profile Header */}
      <Paper sx={{ p: 4, mb: 3 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item>
            <Avatar
              src={user.avatar_url}
              sx={{ width: 120, height: 120 }}
            >
              {user.username[0].toUpperCase()}
            </Avatar>
          </Grid>
          <Grid item xs>
            <Typography variant="h4">{user.username}</Typography>
            {user.is_admin && (
              <Chip label="Admin" color="primary" size="small" sx={{ mt: 1 }} />
            )}
            
            {/* Badges */}
            <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
              {badges.map((userBadge) => (
                <MuiBadge
                  key={userBadge.id}
                  overlap="circular"
                  anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                  badgeContent={
                    <Avatar
                      src={userBadge.badge?.icon_url}
                      sx={{ width: 24, height: 24 }}
                    />
                  }
                >
                  <Chip
                    label={userBadge.badge?.name}
                    size="small"
                    variant="outlined"
                  />
                </MuiBadge>
              ))}
            </Box>

            {/* Bio */}
            <Box sx={{ mt: 2 }}>
              {editingBio && isOwnProfile ? (
                <Box>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                    placeholder="Tell us about yourself..."
                    sx={{ mb: 1 }}
                  />
                  <Box>
                    <Button size="small" variant="contained" onClick={handleSaveBio}>
                      Save
                    </Button>
                    <Button
                      size="small"
                      onClick={() => {
                        setEditingBio(false)
                        setBio(user.bio || '')
                      }}
                      sx={{ ml: 1 }}
                    >
                      Cancel
                    </Button>
                  </Box>
                </Box>
              ) : (
                <Box>
                  <Typography variant="body1" color={user.bio ? 'inherit' : 'text.secondary'}>
                    {user.bio || 'No bio yet'}
                  </Typography>
                  {isOwnProfile && (
                    <IconButton size="small" onClick={() => setEditingBio(true)}>
                      <Edit />
                    </IconButton>
                  )}
                </Box>
              )}
            </Box>
          </Grid>
          {!isOwnProfile && currentUser && (
            <Grid item>
              <Button
                variant="contained"
                startIcon={<Message />}
                onClick={() => navigate(`/messages/${user.id}`)}
                disabled={isBlocked}
                sx={{ mb: 1 }}
              >
                Message
              </Button>
              <Button
                variant="outlined"
                startIcon={<Block />}
                onClick={handleBlockUser}
                color={isBlocked ? 'error' : 'inherit'}
                fullWidth
              >
                {isBlocked ? 'Unblock' : 'Block'}
              </Button>
            </Grid>
          )}
        </Grid>
      </Paper>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab label="Books" icon={<MenuBook />} />
          <Tab label="Courses" icon={<School />} />
          {isOwnProfile && (
            <>
              <Tab label="Messages" icon={<Message />} />
              <Tab label="Gift History" icon={<CardGiftcard />} />
              <Tab label="Settings" icon={<Settings />} />
            </>
          )}
        </Tabs>
      </Paper>

      {/* Tab Panels */}
      <TabPanel value={tabValue} index={0}>
        <Typography variant="h6" gutterBottom>
          Book Ownership ({books.length})
        </Typography>
        <Grid container spacing={2}>
          {books.map((ownership) => (
            <Grid item xs={12} sm={6} md={4} key={ownership.id}>
              <Paper sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'start' }}>
                  <img
                    src={ownership.book?.cover_url}
                    alt={ownership.book?.title}
                    style={{ width: 60, height: 80, borderRadius: 4, marginRight: 16 }}
                  />
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="subtitle1">{ownership.book?.title}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {format(new Date(ownership.purchase_date), 'MMM dd, yyyy')}
                    </Typography>
                    {ownership.is_gift && (
                      <Chip label="Gift" size="small" color="secondary" sx={{ ml: 1 }} />
                    )}
                    {isOwnProfile && (
                      <Box sx={{ mt: 1 }}>
                        <Button
                          size="small"
                          startIcon={<Download />}
                          onClick={() => window.open(ownership.book?.file_url, '_blank')}
                        >
                          Download
                        </Button>
                      </Box>
                    )}
                  </Box>
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Typography variant="h6" gutterBottom>
          Course History ({courses.length})
        </Typography>
        {(!isOwnProfile && !user.course_progress_public) ? (
          <Typography color="text.secondary">
            This user's course progress is private.
          </Typography>
        ) : (
          <List>
            {courses.map((enrollment) => (
              <ListItem key={enrollment.id}>
                <ListItemAvatar>
                  <Avatar src={enrollment.course?.image_url}>
                    <School />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={enrollment.course?.title}
                  secondary={
                    <>
                      Status: {enrollment.status} • Progress: {enrollment.progress}%
                      {enrollment.completed_at && (
                        <> • Completed: {format(new Date(enrollment.completed_at), 'MMM dd, yyyy')}</>
                      )}
                    </>
                  }
                />
                {enrollment.certificate_url && (
                  <ListItemSecondaryAction>
                    <IconButton
                      onClick={() => window.open(enrollment.certificate_url, '_blank')}
                    >
                      <EmojiEvents color="primary" />
                    </IconButton>
                  </ListItemSecondaryAction>
                )}
              </ListItem>
            ))}
          </List>
        )}
      </TabPanel>

      {isOwnProfile && (
        <>
          <TabPanel value={tabValue} index={2}>
            <Typography variant="h6" gutterBottom>
              Messages
            </Typography>
            <List>
              {messages.map((message) => (
                <ListItem key={message.id}>
                  <ListItemAvatar>
                    <Avatar src={
                      message.sender_id === currentUser?.id
                        ? message.recipient?.avatar_url
                        : message.sender?.avatar_url
                    }>
                      {(message.sender_id === currentUser?.id
                        ? message.recipient?.username[0]
                        : message.sender?.username[0]
                      )?.toUpperCase()}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      message.sender_id === currentUser?.id
                        ? `To: ${message.recipient?.username}`
                        : `From: ${message.sender?.username}`
                    }
                    secondary={
                      <>
                        {message.content.substring(0, 50)}...
                        <br />
                        {format(new Date(message.created_at), 'MMM dd, yyyy HH:mm')}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Typography variant="h6" gutterBottom>
              Gift History
            </Typography>
            <List>
              {giftHistory.map((gift) => (
                <ListItem key={gift.id}>
                  <ListItemAvatar>
                    <Avatar>
                      <CardGiftcard />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={gift.book?.title}
                    secondary={
                      <>
                        From: {gift.gifter?.username}
                        <br />
                        {gift.gift_message && `Message: ${gift.gift_message}`}
                        <br />
                        {format(new Date(gift.purchase_date), 'MMM dd, yyyy')}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            <Typography variant="h6" gutterBottom>
              Settings
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Privacy
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={courseProgressPublic}
                    onChange={handleToggleCoursePrivacy}
                  />
                }
                label="Show course progress publicly"
              />
            </Box>

            <Divider sx={{ my: 3 }} />

            <Box>
              <Typography variant="subtitle1" gutterBottom color="error">
                Danger Zone
              </Typography>
              <Button
                variant="outlined"
                color="error"
                startIcon={<Delete />}
                onClick={handleDeleteAccount}
              >
                Delete Account
              </Button>
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                This will permanently delete your account and all associated data.
              </Typography>
            </Box>
          </TabPanel>
        </>
      )}
    </Box>
  )
}

export default ProfilePage''')

    create_file('src/pages/Cart.tsx', '''import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Button,
  Divider,
  TextField,
  Avatar
} from '@mui/material'
import {
  Delete,
  Add,
  Remove,
  ShoppingCartCheckout,
  ArrowBack
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { useCart } from '@/context/CartContext'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'
import { paymobService } from '@/services/paymob'
import { supabase } from '@/services/supabase'

const CartPage: React.FC = () => {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { items, itemCount, total, removeFromCart, updateQuantity, clearCart } = useCart()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [loading, setLoading] = useState(false)

  const handleCheckout = async () => {
    if (!profile) {
      showNotification('Please login to checkout', 'warning')
      navigate('/login')
      return
    }

    if (!profile.email_verified) {
      showNotification('Please verify your email before making purchases', 'warning')
      return
    }

    setLoading(true)
    try {
      // Create transaction items
      const transactionItems = items.flatMap(item => {
        const baseItem = {
          book_id: item.book.id,
          quantity: 1,
          price: item.book.price,
          is_gift: false
        }

        // Add items for purchases
        const purchaseItems = Array(item.quantity - (item.recipients?.length || 0))
          .fill(null)
          .map(() => ({ ...baseItem }))

        // Add items for gifts
        const giftItems = (item.recipients || []).map(recipient => ({
          ...baseItem,
          is_gift: true,
          recipient_id: recipient.userId,
          gift_message: recipient.message
        }))

        return [...purchaseItems, ...giftItems]
      })

      // Create transaction record
      const { data: transaction, error: transactionError } = await supabase
        .from('transactions')
        .insert({
          user_id: profile.id,
          amount: total,
          currency: 'USD',
          status: 'pending',
          items: transactionItems
        })
        .select()
        .single()

      if (transactionError) throw transactionError

      // Initialize Paymob checkout
      const checkoutUrl = await paymobService.initiateCheckout(
        total,
        transactionItems,
        profile.email,
        profile.id
      )

      // Clear cart and redirect to payment
      clearCart()
      window.location.href = checkoutUrl
    } catch (error) {
      console.error('Checkout error:', error)
      showNotification('Failed to initialize checkout', 'error')
    } finally {
      setLoading(false)
    }
  }

  if (items.length === 0) {
    return (
      <Box textAlign="center" py={8}>
        <Typography variant="h5" gutterBottom>
          {t('emptyCart')}
        </Typography>
        <Button
          variant="contained"
          startIcon={<ArrowBack />}
          onClick={() => navigate('/books')}
          sx={{ mt: 2 }}
        >
          Continue Shopping
        </Button>
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('cart')} ({itemCount} items)
      </Typography>

      <Paper sx={{ p: 3 }}>
        <List>
          {items.map((item, index) => (
            <React.Fragment key={item.book.id}>
              {index > 0 && <Divider />}
              <ListItem sx={{ py: 2 }}>
                <ListItemAvatar>
                  <Avatar
                    src={item.book.cover_url}
                    variant="rounded"
                    sx={{ width: 60, height: 80 }}
                  />
                </ListItemAvatar>
                <ListItemText
                  primary={item.book.title}
                  secondary={
                    <>
                      ${item.book.price} each
                      {item.recipients && item.recipients.length > 0 && (
                        <Typography variant="caption" display="block">
                          {item.recipients.length} as gifts
                        </Typography>
                      )}
                    </>
                  }
                  sx={{ ml: 2 }}
                />
                <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
                  <IconButton
                    size="small"
                    onClick={() => updateQuantity(item.book.id, item.quantity - 1)}
                    disabled={item.quantity <= 1}
                  >
                    <Remove />
                  </IconButton>
                  <TextField
                    size="small"
                    value={item.quantity}
                    onChange={(e) => {
                      const value = parseInt(e.target.value) || 0
                      if (value > 0) {
                        updateQuantity(item.book.id, value)
                      }
                    }}
                    inputProps={{ min: 1, style: { textAlign: 'center' } }}
                    sx={{ width: 60, mx: 1 }}
                  />
                  <IconButton
                    size="small"
                    onClick={() => updateQuantity(item.book.id, item.quantity + 1)}
                  >
                    <Add />
                  </IconButton>
                </Box>
                <Typography variant="h6">
                  ${(item.book.price * item.quantity).toFixed(2)}
                </Typography>
                <ListItemSecondaryAction>
                  <IconButton
                    edge="end"
                    onClick={() => removeFromCart(item.book.id)}
                    color="error"
                  >
                    <Delete />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            </React.Fragment>
          ))}
        </List>

        <Divider sx={{ my: 3 }} />

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">
            {t('total')}: ${total.toFixed(2)}
          </Typography>
          <Button
            variant="contained"
            size="large"
            startIcon={<ShoppingCartCheckout />}
            onClick={handleCheckout}
            disabled={loading}
          >
            {loading ? 'Processing...' : t('proceedToPayment')}
          </Button>
        </Box>
      </Paper>
    </Box>
  )
}

export default CartPage''')

    create_file('src/pages/Register.tsx', '''import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  InputAdornment,
  IconButton
} from '@mui/material'
import { Visibility, VisibilityOff } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

const RegisterPage: React.FC = () => {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { signUp } = useAuth()
  const { showNotification } = useNotification()
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    // Username validation
    if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters'
    } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
      newErrors.username = 'Username can only contain letters, numbers, and underscores'
    }

    // Email validation
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = t('invalidEmail')
    }

    // Password validation
    if (formData.password.length < 8) {
      newErrors.password = t('passwordTooShort')
    } else if (!/(?=.*[0-9])(?=.*[a-zA-Z])/.test(formData.password)) {
      newErrors.password = 'Password must contain at least one letter and one number'
    }

    // Confirm password
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = t('passwordsDontMatch')
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setLoading(true)
    try {
      await signUp(formData.email, formData.password, formData.username)
      showNotification(t('registrationSuccess'), 'success')
      navigate('/')
    } catch (error: any) {
      if (error.message?.includes('username')) {
        setErrors({ username: t('usernameTaken') })
      } else {
        showNotification(error.message || t('registrationFailed'), 'error')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
  }

  return (
    <Box
      sx={{
        minHeight: '80vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Paper sx={{ p: 4, maxWidth: 400, width: '100%' }}>
        <Typography variant="h4" gutterBottom align="center">
          {t('register')}
        </Typography>

        <Alert severity="info" sx={{ mb: 3 }}>
          Email verification is required to make purchases
        </Alert>

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label={t('username')}
            value={formData.username}
            onChange={handleChange('username')}
            error={!!errors.username}
            helperText={errors.username}
            margin="normal"
            required
          />

          <TextField
            fullWidth
            type="email"
            label={t('email')}
            value={formData.email}
            onChange={handleChange('email')}
            error={!!errors.email}
            helperText={errors.email}
            margin="normal"
            required
          />

          <TextField
            fullWidth
            type={showPassword ? 'text' : 'password'}
            label={t('password')}
            value={formData.password}
            onChange={handleChange('password')}
            error={!!errors.password}
            helperText={errors.password}
            margin="normal"
            required
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => setShowPassword(!showPassword)}
                    edge="end"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <TextField
            fullWidth
            type={showConfirmPassword ? 'text' : 'password'}
            label={t('confirmPassword')}
            value={formData.confirmPassword}
            onChange={handleChange('confirmPassword')}
            error={!!errors.confirmPassword}
            helperText={errors.confirmPassword}
            margin="normal"
            required
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    edge="end"
                  >
                    {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <Button
            fullWidth
            type="submit"
            variant="contained"
            size="large"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading}
          >
            {loading ? 'Creating account...' : t('signUp')}
          </Button>

          <Typography align="center">
            {t('alreadyHaveAccount')}{' '}
            <Link to="/login" style={{ color: 'inherit' }}>
              {t('signIn')}
            </Link>
          </Typography>
        </form>
      </Paper>
    </Box>
  )
}

export default RegisterPage''')

    create_file('src/pages/Login.tsx', '''import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  InputAdornment,
  IconButton,
  Alert
} from '@mui/material'
import { Visibility, VisibilityOff } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

const LoginPage: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { t } = useTranslation()
  const { signIn } = useAuth()
  const { showNotification } = useNotification()
  
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const from = location.state?.from?.pathname || '/'

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = t('invalidEmail')
    }

    if (!formData.password) {
      newErrors.password = 'Password is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setLoading(true)
    try {
      await signIn(formData.email, formData.password)
      showNotification(t('loginSuccess'), 'success')
      navigate(from, { replace: true })
    } catch (error: any) {
      showNotification(error.message || t('loginFailed'), 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }))
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
  }

  const handleForgotPassword = async () => {
    if (!formData.email) {
      setErrors({ email: 'Please enter your email first' })
      return
    }

    try {
      const { error } = await supabase.auth.resetPasswordForEmail(formData.email, {
        redirectTo: `${window.location.origin}/reset-password`,
      })
      
      if (error) throw error
      
      showNotification('Password reset email sent. Check your inbox.', 'success')
    } catch (error: any) {
      showNotification('Failed to send reset email', 'error')
    }
  }

  return (
    <Box
      sx={{
        minHeight: '80vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Paper sx={{ p: 4, maxWidth: 400, width: '100%' }}>
        <Typography variant="h4" gutterBottom align="center">
          {t('login')}
        </Typography>

        {from !== '/' && (
          <Alert severity="info" sx={{ mb: 3 }}>
            Please login to continue
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            type="email"
            label={t('email')}
            value={formData.email}
            onChange={handleChange('email')}
            error={!!errors.email}
            helperText={errors.email}
            margin="normal"
            required
          />

          <TextField
            fullWidth
            type={showPassword ? 'text' : 'password'}
            label={t('password')}
            value={formData.password}
            onChange={handleChange('password')}
            error={!!errors.password}
            helperText={errors.password}
            margin="normal"
            required
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => setShowPassword(!showPassword)}
                    edge="end"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <Button
            fullWidth
            type="submit"
            variant="contained"
            size="large"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading}
          >
            {loading ? 'Signing in...' : t('signIn')}
          </Button>

          <Box sx={{ mb: 2, textAlign: 'center' }}>
            <Button
              variant="text"
              onClick={handleForgotPassword}
              size="small"
            >
              {t('forgotPassword')}
            </Button>
          </Box>

          <Typography align="center">
            {t('dontHaveAccount')}{' '}
            <Link to="/register" style={{ color: 'inherit' }}>
              {t('signUp')}
            </Link>
          </Typography>
        </form>
      </Paper>
    </Box>
  )
}

export default LoginPage''')

    create_file('src/pages/NotFound.tsx', '''import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Box, Typography, Button } from '@mui/material'
import { Home } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate()
  const { t } = useTranslation()

  return (
    <Box
      sx={{
        minHeight: '60vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
      }}
    >
      <Typography variant="h1" component="h1" gutterBottom>
        404
      </Typography>
      <Typography variant="h4" gutterBottom>
        {t('pageNotFound')}
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        The page you are looking for doesn't exist or has been moved.
      </Typography>
      <Button
        variant="contained"
        size="large"
        startIcon={<Home />}
        onClick={() => navigate('/')}
      >
        {t('backToHome')}
      </Button>
    </Box>
  )
}

export default NotFoundPage''')

    create_file('src/pages/Admin/index.tsx', '''import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'
import AdminLayout from './AdminLayout'
import Dashboard from './Dashboard'
import BooksManagement from './BooksManagement'
import CoursesManagement from './CoursesManagement'
import UsersManagement from './UsersManagement'
import TransactionsView from './TransactionsView'
import SiteSettings from './SiteSettings'

const AdminPage: React.FC = () => {
  const { profile } = useAuth()

  if (!profile?.is_admin) {
    return <Navigate to="/" replace />
  }

  return (
    <AdminLayout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/books" element={<BooksManagement />} />
        <Route path="/courses" element={<CoursesManagement />} />
        <Route path="/users" element={<UsersManagement />} />
        <Route path="/transactions" element={<TransactionsView />} />
        <Route path="/settings" element={<SiteSettings />} />
      </Routes>
    </AdminLayout>
  )
}

export default AdminPage''')

    create_file('src/pages/Admin/AdminLayout.tsx', '''import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Divider,
  useTheme,
  useMediaQuery
} from '@mui/material'
import {
  Dashboard,
  MenuBook,
  School,
  People,
  Receipt,
  Settings
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'

const drawerWidth = 240

interface AdminLayoutProps {
  children: React.ReactNode
}

const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  const location = useLocation()
  const { t } = useTranslation()
  const [mobileOpen, setMobileOpen] = useState(false)

  const menuItems = [
    { path: '/admin', label: t('dashboard'), icon: <Dashboard /> },
    { path: '/admin/books', label: t('manageBooks'), icon: <MenuBook /> },
    { path: '/admin/courses', label: t('manageCourses'), icon: <School /> },
    { path: '/admin/users', label: t('manageUsers'), icon: <People /> },
    { path: '/admin/transactions', label: t('transactions'), icon: <Receipt /> },
    { path: '/admin/settings', label: t('siteSettings'), icon: <Settings /> },
  ]

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap>
          {t('admin')} Panel
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.path} disablePadding>
            <ListItemButton
              component={Link}
              to={item.path}
              selected={location.pathname === item.path}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </div>
  )

  return (
    <Box sx={{ display: 'flex' }}>
      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        {isMobile ? (
          <Drawer
            variant="temporary"
            open={mobileOpen}
            onClose={() => setMobileOpen(false)}
            ModalProps={{ keepMounted: true }}
            sx={{
              '& .MuiDrawer-paper': {
                boxSizing: 'border-box',
                width: drawerWidth,
              },
            }}
          >
            {drawer}
          </Drawer>
        ) : (
          <Drawer
            variant="permanent"
            sx={{
              '& .MuiDrawer-paper': {
                boxSizing: 'border-box',
                width: drawerWidth,
                position: 'relative',
              },
            }}
            open
          >
            {drawer}
          </Drawer>
        )}
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        {children}
      </Box>
    </Box>
  )
}

export default AdminLayout''')

    create_file('src/pages/Admin/Dashboard.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress
} from '@mui/material'
import {
  People,
  MenuBook,
  School,
  AttachMoney
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { adminApi } from '@/services/api/admin'

interface StatCardProps {
  title: string
  value: number
  icon: React.ReactNode
  color: string
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color }) => (
  <Paper sx={{ p: 3, height: '100%' }}>
    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
      <Box
        sx={{
          p: 1.5,
          borderRadius: 2,
          bgcolor: `${color}.100`,
          color: `${color}.main`,
          mr: 2
        }}
      >
        {icon}
      </Box>
      <Typography variant="h6">{title}</Typography>
    </Box>
    <Typography variant="h3" fontWeight="bold">
      {value.toLocaleString()}
    </Typography>
  </Paper>
)

const Dashboard: React.FC = () => {
  const { t } = useTranslation()
  const [stats, setStats] = useState({
    users: 0,
    books: 0,
    courses: 0,
    transactions: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const data = await adminApi.getDashboardStats()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('dashboard')}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Users"
            value={stats.users}
            icon={<People />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Books"
            value={stats.books}
            icon={<MenuBook />}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Courses"
            value={stats.courses}
            icon={<School />}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Transactions"
            value={stats.transactions}
            icon={<AttachMoney />}
            color="error"
          />
        </Grid>
      </Grid>

      {/* Add more dashboard widgets here */}
    </Box>
  )
}

export default Dashboard''')

    create_file('src/pages/Admin/BooksManagement.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  InputAdornment
} from '@mui/material'
import { Edit, Delete, Add, Upload } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Book } from '@/types'
import { booksApi } from '@/services/api/books'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/context/AuthContext'
import { adminApi } from '@/services/api/admin'
import { useNotification } from '@/context/NotificationContext'

const BooksManagement: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingBook, setEditingBook] = useState<Book | null>(null)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: 0,
    cover_url: '',
    file_url: ''
  })
  const [coverFile, setCoverFile] = useState<File | null>(null)
  const [bookFile, setBookFile] = useState<File | null>(null)

  useEffect(() => {
    fetchBooks()
  }, [])

  const fetchBooks = async () => {
    try {
      const data = await booksApi.getAll()
      setBooks(data)
    } catch (error) {
      console.error('Error fetching books:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (book?: Book) => {
    if (book) {
      setEditingBook(book)
      setFormData({
        title: book.title,
        description: book.description,
        price: book.price,
        cover_url: book.cover_url,
        file_url: book.file_url
      })
    } else {
      setEditingBook(null)
      setFormData({
        title: '',
        description: '',
        price: 0,
        cover_url: '',
        file_url: ''
      })
    }
    setDialogOpen(true)
  }

  const handleCloseDialog = () => {
    setDialogOpen(false)
    setEditingBook(null)
    setCoverFile(null)
    setBookFile(null)
  }

  const handleUploadFile = async (file: File, bucket: string, path: string) => {
    try {
      const { data, error } = await supabase.storage
        .from(bucket)
        .upload(path, file, { upsert: true })
      
      if (error) throw error
      
      const { data: { publicUrl } } = supabase.storage
        .from(bucket)
        .getPublicUrl(path)
      
      return publicUrl
    } catch (error) {
      console.error('Upload error:', error)
      throw error
    }
  }

  const handleSave = async () => {
    try {
      let coverUrl = formData.cover_url
      let fileUrl = formData.file_url

      // Upload cover if new file selected
      if (coverFile) {
        const path = `covers/${Date.now()}-${coverFile.name}`
        coverUrl = await handleUploadFile(coverFile, 'book-covers', path)
      }

      // Upload book file if new file selected
      if (bookFile) {
        const path = `books/${Date.now()}-${bookFile.name}`
        fileUrl = await handleUploadFile(bookFile, 'book-files', path)
      }

      const bookData = {
        ...formData,
        cover_url: coverUrl,
        file_url: fileUrl
      }

      if (editingBook) {
        await booksApi.update(editingBook.id, bookData)
        await adminApi.logAction(
          profile!.id,
          'update_book',
          'book',
          editingBook.id,
          { title: bookData.title }
        )
      } else {
        const newBook = await booksApi.create(bookData)
        await adminApi.logAction(
          profile!.id,
          'create_book',
          'book',
          newBook.id,
          { title: bookData.title }
        )
      }

      showNotification('Book saved successfully', 'success')
      handleCloseDialog()
      fetchBooks()
    } catch (error) {
      showNotification('Failed to save book', 'error')
    }
  }

  const handleDelete = async (book: Book) => {
    if (!window.confirm(`Are you sure you want to delete "${book.title}"?`)) {
      return
    }

    try {
      await booksApi.delete(book.id)
      await adminApi.logAction(
        profile!.id,
        'delete_book',
        'book',
        book.id,
        { title: book.title }
      )
      showNotification('Book deleted successfully', 'success')
      fetchBooks()
    } catch (error) {
      showNotification('Failed to delete book', 'error')
    }
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">{t('manageBooks')}</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Add Book
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Cover</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Price</TableCell>
              <TableCell>Created</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {books.map((book) => (
              <TableRow key={book.id}>
                <TableCell>
                  <img
                    src={book.cover_url}
                    alt={book.title}
                    style={{ width: 50, height: 70, objectFit: 'cover' }}
                  />
                </TableCell>
                <TableCell>{book.title}</TableCell>
                <TableCell>${book.price}</TableCell>
                <TableCell>
                  {new Date(book.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handleOpenDialog(book)}>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(book)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>{editingBook ? 'Edit Book' : 'Add Book'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            margin="normal"
            multiline
            rows={4}
            required
          />
          <TextField
            fullWidth
            label="Price"
            type="number"
            value={formData.price}
            onChange={(e) => setFormData({ ...formData, price: Number(e.target.value) })}
            margin="normal"
            InputProps={{
              startAdornment: <InputAdornment position="start">$</InputAdornment>,
            }}
            required
          />
          
          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
              fullWidth
            >
              Upload Cover Image
              <input
                type="file"
                hidden
                accept="image/*"
                onChange={(e) => setCoverFile(e.target.files?.[0] || null)}
              />
            </Button>
            {(coverFile || formData.cover_url) && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                {coverFile ? coverFile.name : 'Current cover uploaded'}
              </Typography>
            )}
          </Box>

          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
              fullWidth
            >
              Upload Book File (PDF)
              <input
                type="file"
                hidden
                accept=".pdf"
                onChange={(e) => setBookFile(e.target.files?.[0] || null)}
              />
            </Button>
            {(bookFile || formData.file_url) && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                {bookFile ? bookFile.name : 'Current file uploaded'}
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleSave}
            variant="contained"
            disabled={!formData.title || !formData.description || formData.price <= 0}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default BooksManagement''')

    # Continue with remaining admin pages...
    create_file('src/pages/Admin/CoursesManagement.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Autocomplete,
  Chip
} from '@mui/material'
import { Edit, Delete, Add, People, Upload } from '@mui/icons-material'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import { useTranslation } from 'react-i18next'
import { Course, CourseEnrollment, User } from '@/types'
import { coursesApi } from '@/services/api/courses'
import { usersApi } from '@/services/api/users'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/context/AuthContext'
import { adminApi } from '@/services/api/admin'
import { useNotification } from '@/context/NotificationContext'

const CoursesManagement: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [courses, setCourses] = useState<Course[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null)
  const [enrollments, setEnrollments] = useState<CourseEnrollment[]>([])
  const [loading, setLoading] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [enrollmentDialogOpen, setEnrollmentDialogOpen] = useState(false)
  const [editingCourse, setEditingCourse] = useState<Course | null>(null)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    image_url: '',
    start_date: new Date().toISOString(),
    end_date: new Date().toISOString(),
    telegram_link: ''
  })
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [coursesData, usersData] = await Promise.all([
        coursesApi.getAll(),
        usersApi.getAllUsers()
      ])
      setCourses(coursesData)
      setUsers(usersData.filter(u => !u.is_banned))
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (course?: Course) => {
    if (course) {
      setEditingCourse(course)
      setFormData({
        title: course.title,
        description: course.description,
        image_url: course.image_url,
        start_date: course.start_date,
        end_date: course.end_date,
        telegram_link: course.telegram_link || ''
      })
    } else {
      setEditingCourse(null)
      setFormData({
        title: '',
        description: '',
        image_url: '',
        start_date: new Date().toISOString(),
        end_date: new Date().toISOString(),
        telegram_link: ''
      })
    }
    setDialogOpen(true)
  }

  const handleCloseDialog = () => {
    setDialogOpen(false)
    setEditingCourse(null)
    setImageFile(null)
  }

  const handleManageEnrollments = async (course: Course) => {
    setSelectedCourse(course)
    try {
      const enrollmentsData = await coursesApi.getCourseEnrollments(course.id)
      setEnrollments(enrollmentsData)
    } catch (error) {
      console.error('Error fetching enrollments:', error)
    }
    setEnrollmentDialogOpen(true)
  }

  const handleSave = async () => {
    try {
      let imageUrl = formData.image_url

      if (imageFile) {
        const path = `courses/${Date.now()}-${imageFile.name}`
        const { data, error } = await supabase.storage
          .from('course-images')
          .upload(path, imageFile, { upsert: true })
        
        if (error) throw error
        
        const { data: { publicUrl } } = supabase.storage
          .from('course-images')
          .getPublicUrl(path)
        
        imageUrl = publicUrl
      }

      const courseData = {
        ...formData,
        image_url: imageUrl
      }

      if (editingCourse) {
        await coursesApi.update(editingCourse.id, courseData)
        await adminApi.logAction(
          profile!.id,
          'update_course',
          'course',
          editingCourse.id,
          { title: courseData.title }
        )
      } else {
        const newCourse = await coursesApi.create(courseData)
        await adminApi.logAction(
          profile!.id,
          'create_course',
          'course',
          newCourse.id,
          { title: courseData.title }
        )
      }

      showNotification('Course saved successfully', 'success')
      handleCloseDialog()
      fetchData()
    } catch (error) {
      showNotification('Failed to save course', 'error')
    }
  }

  const handleDelete = async (course: Course) => {
    if (!window.confirm(`Are you sure you want to delete "${course.title}"?`)) {
      return
    }

    try {
      await coursesApi.delete(course.id)
      await adminApi.logAction(
        profile!.id,
        'delete_course',
        'course',
        course.id,
        { title: course.title }
      )
      showNotification('Course deleted successfully', 'success')
      fetchData()
    } catch (error) {
      showNotification('Failed to delete course', 'error')
    }
  }

  const handleEnrollUser = async () => {
    if (!selectedUser || !selectedCourse) return

    try {
      await coursesApi.enrollUser(selectedCourse.id, selectedUser.id)
      await adminApi.logAction(
        profile!.id,
        'enroll_user',
        'course_enrollment',
        selectedCourse.id,
        { 
          course: selectedCourse.title,
          user: selectedUser.username
        }
      )
      showNotification('User enrolled successfully', 'success')
      
      // Refresh enrollments
      const enrollmentsData = await coursesApi.getCourseEnrollments(selectedCourse.id)
      setEnrollments(enrollmentsData)
      setSelectedUser(null)
    } catch (error) {
      showNotification('Failed to enroll user', 'error')
    }
  }

  const handleUpdateEnrollment = async (enrollment: CourseEnrollment, updates: Partial<CourseEnrollment>) => {
    try {
      await coursesApi.updateEnrollment(enrollment.id, updates)
      await adminApi.logAction(
        profile!.id,
        'update_enrollment',
        'course_enrollment',
        enrollment.id,
        updates
      )
      showNotification('Enrollment updated', 'success')
      
      // Refresh enrollments
      if (selectedCourse) {
        const enrollmentsData = await coursesApi.getCourseEnrollments(selectedCourse.id)
        setEnrollments(enrollmentsData)
      }
    } catch (error) {
      showNotification('Failed to update enrollment', 'error')
    }
  }

  const handleRemoveEnrollment = async (enrollment: CourseEnrollment) => {
    if (!selectedCourse || !window.confirm('Remove this enrollment?')) return

    try {
      await coursesApi.removeEnrollment(selectedCourse.id, enrollment.user_id)
      await adminApi.logAction(
        profile!.id,
        'remove_enrollment',
        'course_enrollment',
        enrollment.id,
        { 
          course: selectedCourse.title,
          user: enrollment.user?.username
        }
      )
      showNotification('Enrollment removed', 'success')
      
      // Refresh enrollments
      const enrollmentsData = await coursesApi.getCourseEnrollments(selectedCourse.id)
      setEnrollments(enrollmentsData)
    } catch (error) {
      showNotification('Failed to remove enrollment', 'error')
    }
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">{t('manageCourses')}</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Add Course
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Image</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Start Date</TableCell>
              <TableCell>End Date</TableCell>
              <TableCell>Enrollments</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {courses.map((course) => (
              <TableRow key={course.id}>
                <TableCell>
                  <img
                    src={course.image_url}
                    alt={course.title}
                    style={{ width: 60, height: 40, objectFit: 'cover' }}
                  />
                </TableCell>
                <TableCell>{course.title}</TableCell>
                <TableCell>
                  {new Date(course.start_date).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  {new Date(course.end_date).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Button
                    size="small"
                    startIcon={<People />}
                    onClick={() => handleManageEnrollments(course)}
                  >
                    Manage
                  </Button>
                </TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handleOpenDialog(course)}>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(course)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Course Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>{editingCourse ? 'Edit Course' : 'Add Course'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            margin="normal"
            multiline
            rows={4}
            required
          />
          
          <Box sx={{ mt: 2, mb: 2 }}>
            <DatePicker
              label="Start Date"
              value={new Date(formData.start_date)}
              onChange={(date) => date && setFormData({ ...formData, start_date: date.toISOString() })}
              slotProps={{ textField: { fullWidth: true } }}
            />
          </Box>
          
          <Box sx={{ mb: 2 }}>
            <DatePicker
              label="End Date"
              value={new Date(formData.end_date)}
              onChange={(date) => date && setFormData({ ...formData, end_date: date.toISOString() })}
              slotProps={{ textField: { fullWidth: true } }}
            />
          </Box>

          <TextField
            fullWidth
            label="Telegram Group Link"
            value={formData.telegram_link}
            onChange={(e) => setFormData({ ...formData, telegram_link: e.target.value })}
            margin="normal"
          />
          
          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
              fullWidth
            >
              Upload Course Image
              <input
                type="file"
                hidden
                accept="image/*"
                onChange={(e) => setImageFile(e.target.files?.[0] || null)}
              />
            </Button>
            {(imageFile || formData.image_url) && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                {imageFile ? imageFile.name : 'Current image uploaded'}
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleSave}
            variant="contained"
            disabled={!formData.title || !formData.description}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Enrollment Dialog */}
      <Dialog
        open={enrollmentDialogOpen}
        onClose={() => setEnrollmentDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Manage Enrollments - {selectedCourse?.title}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <Autocomplete
                options={users.filter(u => !enrollments.some(e => e.user_id === u.id))}
                getOptionLabel={(option) => option.username}
                value={selectedUser}
                onChange={(_, value) => setSelectedUser(value)}
                renderInput={(params) => (
                  <TextField {...params} label="Select user to enroll" />
                )}
                sx={{ flex: 1 }}
              />
              <Button
                variant="contained"
                onClick={handleEnrollUser}
                disabled={!selectedUser}
              >
                Enroll
              </Button>
            </Box>
          </Box>

          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>User</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Progress</TableCell>
                  <TableCell>Enrolled</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {enrollments.map((enrollment) => (
                  <TableRow key={enrollment.id}>
                    <TableCell>{enrollment.user?.username}</TableCell>
                    <TableCell>
                      <Chip
                        label={enrollment.status}
                        color={
                          enrollment.status === 'completed' ? 'success' :
                          enrollment.status === 'in_progress' ? 'primary' : 'default'
                        }
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{enrollment.progress}%</TableCell>
                    <TableCell>
                      {new Date(enrollment.enrolled_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell align="right">
                      <Button
                        size="small"
                        onClick={() => handleUpdateEnrollment(enrollment, {
                          status: enrollment.status === 'completed' ? 'in_progress' : 'completed',
                          progress: enrollment.status === 'completed' ? 50 : 100,
                          completed_at: enrollment.status === 'completed' ? null : new Date().toISOString()
                        })}
                      >
                        Toggle Complete
                      </Button>
                      <IconButton
                        size="small"
                        onClick={() => handleRemoveEnrollment(enrollment)}
                        color="error"
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEnrollmentDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default CoursesManagement''')

    create_file('src/pages/Admin/UsersManagement.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  Avatar,
  TextField,
  InputAdornment,
  Menu,
  MenuItem,
  Switch,
  FormControlLabel
} from '@mui/material'
import {
  Search,
  MoreVert,
  Block,
  Delete,
  AdminPanelSettings,
  Badge as BadgeIcon
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { User } from '@/types'
import { usersApi } from '@/services/api/users'
import { useAuth } from '@/context/AuthContext'
import { adminApi } from '@/services/api/admin'
import { useNotification } from '@/context/NotificationContext'

const UsersManagement: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [users, setUsers] = useState<User[]>([])
  const [filteredUsers, setFilteredUsers] = useState<User[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  useEffect(() => {
    if (searchQuery) {
      const filtered = users.filter(
        user =>
          user.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
          user.email.toLowerCase().includes(searchQuery.toLowerCase())
      )
      setFilteredUsers(filtered)
    } else {
      setFilteredUsers(users)
    }
  }, [searchQuery, users])

  const fetchUsers = async () => {
    try {
      const data = await usersApi.getAllUsers()
      setUsers(data)
      setFilteredUsers(data)
    } catch (error) {
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, user: User) => {
    setAnchorEl(event.currentTarget)
    setSelectedUser(user)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
    setSelectedUser(null)
  }

  const handleToggleBan = async () => {
    if (!selectedUser) return

    try {
      if (selectedUser.is_banned) {
        await usersApi.unbanUser(selectedUser.id)
        await adminApi.logAction(
          profile!.id,
          'unban_user',
          'user',
          selectedUser.id,
          { username: selectedUser.username }
        )
        showNotification('User unbanned', 'success')
      } else {
        await usersApi.banUser(selectedUser.id)
        await adminApi.logAction(
          profile!.id,
          'ban_user',
          'user',
          selectedUser.id,
          { username: selectedUser.username }
        )
        showNotification('User banned', 'success')
      }
      
      fetchUsers()
    } catch (error) {
      showNotification('Failed to update ban status', 'error')
    } finally {
      handleMenuClose()
    }
  }

  const handleToggleAdmin = async () => {
    if (!selectedUser) return

    try {
      await usersApi.updateProfile(selectedUser.id, {
        is_admin: !selectedUser.is_admin
      })
      await adminApi.logAction(
        profile!.id,
        selectedUser.is_admin ? 'remove_admin' : 'make_admin',
        'user',
        selectedUser.id,
        { username: selectedUser.username }
      )
      showNotification(
        selectedUser.is_admin ? 'Admin privileges removed' : 'Admin privileges granted',
        'success'
      )
      fetchUsers()
    } catch (error) {
      showNotification('Failed to update admin status', 'error')
    } finally {
      handleMenuClose()
    }
  }

  const handleDeleteUser = async () => {
    if (!selectedUser || !window.confirm(`Delete user "${selectedUser.username}"? This cannot be undone.`)) {
      return
    }

    try {
      await usersApi.deleteAccount(selectedUser.id)
      await adminApi.logAction(
        profile!.id,
        'delete_user',
        'user',
        selectedUser.id,
        { username: selectedUser.username }
      )
      showNotification('User deleted', 'success')
      fetchUsers()
    } catch (error) {
      showNotification('Failed to delete user', 'error')
    } finally {
      handleMenuClose()
    }
  }

  const handleViewProfile = () => {
    if (selectedUser) {
      window.open(`/profile/${selectedUser.id}`, '_blank')
    }
    handleMenuClose()
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('manageUsers')}
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search users..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Avatar</TableCell>
              <TableCell>Username</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Joined</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredUsers.map((user) => (
              <TableRow key={user.id}>
                <TableCell>
                  <Avatar src={user.avatar_url} sx={{ width: 40, height: 40 }}>
                    {user.username[0].toUpperCase()}
                  </Avatar>
                </TableCell>
                <TableCell>
                  {user.username}
                  {user.is_admin && (
                    <Chip
                      icon={<AdminPanelSettings />}
                      label="Admin"
                      size="small"
                      color="primary"
                      sx={{ ml: 1 }}
                    />
                  )}
                </TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  {user.is_banned ? (
                    <Chip label="Banned" color="error" size="small" />
                  ) : user.email_verified ? (
                    <Chip label="Active" color="success" size="small" />
                  ) : (
                    <Chip label="Unverified" color="warning" size="small" />
                  )}
                </TableCell>
                <TableCell>
                  {new Date(user.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    onClick={(e) => handleMenuOpen(e, user)}
                    disabled={user.id === profile?.id}
                  >
                    <MoreVert />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleViewProfile}>
          View Profile
        </MenuItem>
        <MenuItem onClick={handleToggleBan}>
          <Block sx={{ mr: 1 }} />
          {selectedUser?.is_banned ? 'Unban User' : 'Ban User'}
        </MenuItem>
        <MenuItem onClick={handleToggleAdmin}>
          <AdminPanelSettings sx={{ mr: 1 }} />
          {selectedUser?.is_admin ? 'Remove Admin' : 'Make Admin'}
        </MenuItem>
        <MenuItem onClick={handleDeleteUser} sx={{ color: 'error.main' }}>
          <Delete sx={{ mr: 1 }} />
          Delete User
        </MenuItem>
      </Menu>
    </Box>
  )
}

export default UsersManagement''')

    create_file('src/pages/Admin/TransactionsView.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  List,
  ListItem,
  ListItemText
} from '@mui/material'
import { Visibility } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Transaction } from '@/types'
import { supabase } from '@/services/supabase'

const TransactionsView: React.FC = () => {
  const { t } = useTranslation()
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null)
  const [detailsOpen, setDetailsOpen] = useState(false)

  useEffect(() => {
    fetchTransactions()
  }, [])

  const fetchTransactions = async () => {
    try {
      const { data, error } = await supabase
        .from('transactions')
        .select(`
          *,
          user:users(id, username, email)
        `)
        .order('created_at', { ascending: false })

      if (error) throw error
      setTransactions(data || [])
    } catch (error) {
      console.error('Error fetching transactions:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleViewDetails = (transaction: Transaction) => {
    setSelectedTransaction(transaction)
    setDetailsOpen(true)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success'
      case 'pending':
        return 'warning'
      case 'failed':
        return 'error'
      default:
        return 'default'
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('transactions')}
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>User</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Date</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map((transaction) => (
              <TableRow key={transaction.id}>
                <TableCell>{transaction.id.substring(0, 8)}...</TableCell>
                <TableCell>{transaction.user?.username}</TableCell>
                <TableCell>${transaction.amount.toFixed(2)}</TableCell>
                <TableCell>
                  <Chip
                    label={transaction.status}
                    color={getStatusColor(transaction.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {new Date(transaction.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handleViewDetails(transaction)}>
                    <Visibility />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog
        open={detailsOpen}
        onClose={() => setDetailsOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Transaction Details</DialogTitle>
        <DialogContent>
          {selectedTransaction && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Transaction ID: {selectedTransaction.id}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                User: {selectedTransaction.user?.username} ({selectedTransaction.user?.email})
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                Amount: ${selectedTransaction.amount.toFixed(2)} {selectedTransaction.currency}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                Status: <Chip
                  label={selectedTransaction.status}
                  color={getStatusColor(selectedTransaction.status)}
                  size="small"
                />
              </Typography>
              {selectedTransaction.paymob_transaction_id && (
                <Typography variant="subtitle2" gutterBottom>
                  Paymob ID: {selectedTransaction.paymob_transaction_id}
                </Typography>
              )}
              <Typography variant="subtitle2" gutterBottom>
                Created: {new Date(selectedTransaction.created_at).toLocaleString()}
              </Typography>
              {selectedTransaction.completed_at && (
                <Typography variant="subtitle2" gutterBottom>
                  Completed: {new Date(selectedTransaction.completed_at).toLocaleString()}
                </Typography>
              )}
              
              <Typography variant="h6" sx={{ mt: 2 }}>
                Items:
              </Typography>
              <List>
                {selectedTransaction.items?.map((item, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={`Book ID: ${item.book_id}`}
                      secondary={
                        <>
                          Quantity: {item.quantity} × ${item.price} = ${(item.quantity * item.price).toFixed(2)}
                          {item.is_gift && ` (Gift to ${item.recipient_id})`}
                        </>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  )
}

export default TransactionsView''')

    create_file('src/pages/Admin/SiteSettings.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider
} from '@mui/material'
import { Save } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { adminApi } from '@/services/api/admin'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

const SiteSettings: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [settings, setSettings] = useState({
    site_name: 'React Academy',
    site_description: 'Your journey to knowledge starts here',
    maintenance_mode: false,
    registration_enabled: true,
    email_verification_required: true,
    max_file_size_mb: 50,
    allowed_file_types: ['pdf'],
    telegram_admin_contact: '',
    support_email: ''
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      const data = await adminApi.getSiteSettings()
      if (data) {
        setSettings(prev => ({ ...prev, ...data }))
      }
    } catch (error) {
      console.error('Error fetching settings:', error)
    }
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      await adminApi.updateSiteSettings(settings)
      await adminApi.logAction(
        profile!.id,
        'update_settings',
        'site_settings',
        'global',
        settings
      )
      showNotification('Settings saved successfully', 'success')
    } catch (error) {
      showNotification('Failed to save settings', 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('siteSettings')}
      </Typography>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          General Settings
        </Typography>
        
        <TextField
          fullWidth
          label="Site Name"
          value={settings.site_name}
          onChange={(e) => setSettings({ ...settings, site_name: e.target.value })}
          margin="normal"
        />

        <TextField
          fullWidth
          label="Site Description"
          value={settings.site_description}
          onChange={(e) => setSettings({ ...settings, site_description: e.target.value })}
          margin="normal"
          multiline
          rows={2}
        />

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          System Settings
        </Typography>

        <FormControlLabel
          control={
            <Switch
              checked={settings.maintenance_mode}
              onChange={(e) => setSettings({ ...settings, maintenance_mode: e.target.checked })}
            />
          }
          label="Maintenance Mode"
          sx={{ display: 'block', mb: 2 }}
        />

        <FormControlLabel
          control={
            <Switch
              checked={settings.registration_enabled}
              onChange={(e) => setSettings({ ...settings, registration_enabled: e.target.checked })}
            />
          }
          label="Registration Enabled"
          sx={{ display: 'block', mb: 2 }}
        />

        <FormControlLabel
          control={
            <Switch
              checked={settings.email_verification_required}
              onChange={(e) => setSettings({ ...settings, email_verification_required: e.target.checked })}
            />
          }
          label="Email Verification Required"
          sx={{ display: 'block', mb: 2 }}
        />

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Contact Settings
        </Typography>

        <TextField
          fullWidth
          label="Telegram Admin Contact"
          value={settings.telegram_admin_contact}
          onChange={(e) => setSettings({ ...settings, telegram_admin_contact: e.target.value })}
          margin="normal"
          placeholder="https://t.me/your_admin"
        />

        <TextField
          fullWidth
          label="Support Email"
          type="email"
          value={settings.support_email}
          onChange={(e) => setSettings({ ...settings, support_email: e.target.value })}
          margin="normal"
        />

        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            startIcon={<Save />}
            onClick={handleSave}
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Save Settings'}
          </Button>
        </Box>
      </Paper>
    </Box>
  )
}

export default SiteSettings''')

    # Add missing hook file
    create_file('src/hooks/useBlockUser.ts', '''import { useState, useCallback } from 'react'
import { usersApi } from '@/services/api/users'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

export const useBlockUser = () => {
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [loading, setLoading] = useState(false)

  const blockUser = useCallback(async (userId: string) => {
    if (!profile) return false

    setLoading(true)
    try {
      await usersApi.blockUser(profile.id, userId)
      showNotification('User blocked', 'success')
      return true
    } catch (error) {
      showNotification('Failed to block user', 'error')
      return false
    } finally {
      setLoading(false)
    }
  }, [profile, showNotification])

  const unblockUser = useCallback(async (userId: string) => {
    if (!profile) return false

    setLoading(true)
    try {
      await usersApi.unblockUser(profile.id, userId)
      showNotification('User unblocked', 'success')
      return true
    } catch (error) {
      showNotification('Failed to unblock user', 'error')
      return false
    } finally {
      setLoading(false)
    }
  }, [profile, showNotification])

  const checkBlocked = useCallback(async (userId: string) => {
    if (!profile) return false

    try {
      return await usersApi.isBlocked(profile.id, userId)
    } catch (error) {
      return false
    }
  }, [profile])

  return {
    blockUser,
    unblockUser,
    checkBlocked,
    loading
  }
}''')

    print("React Academy App project structure created successfully!")
    print("\nSQL script for Supabase setup:")
    print("=" * 80)
    print('''
-- Create tables

-- Users table (extends Supabase auth.users)
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  avatar_url TEXT,
  bio TEXT,
  is_admin BOOLEAN DEFAULT false,
  is_banned BOOLEAN DEFAULT false,
  email_verified BOOLEAN DEFAULT false,
  course_progress_public BOOLEAN DEFAULT true,  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Books table
CREATE TABLE books (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  cover_url TEXT NOT NULL,
  file_url TEXT NOT NULL,
  price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Courses table
CREATE TABLE courses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  image_url TEXT NOT NULL,
  start_date TIMESTAMP WITH TIME ZONE NOT NULL,
  end_date TIMESTAMP WITH TIME ZONE NOT NULL,
  telegram_link TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Book ownership table
CREATE TABLE book_ownership (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  purchase_date TIMESTAMP WITH TIME ZONE NOT NULL,
  transaction_id UUID,
  is_gift BOOLEAN DEFAULT false,
  gifted_by UUID REFERENCES users(id),
  gift_message TEXT,
  UNIQUE(book_id, user_id)
);

-- Course enrollments table
CREATE TABLE course_enrollments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status TEXT NOT NULL CHECK (status IN ('not_started', 'in_progress', 'completed')),
  progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
  enrolled_at TIMESTAMP WITH TIME ZONE NOT NULL,
  completed_at TIMESTAMP WITH TIME ZONE,
  certificate_url TEXT,
  UNIQUE(course_id, user_id)
);

-- Reviews table
CREATE TABLE reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  content TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(book_id, user_id)
);

-- Review likes table
CREATE TABLE review_likes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  review_id UUID NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(review_id, user_id)
);

-- Review replies table
CREATE TABLE review_replies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  review_id UUID NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Messages table
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  recipient_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  read_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications table
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type TEXT NOT NULL CHECK (type IN ('gift', 'message', 'review_like', 'review_reply', 'profile_visit', 'course_complete', 'certificate', 'custom')),
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  data JSONB,
  read_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Badges table
CREATE TABLE badges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  icon_url TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User badges table
CREATE TABLE user_badges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  badge_id UUID NOT NULL REFERENCES badges(id) ON DELETE CASCADE,
  assigned_by UUID NOT NULL REFERENCES users(id),
  assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, badge_id)
);

-- Certificates table
CREATE TABLE certificates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  certificate_url TEXT NOT NULL,
  issued_by UUID NOT NULL REFERENCES users(id),
  issued_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, course_id)
);

-- Blocked users table
CREATE TABLE blocked_users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  blocker_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  blocked_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(blocker_id, blocked_id)
);

-- Transactions table
CREATE TABLE transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  amount DECIMAL(10, 2) NOT NULL,
  currency TEXT DEFAULT 'USD',
  status TEXT NOT NULL CHECK (status IN ('pending', 'completed', 'failed')),
  paymob_transaction_id TEXT,
  items JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE
);

-- Admin logs table
CREATE TABLE admin_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  admin_id UUID NOT NULL REFERENCES users(id),
  action TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  details JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Site settings table
CREATE TABLE site_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  settings JSONB NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_books_created_at ON books(created_at DESC);
CREATE INDEX idx_courses_start_date ON courses(start_date DESC);
CREATE INDEX idx_book_ownership_user_id ON book_ownership(user_id);
CREATE INDEX idx_book_ownership_book_id ON book_ownership(book_id);
CREATE INDEX idx_course_enrollments_user_id ON course_enrollments(user_id);
CREATE INDEX idx_course_enrollments_course_id ON course_enrollments(course_id);
CREATE INDEX idx_reviews_book_id ON reviews(book_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_admin_logs_admin_id ON admin_logs(admin_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_books_updated_at BEFORE UPDATE ON books
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON courses
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) Policies

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE books ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE book_ownership ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE review_likes ENABLE ROW LEVEL SECURITY;
ALTER TABLE review_replies ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE certificates ENABLE ROW LEVEL SECURITY;
ALTER TABLE blocked_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE site_settings ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can view all profiles" ON users
  FOR SELECT USING (true);

CREATE POLICY "Users can update own profile" ON users
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON users
  FOR INSERT WITH CHECK (auth.uid() = id);

-- Books policies
CREATE POLICY "Anyone can view books" ON books
  FOR SELECT USING (true);

CREATE POLICY "Only admins can manage books" ON books
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.is_admin = true
    )
  );

-- Book ownership policies
CREATE POLICY "Anyone can view book ownership" ON book_ownership
  FOR SELECT USING (true);

CREATE POLICY "Users can insert own book ownership" ON book_ownership
  FOR INSERT WITH CHECK (user_id = auth.uid() OR gifted_by = auth.uid());

-- Courses policies
CREATE POLICY "Anyone can view courses" ON courses
  FOR SELECT USING (true);

CREATE POLICY "Only admins can manage courses" ON courses
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.is_admin = true
    )
  );

-- Course enrollments policies
CREATE POLICY "Users can view enrollments based on privacy settings" ON course_enrollments
  FOR SELECT USING (
    user_id = auth.uid() OR
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = course_enrollments.user_id
      AND users.course_progress_public = true
    ) OR
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.is_admin = true
    )
  );

CREATE POLICY "Admins can manage enrollments" ON course_enrollments
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.is_admin = true
    )
  );

-- Reviews policies
CREATE POLICY "Anyone can view non-banned user reviews" ON reviews
  FOR SELECT USING (
    NOT EXISTS (
      SELECT 1 FROM users
      WHERE users.id = reviews.user_id
      AND users.is_banned = true
    )
  );

CREATE POLICY "Users can manage own reviews" ON reviews
  FOR ALL USING (user_id = auth.uid());

-- Review likes policies
CREATE POLICY "Anyone can view review likes" ON review_likes
  FOR SELECT USING (true);

CREATE POLICY "Users can manage own likes" ON review_likes
  FOR ALL USING (user_id = auth.uid());

-- Review replies policies
CREATE POLICY "Anyone can view replies" ON review_replies
  FOR SELECT USING (true);

CREATE POLICY "Users can create replies" ON review_replies
  FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own replies" ON review_replies
  FOR DELETE USING (user_id = auth.uid());

-- Messages policies
CREATE POLICY "Users can view own messages" ON messages
  FOR SELECT USING (sender_id = auth.uid() OR recipient_id = auth.uid());

CREATE POLICY "Users can send messages" ON messages
  FOR INSERT WITH CHECK (
    sender_id = auth.uid() AND
    NOT EXISTS (
      SELECT 1 FROM blocked_users
      WHERE (blocker_id = recipient_id AND blocked_id = sender_id)
      OR (blocker_id = sender_id AND blocked_id = recipient_id)
    )
  );

CREATE POLICY "Users can delete own messages" ON messages
  FOR DELETE USING (sender_id = auth.uid());

-- Notifications policies
CREATE POLICY "Users can view own notifications" ON notifications
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can update own notifications" ON notifications
  FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "System can create notifications" ON notifications
  FOR INSERT WITH CHECK (true);

-- Blocked users policies
CREATE POLICY "Users can view own blocks" ON blocked_users
  FOR SELECT USING (blocker_id = auth.uid());

CREATE POLICY "Users can manage own blocks" ON blocked_users
  FOR ALL USING (blocker_id = auth.uid());

-- Transactions policies
CREATE POLICY "Users can view own transactions" ON transactions
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Admins can view all transactions" ON transactions
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.is_admin = true
    )
  );

-- Admin logs policies
CREATE POLICY "Only admins can view admin logs" ON admin_logs
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.is_admin = true
    )
  );

CREATE POLICY "Only admins can create admin logs" ON admin_logs
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.is_admin = true
    )
  );

-- Site settings policies
CREATE POLICY "Anyone can view site settings" ON site_settings
  FOR SELECT USING (true);

CREATE POLICY "Only admins can manage site settings" ON site_settings
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.is_admin = true
    )
  );

-- Create storage buckets
INSERT INTO storage.buckets (id, name, public)
VALUES 
  ('avatars', 'avatars', true),
  ('book-covers', 'book-covers', true),
  ('book-files', 'book-files', false),
  ('course-images', 'course-images', true),
  ('certificates', 'certificates', false),
  ('badges', 'badges', true);

-- Storage policies
CREATE POLICY "Anyone can view public files" ON storage.objects
  FOR SELECT USING (bucket_id IN ('avatars', 'book-covers', 'course-images', 'badges'));

CREATE POLICY "Users can upload own avatar" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can update own avatar" ON storage.objects
  FOR UPDATE USING (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Admins can manage book covers" ON storage.objects
  FOR ALL USING (
    bucket_id = 'book-covers' AND
    EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.is_admin = true
    )
  );

CREATE POLICY "Users can download owned books" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'book-files' AND
    EXISTS (
      SELECT 1 FROM book_ownership bo
      JOIN books b ON b.id = bo.book_id
      WHERE bo.user_id = auth.uid()
      AND b.file_url LIKE '%' || name
    )
  );

CREATE POLICY "Users can download own certificates" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'certificates' AND
    EXISTS (
      SELECT 1 FROM certificates c
      WHERE c.user_id = auth.uid()
      AND c.certificate_url LIKE '%' || name
    )
  );

-- Create initial admin user (update email and username as needed)
-- Note: You'll need to create the auth user first through Supabase Auth
-- Then run this to make them admin:
-- UPDATE users SET is_admin = true WHERE email = 'admin@example.com';

-- Insert default site settings
INSERT INTO site_settings (settings)
VALUES ('{
  "site_name": "React Academy",
  "site_description": "Your journey to knowledge starts here",
  "maintenance_mode": false,
  "registration_enabled": true,
  "email_verification_required": true,
  "max_file_size_mb": 50,
  "allowed_file_types": ["pdf"],
  "telegram_admin_contact": "",
  "support_email": ""
}'::jsonb);

-- Create function to handle user registration
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email, username, email_verified)
  VALUES (
    NEW.id,
    NEW.email,
    NEW.raw_user_meta_data->>'username',
    false
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create user profile on signup
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Create webhook endpoint for Paymob (optional, if using Supabase Edge Functions)
-- This would be implemented as a Supabase Edge Function to handle payment webhooks
''')
    
    print("\n" + "=" * 80)
    print("\nTo set up the project:")
    print("1. Run 'npm install' to install dependencies")
    print("2. Copy the SQL script above and run it in your Supabase SQL editor")
    print("3. Create storage buckets in Supabase as specified in the SQL")
    print("4. Configure Paymob webhook to point to your API endpoint")
    print("5. Run 'npm run dev' to start the development server")
    print("6. Deploy to Vercel when ready")
    print("\nNote: The provided Supabase and Paymob credentials are already configured in .env")

if __name__ == "__main__":
    create_project()