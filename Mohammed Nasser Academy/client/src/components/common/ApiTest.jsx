import React, { useEffect, useState } from 'react';
import api, { testApiConnection } from '../lib/api';

const ApiTest = () => {
  const [status, setStatus] = useState('Testing...');
  const [details, setDetails] = useState(null);
  
  useEffect(() => {
    const runTest = async () => {
      try {
        const result = await testApiConnection();
        setStatus('✅ API Connected Successfully!');
        setDetails(result);
      } catch (error) {
        setStatus('❌ API Connection Failed');
        setDetails({ error: error.message });
      }
    };
    
    runTest();
  }, []);
  
  return (
    <div style={{ padding: '20px', background: '#f0f0f0', borderRadius: '8px', margin: '20px' }}>
      <h3>API Connection Test</h3>
      <p>{status}</p>
      {details && (
        <pre style={{ background: '#fff', padding: '10px', borderRadius: '4px' }}>
          {JSON.stringify(details, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default ApiTest;
