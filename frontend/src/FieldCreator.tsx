// frontend/src/FieldCreator.tsx
import React from 'react';
import { useState } from 'react';

interface Field {
  name: string;
  type: string;
}

export function FieldCreator({ onAddField }: { onAddField: (field: Field) => void }) {
  const [name, setName] = useState('');
  const [type, setType] = useState('String');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name) {
      onAddField({ name, type });
      setName('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
        placeholder="Field Name" 
        required 
      />
      <select value={type} onChange={(e) => setType(e.target.value)}>
        <option value="String">Text</option>
        <option value="Int">Number</option>
        <option value="Boolean">True/False</option>
      </select>
      <button type="submit">Add Field</button>
    </form>
  );
}
