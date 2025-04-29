import React from 'react';
import { useState } from 'react';
import axios from 'axios';

interface SuggestedField {
  name: string;
  type: string;
}

export function FieldSuggester({ onFieldsSelected }: { onFieldsSelected: (fields: SuggestedField[]) => void }) {
  const [prompt, setPrompt] = useState('');
  const [suggestions, setSuggestions] = useState<SuggestedField[]>([]);

  const handleSuggest = async () => {
    const res = await axios.post('/ai/field-suggestions', { prompt });
    const fields = JSON.parse(res.data.fields);
    setSuggestions(fields);
  };

  const handleConfirm = () => {
    onFieldsSelected(suggestions);
  };

  return (
    <div>
      <h3>AIフィールドサジェスト</h3>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="アプリの用途を入力"
      />
      <button onClick={handleSuggest}>フィールド提案を取得</button>

      {suggestions.length > 0 && (
        <div>
          <h4>提案されたフィールド:</h4>
          <ul>
            {suggestions.map((field, idx) => (
              <li key={idx}>
                {field.name} ({field.type})
              </li>
            ))}
          </ul>
          <button onClick={handleConfirm}>これらを追加</button>
        </div>
      )}
    </div>
  );
}
