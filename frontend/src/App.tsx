
import { useState, useEffect } from 'react';
import { Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import { signIn, signUp, signOut, getSession, getCurrentUser } from './api/auth';
import './styles/App.css';
import { FundingList } from './pages/FundingList';
import { FundingDetail } from './pages/FundingDetail';
import { Profile } from './pages/Profile';
import { ErrorMessage } from './components/common/ErrorMessage';
import { supabase } from './api/auth';
import type { Session } from '@supabase/supabase-js';

function App() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [logs, setLogs] = useState<string[]>([]);
  const [session, setSession] = useState<Session | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [envVarsCheck, setEnvVarsCheck] = useState<{ url: boolean; key: boolean }>({
    url: false,
    key: false,
  });

  useEffect(() => {
    const url = !!import.meta.env.VITE_SUPABASE_URL;
    const key = !!import.meta.env.VITE_SUPABASE_ANON_KEY;
    setEnvVarsCheck({ url, key });
    addLog(`Env Vars Check: URL = ${url}, Key = ${key} `);

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

  const addLog = (msg: string | object) => {
    const timestamp = new Date().toLocaleTimeString();
    const content = typeof msg === 'object' ? JSON.stringify(msg, null, 2) : msg;
    setLogs((prev) => [`[${timestamp}] ${content} `, ...prev]);
  };

  const handleSignUp = async () => {
    try {
      addLog(`Attempting sign up for ${email}...`);
      const data = await signUp(email, password, '');
      addLog('Sign Up Success:');
      addLog(data);
    } catch (error: any) {
      addLog(`Sign Up Error: ${error} `);
      setErrorMessage(error.message || 'Error signing up');
    }
  };

  const handleSignIn = async () => {
    try {
      addLog(`Attempting sign in for ${email}...`);
      const data = await signIn(email, password);
      addLog('Sign In Success:');
      addLog(data);
    } catch (error: any) {
      addLog(`Sign In Error: ${error} `);
      setErrorMessage(error.message || 'Error signing in');
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut();
      addLog('Sign Out Success');
      navigate('/');
    } catch (error: any) {
      addLog(`Sign Out Error: ${error} `);
      setErrorMessage(error.message || 'Error signing out');
    }
  };

  const handleGetSession = async () => {
    try {
      const { data, error } = await getSession();
      if (error) throw error;
      addLog('Session Data:');
      addLog(data);
    } catch (error: any) {
      addLog(`Get Session Error: ${error} `);
      setErrorMessage(error.message || 'Error getting session');
    }
  };

  const handleGetUser = async () => {
    try {
      const { data, error } = await getCurrentUser();
      if (error) throw error;
      addLog('User Data:');
      addLog(data);
    } catch (error: any) {
      addLog(`Get User Error: ${error} `);
      setErrorMessage(error.message || 'Error getting user');
    }
  };

  return (
    <div className="container" style={{ width: '100%', margin: '0 auto', padding: '2rem', textAlign: 'center' }}>

      <ErrorMessage message={errorMessage} onClose={() => setErrorMessage('')} />
      {session && (
        <nav style={{
          marginBottom: '2rem',
          borderBottom: '1px solid #ccc',
          paddingBottom: '1rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div>
            <Link to="/fundings" style={{ marginRight: '1rem' }}>Browse Fundings</Link>
            <Link to="/profile">My Profile</Link>
          </div>
          <button onClick={handleSignOut}>Sign Out</button>
        </nav>
      )}

      <Routes>
        <Route path="/" element={
          session ? <Navigate to="/profile" replace /> : (
            <>
              <div className="card" style={{
                marginBottom: '1rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '0.5rem',
                alignItems: 'center', // Center children horizontally
                justifyContent: 'center', // Center children vertically if needed, mostly for flex container
                width: '100%'
              }}>
                <h1 style={{ textAlign: 'center' }}>Login</h1>
                <input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  style={{ padding: '0.5rem', width: '30vw', minWidth: '250px' }}
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  style={{ padding: '0.5rem', width: '30vw', minWidth: '250px' }}
                />
              </div>

              <div className="card" style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap', justifyContent: 'center' }}>
                <button onClick={handleSignUp}>Sign Up</button>
                <button onClick={handleSignIn}>Sign In</button>
              </div>
            </>
          )
        } />
        <Route path="/fundings" element={<FundingList />} />
        <Route path="/funding/:id" element={<FundingDetail />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </div>

  );
}

export default App;
