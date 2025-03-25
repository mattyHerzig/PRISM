import React, { useEffect, useState } from 'react';
import './App.css';
import { initializeApp } from 'firebase/app';
import { getDatabase, ref, get } from 'firebase/database';

const firebaseConfig = {
  databaseURL: "https://prism-7d7a9-default-rtdb.firebaseio.com"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

function App() {
  const [users, setUsers] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const snapshot = await get(ref(db, 'users'));
      if (snapshot.exists()) {
        setUsers(snapshot.val());
      }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>🚀 PR Scores Dashboard</h1>
      {Object.entries(users).map(([user, data]) => (
        <div key={user} className="card">
          <h2>{user}</h2>

          <div className="cumulative">
            <strong>Cumulative Score:</strong><br />
            📖 Readability: {data.cumulative_score?.readability_score?.toFixed(2)}<br />
            ⚙️ Robustness: {data.cumulative_score?.robustness_score?.toFixed(2)}<br />
            🔐 Security: {data.cumulative_score?.security_score?.toFixed(2)}<br />
            🚀 Performance: {data.cumulative_score?.performance_score?.toFixed(2)}<br />
            🧮 PR Count: {data.cumulative_score?.pr_count}
          </div>

          <h4>Pull Requests:</h4>
          {Object.entries(data)
            .filter(([key]) => key !== "cumulative_score")
            .map(([prId, scores]) => (
              <div key={prId} className="pr">
                <strong>{prId}</strong> ({scores.model})<br />
                📖 C: {scores.readability_score} | ⚙️ R: {scores.robustness_score} | 🔐 V: {scores.security_score} | 🚀 E: {scores.performance_score}
              </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default App;
