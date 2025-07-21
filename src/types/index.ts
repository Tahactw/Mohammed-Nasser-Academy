export interface User {
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
}