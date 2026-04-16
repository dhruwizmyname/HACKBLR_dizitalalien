import { useState, useEffect, useMemo } from 'react'
import VapiWeb from '@vapi-ai/web'
import './App.css'

// Handle case where Vapi might be exported as .default or the module itself
const Vapi = typeof VapiWeb === 'function' ? VapiWeb : (VapiWeb.default || VapiWeb);

function App() {
  const vapi = useMemo(() => {
    try {
      console.log('Initializing Vapi with:', import.meta.env.VITE_VAPI_PUBLIC_KEY);
      return new Vapi(import.meta.env.VITE_VAPI_PUBLIC_KEY);
    } catch (e) {
      console.error('Failed to initialize Vapi:', e);
      return null;
    }
  }, []);
  const [callStatus, setCallStatus] = useState('inactive'); // inactive, loading, active
  const [transcript, setTranscript] = useState('');

  useEffect(() => {
    if (!vapi) return;
    
    vapi.on('call-start', () => setCallStatus('active'));
    vapi.on('call-end', () => setCallStatus('inactive'));
    vapi.on('message', (message) => {
      if (message.type === 'transcript' && message.transcriptType === 'final') {
        setTranscript((prev) => prev + '\n' + message.role + ': ' + message.transcript);
      }
    });
    vapi.on('error', (e) => {
      console.error('Vapi Error:', e);
      setCallStatus('inactive');
    });
    return () => vapi.removeAllListeners();
  }, [vapi]);

  const toggleCall = () => {
    if (!vapi) {
      alert("Voice assistant failed to initialize. Please check your console.");
      return;
    }

    if (callStatus === 'active') {
      vapi.stop();
      setCallStatus('inactive');
    } else {
      setCallStatus('loading');
      vapi.start(import.meta.env.VITE_VAPI_ASSISTANT_ID);
    }
  };

  return (
    <div className="container">
      <h1>🎙️ Mental Voice Assistant</h1>
      <p>Talk to the Tribal Mental Health AI Database</p>

      <button 
        onClick={toggleCall} 
        className={`call-button ${callStatus}`}
        disabled={callStatus === 'loading'}
      >
        {callStatus === 'inactive' && 'Start Call'}
        {callStatus === 'loading' && 'Connecting...'}
        {callStatus === 'active' && 'Stop Call'}
      </button>

      <div className="transcript-box">
        <h3>Live Transcript</h3>
        <pre>{transcript || 'Your conversation will appear here...'}</pre>
      </div>
    </div>
  )
}

export default App