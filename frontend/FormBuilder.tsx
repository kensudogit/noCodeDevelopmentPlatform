import React from 'react';
import { useState } from "react";
import { FieldPalette } from "./FieldPalette";

export function FormBuilder() {
  const [components, setComponents] = useState<any[]>([]);

  const handleSelect = (comp: any) => {
    setComponents([...components, comp]);
  };

  const handleSave = async () => {
    await fetch('/api/layouts', {
      method: 'POST',
      body: JSON.stringify({ layout: components }),
      headers: { 'Content-Type': 'application/json' }
    });
    alert("保存しました！");
  };

  return (
    <div>
      <FieldPalette onSelect={handleSelect} />
      <h3>作成中のフォーム</h3>
      <div>
        {components.map((comp, idx) => (
          <div key={idx}>{comp.label}</div>
        ))}
      </div>
      <button onClick={handleSave}>保存</button>
    </div>
  );
}
