import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Home from './pages/Home';
import About from './pages/About';
import Logs from './pages/Logs';
import NotFound from './pages/NotFound';
import { useState, useRef } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const sessionIdRef = useRef(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);

  return (
    <Router>
      <div className="flex flex-col h-screen overflow-hidden bg-surface-50 text-surface-900">
        <NavBar />
        <main className="flex-1 overflow-hidden relative z-0">
          <Routes>
            <Route
              path="/"
              element={
                <Home
                  messages={messages}
                  setMessages={setMessages}
                  sessionIdRef={sessionIdRef}
                />
              }
            />
            <Route path="/about" element={<About />} />
            <Route path="/logs" element={<Logs />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
