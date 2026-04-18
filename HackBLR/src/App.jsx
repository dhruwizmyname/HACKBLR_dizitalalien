import { useState, useEffect, useMemo } from 'react'
import VapiWeb from '@vapi-ai/web'
import './App.css'

// Handle case where Vapi might be exported as .default or the module itself
const Vapi = typeof VapiWeb === 'function' ? VapiWeb : (VapiWeb.default || VapiWeb);

function App() {
  const vapi = useMemo(() => {
    const publicKey = import.meta.env.VITE_VAPI_PUBLIC_KEY;
    const assistantId = import.meta.env.VITE_VAPI_ASSISTANT_ID;

    if (!publicKey || publicKey === 'your-vapi-public-key') {
      console.error('Vapi Public Key is missing or invalid. Check your .env file.');
      return null;
    }

    try {
      console.log('🚀 Initializing Vapi Client...');
      return new Vapi(publicKey);
    } catch (e) {
      console.error('❌ Failed to initialize Vapi:', e);
      return null;
    }
  }, []);

  const [callStatus, setCallStatus] = useState('inactive'); // inactive, loading, active
  const [transcript, setTranscript] = useState([]);

  useEffect(() => {
    if (!vapi) return;
    
    vapi.on('call-start', () => {
      console.log('📞 Call started');
      setCallStatus('active');
    });

    vapi.on('call-end', () => {
      console.log('📞 Call ended');
      setCallStatus('inactive');
    });

    vapi.on('message', (message) => {
      if (message.type === 'transcript' && message.transcriptType === 'final') {
        setTranscript((prev) => [...prev, { role: message.role, text: message.transcript }]);
      }
    });

    vapi.on('error', (e) => {
      console.error('⚠️ Vapi Error:', e);
      setCallStatus('inactive');
    });

    return () => vapi.removeAllListeners();
  }, [vapi]);

  const toggleCall = () => {
    if (!vapi) {
      alert("Assistant initialization failed. Please ensure VITE_VAPI_PUBLIC_KEY is set in your .env and restart the dev server.");
      return;
    }

    const assistantId = import.meta.env.VITE_VAPI_ASSISTANT_ID;
    if (!assistantId || assistantId === 'your-vapi-assistant-id') {
      alert("Assistant ID is missing. Please set VITE_VAPI_ASSISTANT_ID in your .env");
      return;
    }

    if (callStatus === 'active') {
      vapi.stop();
    } else {
      setCallStatus('loading');
      vapi.start(assistantId);
    }
  };

  return (
    <div className="app-wrapper">
      <header className="app-header">
        <div className="logo-section">
          <span className="icon-pulse">🎙️</span>
          <h1>Tribal Support AI</h1>
        </div>
        <p className="subtitle">Voice-activated Mental Health Assistant</p>
      </header>

      <main className="main-content">
        <div className="card glass-card">
          <div className="visualizer-container">
            <div className={`status-indicator ${callStatus}`}>
              {callStatus === 'active' ? 'Listening...' : callStatus === 'loading' ? 'Connecting...' : 'Ready'}
            </div>
            <div className={`wave-animation ${callStatus}`}>
              <span></span><span></span><span></span><span></span><span></span>
            </div>
          </div>

          <button 
            onClick={toggleCall} 
            className={`action-btn ${callStatus}`}
            disabled={callStatus === 'loading'}
          >
            <div className="btn-content">
              {callStatus === 'inactive' && <><span className="btn-icon">▶️</span> Start Support Session</>}
              {callStatus === 'loading' && <span className="loader"></span>}
              {callStatus === 'active' && <><span className="btn-icon">⏹️</span> End Session</>}
            </div>
          </button>
        </div>

        <div className="transcript-section">
          <h3>Conversation History</h3>
          <div className="chat-container">
            {transcript.length === 0 ? (
              <p className="empty-state">Your conversation will appear here once the session starts.</p>
            ) : (
              transcript.map((msg, i) => (
                <div key={i} className={`message-bubble ${msg.role}`}>
                  <span className="role-label">{msg.role === 'assistant' ? '🤖 AI' : '👤 You'}</span>
                  <p>{msg.text}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>Built for HackBLR • Secure & Anonymous</p>
      </footer>
    </div>
  )
}

export default App