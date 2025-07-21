import i18n from 'i18next'
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

export default i18n