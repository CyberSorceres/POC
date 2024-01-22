import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [inputText, setInputText] = useState('');
  const [apiResponse, setApiResponse] = useState('');

  const handleSubmit = async () => {
    try {
      const response = await axios.post(
        'https://721xnxeo50.execute-api.eu-central-1.amazonaws.com/dev',
        { prompt: inputText }
      );
      setApiResponse(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error('Error sending request to API:', error);
      setApiResponse('Error occurred while sending request.');
    }
  };

  return (
    <div className="App">
      <h1>React API Demo</h1>
      <label>
        Enter Prompt:
        <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} />
      </label>
      <button onClick={handleSubmit}>Submit</button>
      <div>
        <h2>API Response:</h2>
        <pre>{apiResponse}</pre>
      </div>
    </div>
  );
};

export default App;
