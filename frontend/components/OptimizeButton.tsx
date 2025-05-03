import React from 'react';
import { useState } from "react";

export function OptimizeButton({ layout }: { layout: any }) {
  const [suggestion, setSuggestion] = useState('');

  const handleOptimize = async () => {
    const res = await fetch('/api/ai/optimize-form', {
      method: 'POST',
      body: JSON.stringify({ layout }),
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    setSuggestion(data.suggestion);
  };

  return (
    <div>
      <button onClick={handleOptimize}>フォームをAIで最適化提案</button>
      {suggestion && (
        <div>
          <h4>改善提案</h4>
          <pre>{suggestion}</pre>
        </div>
      )}
    </div>
  );
}
