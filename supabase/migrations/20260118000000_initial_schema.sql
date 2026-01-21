-- Create custom types
CREATE TYPE experience_type AS ENUM ('Professional', 'Academic', 'Volunteer', 'Research');
CREATE TYPE funding_agency AS ENUM ('CIHR', 'FRQS', 'Other');
CREATE TYPE application_status AS ENUM ('Draft', 'In Review', 'Submitted');
CREATE TYPE document_type AS ENUM ('CV', 'Research Statement', 'Other');

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
  institution_vision TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Requirements (One-to-many from Funding)
CREATE TABLE requirements (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  funding_id UUID REFERENCES funding(id) ON DELETE CASCADE NOT NULL,
  category TEXT NOT NULL, -- e.g., "CV", "Statement"
  description TEXT NOT NULL,
  max_pages INTEGER,
  format_rules JSONB, -- Store margins, font sizes as JSON
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE experience ENABLE ROW LEVEL SECURITY;
ALTER TABLE funding ENABLE ROW LEVEL SECURITY;
ALTER TABLE requirements ENABLE ROW LEVEL SECURITY;

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

-- 5. Experience Analysis (LLM Output)
CREATE TABLE IF NOT EXISTS public.experience_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    experience_id UUID NOT NULL REFERENCES public.experience(id) ON DELETE CASCADE,
    funding_id UUID NOT NULL REFERENCES public.funding(id) ON DELETE CASCADE,
    story TEXT NOT NULL,
    rationale TEXT NOT NULL,
    experience_rating_facet_a INTEGER NOT NULL, -- Competency & Capacity
    experience_rating_facet_b INTEGER NOT NULL, -- Fit with Program Priorities
    experience_rating_facet_c INTEGER NOT NULL, -- Impact & Value
    experience_rating_facet_d INTEGER NOT NULL, -- Narrative Flow & Coherence
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    UNIQUE(experience_id, funding_id)
);

-- Enable RLS
ALTER TABLE public.experience_analysis ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can all actions on own analyses"
ON public.experience_analysis
FOR ALL
USING (auth.uid() = user_id);