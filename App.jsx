import { useState } from 'react';

function Chatbox() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    const response = await fetch('http://localhost:5000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: input }),
    });

    const data = await response.json();
    setMessages([...messages, { user: input, bot: data.answer }]);
    setInput('');
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto' }}>
      <h1>LangGraph Chatbot</h1>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '400px', overflowY: 'scroll' }}>
        {messages.map((msg, i) => (
          <div key={i}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
              <img src="/images/user.png" alt="user" style={{ width: '30px', height: '30px', marginRight: '10px' }} />
              <p><strong>You:</strong> {msg.user}</p>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px' }}>
              <img src="/images/bot.png" alt="bot" style={{ width: '30px', height: '30px', marginRight: '10px' }} />
              <p><strong>Bot:</strong> {msg.bot}</p>
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '10px' }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ width: '80%', padding: '8px' }}
        />
        <button onClick={sendMessage} style={{ padding: '8px 16px', marginLeft: '10px' }}>Send</button>
      </div>
    </div>
  );
}

export default Chatbox;
