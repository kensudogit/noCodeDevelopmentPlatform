import React from 'react';
import { useEffect, useState } from "react";

export function AppMarket({ onInstall }: { onInstall: (app: any) => void }) {
  const [apps, setApps] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/apps')
      .then(res => res.json())
      .then(setApps);
  }, []);

  return (
    <div>
      <h2>アプリマーケット</h2>
      {apps.map((app, idx) => (
        <div key={idx}>
          <h3>{app.name}</h3>
          <p>{app.description}</p>
          <button onClick={() => onInstall(app)}>インストール</button>
        </div>
      ))}
    </div>
  );
}
