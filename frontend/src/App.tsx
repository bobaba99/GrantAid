import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { signIn, signUp, signOut, getSession, getCurrentUser } from './api/auth';
import './App.css';
import { FundingList } from './pages/FundingList';
import { FundingDetail } from './pages/FundingDetail';
import { Profile } from './pages/Profile';

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [logs, setLogs] = useState<string[]>([]);
  const [envVarsCheck, setEnvVarsCheck] = useState<{ url: boolean; key: boolean }>({
    url: false,
    key: false,
  });

  useEffect(() => {
    const url = !!import.meta.env.VITE_SUPABASE_URL;
    const key = !!import.meta.env.VITE_SUPABASE_ANON_KEY;
    setEnvVarsCheck({ url, key });
    addLog(`Env Vars Check: URL=${url}, Key=${key}`);
  }, []);

  const addLog = (msg: string | object) => {
    const timestamp = new Date().toLocaleTimeString();
    const content = typeof msg === 'object' ? JSON.stringify(msg, null, 2) : msg;
    setLogs((prev) => [`[${timestamp}] ${content}`, ...prev]);
  };

  const handleSignUp = async () => {
    try {
      addLog(`Attempting sign up for ${email}...`);
      const data = await signUp(email, password, username);
      addLog('Sign Up Success:');
      addLog(data);
    } catch (error) {
      addLog(`Sign Up Error: ${error}`);
    }
  };

  const handleSignIn = async () => {
    try {
      addLog(`Attempting sign in for ${email}...`);
      const data = await signIn(email, password);
      addLog('Sign In Success:');
      addLog(data);
    } catch (error) {
      addLog(`Sign In Error: ${error}`);
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut();
      addLog('Sign Out Success');
    } catch (error) {
      addLog(`Sign Out Error: ${error}`);
    }
  };

  const handleGetSession = async () => {
    try {
      const { data, error } = await getSession();
      if (error) throw error;
      addLog('Session Data:');
      addLog(data);
    } catch (error) {
      addLog(`Get Session Error: ${error}`);
    }
  };

  const handleGetUser = async () => {
    try {
      const { data, error } = await getCurrentUser();
      if (error) throw error;
      addLog('User Data:');
      addLog(data);
    } catch (error) {
      addLog(`Get User Error: ${error}`);
    }
  };

  return (
    <BrowserRouter>
      <div className="container" style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem', textAlign: 'left' }}>
        <nav style={{ marginBottom: '2rem', borderBottom: '1px solid #ccc', paddingBottom: '1rem' }}>
          <Link to="/" style={{ marginRight: '1rem' }}>Auth Home</Link>
          <Link to="/fundings" style={{ marginRight: '1rem' }}>Browse Grants</Link>
          <Link to="/profile">My Profile</Link>
        </nav>

        <Routes>
          <Route path="/" element={
            <>
              <h1>Auth Testing Harness</h1>

              <div className="card" style={{ marginBottom: '1rem', padding: '1rem', border: '1px solid #ccc' }}>
                <h3>Environment Status</h3>
                <p>VITE_SUPABASE_URL: {envVarsCheck.url ? '✅ Detected' : '❌ Missing'}</p>
                <p>VITE_SUPABASE_ANON_KEY: {envVarsCheck.key ? '✅ Detected' : '❌ Missing'}</p>
              </div>

              <div className="card" style={{ marginBottom: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <h3>Credentials</h3>
                <input
                  type="text"
                  placeholder="Username (for Sign Up)"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  style={{ padding: '0.5rem' }}
                />
                <input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  style={{ padding: '0.5rem' }}
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  style={{ padding: '0.5rem' }}
                />
              </div>

              <div className="card" style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                <button onClick={handleSignUp}>Sign Up</button>
                <button onClick={handleSignIn}>Sign In</button>
                <button onClick={handleSignOut}>Sign Out</button>
                <button onClick={handleGetSession}>Get Session</button>
                <button onClick={handleGetUser}>Get User</button>
                <button onClick={() => setLogs([])}>Clear Logs</button>
              </div>

              <div className="card">
                <h3>Logs</h3>
                <pre style={{
                  background: '#f4f4f4',
                  color: '#333',
                  padding: '1rem',
                  borderRadius: '4px',
                  height: '400px',
                  overflowY: 'auto',
                  textAlign: 'left',
                  fontSize: '0.85rem'
                }}>
                  {logs.length === 0 ? 'No logs yet...' : logs.join('\n\n')}
                </pre>
              </div>
            </>
          } />
          <Route path="/fundings" element={<FundingList />} />
          <Route path="/funding/:id" element={<FundingDetail />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
