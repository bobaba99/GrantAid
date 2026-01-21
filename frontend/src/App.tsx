
import { useState, useEffect } from 'react';
import { Routes, Route, NavLink, Navigate, useNavigate } from 'react-router-dom';
import { signIn, signUp, signOut } from './api/auth';
import './styles/App.css';
import './styles/Navbar.css'; // New Navbar styles
import { FundingList } from './pages/FundingList';
import { FundingDetail } from './pages/FundingDetail';
import { Profile } from './pages/Profile';
import { ErrorMessage } from './components/common/ErrorMessage';
import { supabase } from './api/auth';
import type { Session } from '@supabase/supabase-js';

import { Login } from './pages/Login';

function App() {
  const navigate = useNavigate();
  const [session, setSession] = useState<Session | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleSignUp = async (email: string, pass: string) => {
    try {
      await signUp(email, pass);
    } catch (error: any) {
      console.error('Sign Up Error:', error);
      setErrorMessage(error.message || 'Error signing up');
    }
  };

  const handleSignIn = async (email: string, pass: string) => {
    try {
      await signIn(email, pass);
    } catch (error: any) {
      console.error('Sign In Error:', error);
      setErrorMessage(error.message || 'Error signing in');
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut();
      navigate('/');
    } catch (error: any) {
      console.error('Sign Out Error:', error);
      setErrorMessage(error.message || 'Error signing out');
    }
  };

  if (!session) {
    return (
      <>
        <ErrorMessage message={errorMessage} onClose={() => setErrorMessage('')} />
        <Routes>
          <Route path="*" element={<Login onSignIn={handleSignIn} onSignUp={handleSignUp} />} />
        </Routes>
      </>
    );
  }

  return (
    <div className="container" style={{ width: '100%', margin: '0 auto', padding: '2rem', textAlign: 'center' }}>
      <ErrorMessage message={errorMessage} onClose={() => setErrorMessage('')} />
      <nav className="navbar">
        <div className="nav-links">
          <NavLink
            to="/fundings"
            className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
          >
            Browse Fundings
          </NavLink>
          <NavLink
            to="/profile"
            className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
          >
            My Profile
          </NavLink>
        </div>
        <button onClick={handleSignOut} className="sign-out-btn">Sign Out</button>
      </nav>

      <Routes>
        <Route path="/" element={<Navigate to="/profile" replace />} />
        <Route path="/fundings" element={<FundingList />} />
        <Route path="/funding/:id" element={<FundingDetail />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </div>
  );
}

export default App;
