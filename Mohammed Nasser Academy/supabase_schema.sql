-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing triggers to avoid conflicts
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
DROP TRIGGER IF EXISTS update_courses_updated_at ON courses;
DROP TRIGGER IF EXISTS update_books_updated_at ON books;
DROP TRIGGER IF EXISTS update_reviews_updated_at ON reviews;

-- Add new columns to existing tables if they don't exist
ALTER TABLE users ADD COLUMN IF NOT EXISTS brief TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS theme_preference TEXT DEFAULT 'light' CHECK (theme_preference IN ('light', 'dark', 'auto'));
ALTER TABLE users ADD COLUMN IF NOT EXISTS social_links JSONB DEFAULT '{}'::jsonb;

ALTER TABLE courses ADD COLUMN IF NOT EXISTS brief TEXT;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS telegram_link TEXT;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS prerequisites UUID[];
ALTER TABLE courses ADD COLUMN IF NOT EXISTS difficulty_level TEXT CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced'));

ALTER TABLE books ADD COLUMN IF NOT EXISTS brief TEXT;

ALTER TABLE reviews ADD COLUMN IF NOT EXISTS is_visible BOOLEAN DEFAULT true;

-- Enhanced user badges (drop and recreate to ensure proper structure)
DROP TABLE IF EXISTS user_badges CASCADE;
CREATE TABLE public.user_badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    color TEXT DEFAULT '#FFD700',
    badge_type TEXT CHECK (badge_type IN ('course_completion', 'book_purchase', 'achievement', 'custom')),
    earned_at TIMESTAMPTZ DEFAULT NOW()
);

-- Badge templates for admin to assign
CREATE TABLE IF NOT EXISTS public.badge_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    icon TEXT,
    color TEXT DEFAULT '#FFD700',
    badge_type TEXT CHECK (badge_type IN ('course_completion', 'book_purchase', 'achievement', 'custom')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create or replace updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON courses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_books_updated_at BEFORE UPDATE ON books FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable RLS
ALTER TABLE user_badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE badge_templates ENABLE ROW LEVEL SECURITY;

-- Drop existing policies to avoid conflicts
DROP POLICY IF EXISTS "Public profiles are viewable by everyone" ON users;
DROP POLICY IF EXISTS "Users can update own profile" ON users;
DROP POLICY IF EXISTS "Courses are viewable by everyone" ON courses;
DROP POLICY IF EXISTS "Admin can manage courses" ON courses;
DROP POLICY IF EXISTS "Books are viewable by everyone" ON books;
DROP POLICY IF EXISTS "Admin can manage books" ON books;
DROP POLICY IF EXISTS "Reviews are viewable by everyone" ON reviews;
DROP POLICY IF EXISTS "Users can manage own reviews" ON reviews;
DROP POLICY IF EXISTS "Admin can manage all reviews" ON reviews;

-- Recreate RLS Policies
CREATE POLICY "Public profiles are viewable by everyone" ON users FOR SELECT USING (true);
CREATE POLICY "Users can update own profile" ON users FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Courses are viewable by everyone" ON courses FOR SELECT USING (true);
CREATE POLICY "Admin can manage courses" ON courses FOR ALL USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND (is_admin = true OR email = 'admin@admin.com'))
);

CREATE POLICY "Books are viewable by everyone" ON books FOR SELECT USING (true);
CREATE POLICY "Admin can manage books" ON books FOR ALL USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND (is_admin = true OR email = 'admin@admin.com'))
);

CREATE POLICY "Reviews are viewable by everyone" ON reviews FOR SELECT USING (is_visible = true);
CREATE POLICY "Users can manage own reviews" ON reviews FOR ALL USING (user_id = auth.uid());
CREATE POLICY "Admin can manage all reviews" ON reviews FOR ALL USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND (is_admin = true OR email = 'admin@admin.com'))
);

-- Badge policies
CREATE POLICY "Users can view own badges" ON user_badges FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Public can view user badges" ON user_badges FOR SELECT USING (true);
CREATE POLICY "Admin can manage badges" ON user_badges FOR ALL USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND (is_admin = true OR email = 'admin@admin.com'))
);

CREATE POLICY "Badge templates viewable by everyone" ON badge_templates FOR SELECT USING (true);
CREATE POLICY "Admin can manage badge templates" ON badge_templates FOR ALL USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND (is_admin = true OR email = 'admin@admin.com'))
);

-- Insert default badge templates (handle conflicts)
INSERT INTO badge_templates (name, description, icon, color, badge_type) VALUES
    ('First Course', 'Completed your first course', '🎓', '#4CAF50', 'course_completion'),
    ('Book Lover', 'Purchased 5 books', '📚', '#2196F3', 'book_purchase'),
    ('Active Learner', 'Completed 3 courses', '🚀', '#FF9800', 'achievement'),
    ('Scholar', 'Completed all courses', '👨‍🎓', '#9C27B0', 'achievement'),
    ('Reviewer', 'Left 10 reviews', '⭐', '#FFC107', 'achievement')
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    icon = EXCLUDED.icon,
    color = EXCLUDED.color;

-- Update or insert 5 default courses
INSERT INTO courses (id, title, description, brief, telegram_link, order_index, difficulty_level, is_free) VALUES
    (gen_random_uuid(), 'Introduction to Programming', 'Learn the basics of programming with hands-on projects', 'Start your coding journey', 'https://t.me/+course1', 1, 'beginner', true),
    (gen_random_uuid(), 'Web Development Fundamentals', 'Build modern websites with HTML, CSS, and JavaScript', 'Create amazing websites', 'https://t.me/+course2', 2, 'beginner', true),
    (gen_random_uuid(), 'Advanced JavaScript', 'Master JavaScript and modern frameworks', 'Level up your JS skills', 'https://t.me/+course3', 3, 'intermediate', true),
    (gen_random_uuid(), 'Database Design', 'Learn SQL and database architecture', 'Master data management', 'https://t.me/+course4', 4, 'intermediate', true),
    (gen_random_uuid(), 'Full Stack Development', 'Build complete web applications from scratch', 'Become a full stack developer', 'https://t.me/+course5', 5, 'advanced', true)
ON CONFLICT DO NOTHING;

-- Update the is_admin flag for admin@admin.com user if exists
UPDATE users SET is_admin = true WHERE email = 'admin@admin.com';
