-- Create custom types
CREATE TYPE experience_type AS ENUM ('Professional', 'Academic', 'Volunteer', 'Research');
CREATE TYPE funding_agency AS ENUM ('CIHR', 'NSERC', 'SSHRC', 'FRQNT', 'FRQSC', 'FRQS', 'Other');
CREATE TYPE application_status AS ENUM ('Draft', 'In Review', 'Submitted');
-- TODO: check with portals for document types
CREATE TYPE document_type AS ENUM ('CV', 'Personal Statement', 'Transcript', 'Other');

-- 1. Profiles (Extends auth.users)
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT,
  program_level TEXT, -- Master's, PhD
  research_field TEXT, -- e.g., Alzheimer's disease
  research_focus TEXT, -- e.g., "Prevention of Alzheimer's disease"
  institution TEXT,
  updated_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Experiences (One-to-many from Profiles)
-- Unified "Experience Bank" table
CREATE TABLE experience (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  type experience_type NOT NULL,
  title TEXT NOT NULL,
  organization TEXT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE, -- NULL means 'Present'
  description TEXT,
  key_skills TEXT[], -- Array of strings
  metadata JSONB, -- Store type-specific fields (e.g., GPA for Academic, Salary for Professional)
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Funding (Catalog of available Funding)
CREATE TABLE funding (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  agency funding_agency NOT NULL,
  cycle_year TEXT NOT NULL, -- e.g., "2025-2026"
  deadline DATE NOT NULL,
  website_url TEXT,
  note TEXT,
  institution_objectives TEXT,
  institution_values TEXT,
  institution_mission TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Requirements (One-to-many from Funding)
CREATE TABLE requirements (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  funding_id UUID REFERENCES funding(id) ON DELETE CASCADE NOT NULL,
  category TEXT NOT NULL, -- e.g., "CV", "Statement"
  description TEXT NOT NULL,
  max_words INTEGER,
  format_rules JSONB, -- Store margins, font sizes as JSON
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Applications (Link User to funding)
CREATE TABLE application (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  funding_id UUID REFERENCES funding(id) ON DELETE CASCADE NOT NULL,
  status application_status DEFAULT 'Draft',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, funding_id)
);

-- 6. Application Documents (Generated files for an application)
CREATE TABLE application_documents (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  application_id UUID REFERENCES application(id) ON DELETE CASCADE NOT NULL,
  type document_type NOT NULL,
  content TEXT, -- Markdown or text content
  version INTEGER DEFAULT 1,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE experience ENABLE ROW LEVEL SECURITY;
ALTER TABLE funding ENABLE ROW LEVEL SECURITY;
ALTER TABLE requirements ENABLE ROW LEVEL SECURITY;
ALTER TABLE application ENABLE ROW LEVEL SECURITY;
ALTER TABLE application_documents ENABLE ROW LEVEL SECURITY;

-- RLS Policies

-- Profiles: Users can see and edit their own profile
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

-- Experiences: Users can manage their own experience
CREATE POLICY "Users can view own experience" ON experience
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own experience" ON experience
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own experience" ON experience
  FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own experience" ON experience
  FOR DELETE USING (auth.uid() = user_id);

-- Funding: Publicly readable, writeable only by admins (service_role)
CREATE POLICY "Funding are viewable by everyone" ON funding
  FOR SELECT USING (true);
CREATE POLICY "Requirements are viewable by everyone" ON requirements
  FOR SELECT USING (true);

-- Applications: Users can manage their own application
CREATE POLICY "Users can view own application" ON application
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own application" ON application
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own application" ON application
  FOR UPDATE USING (auth.uid() = user_id);

-- Application: Users can delete draft applications
CREATE POLICY "Users can delete own application" ON application
  FOR DELETE USING (auth.uid() = user_id);

-- Application Documents: Users can access documents for their own application
-- We use a join in the check implicitly by ensuring the application belongs to the user
CREATE POLICY "Users can view own documents" ON application_documents
  FOR SELECT USING (
    EXISTS (SELECT 1 FROM application WHERE id = application_documents.application_id AND user_id = auth.uid())
  );
CREATE POLICY "Users can insert own documents" ON application_documents
  FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM application WHERE id = application_documents.application_id AND user_id = auth.uid())
  );
CREATE POLICY "Users can update own documents" ON application_documents
  FOR UPDATE USING (
    EXISTS (SELECT 1 FROM application WHERE id = application_documents.application_id AND user_id = auth.uid())
  );
CREATE POLICY "Users can delete own documents" ON application_documents
  FOR DELETE USING (
    EXISTS (SELECT 1 FROM application WHERE id = application_documents.application_id AND user_id = auth.uid())
  );
  
-- Function to handle new user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name)
  VALUES (new.id, new.raw_user_meta_data->>'full_name');
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to automatically create profile on signup
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- 7. Experience Rankings (LLM Scoring)
CREATE TABLE experience_rankings (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  experience_id UUID REFERENCES experience(id) ON DELETE CASCADE NOT NULL,
  funding_id UUID REFERENCES funding(id) ON DELETE CASCADE NOT NULL,
  score INTEGER CHECK (score >= 1 AND score <= 10),
  rationale TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(experience_id, funding_id)
);

-- Enable RLS
ALTER TABLE experience_rankings ENABLE ROW LEVEL SECURITY;

-- Policies for Experience Rankings
-- Users can view rankings if they own the experience
CREATE POLICY "Users can view own rankings" ON experience_rankings
  FOR SELECT USING (
    EXISTS (SELECT 1 FROM experience WHERE id = experience_rankings.experience_id AND user_id = auth.uid())
  );
-- Users can insert rankings (usually via service, but users might trigger it)
CREATE POLICY "Users can insert own rankings" ON experience_rankings
  FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM experience WHERE id = experience_rankings.experience_id AND user_id = auth.uid())
  );
-- Users can delete rankings if they update the experience
CREATE POLICY "Users can delete own rankings" ON experience_rankings
  FOR DELETE USING (
    EXISTS (SELECT 1 FROM experience WHERE id = experience_rankings.experience_id AND user_id = auth.uid())
  );
