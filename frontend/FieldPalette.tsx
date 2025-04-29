import React from 'react';

const COMPONENTS = [
    { type: "TextInput", label: "テキスト入力" },
    { type: "DatePicker", label: "日付選択" },
    { type: "Checkbox", label: "チェックボックス" }
  ];
  
  export function FieldPalette({ onSelect }: { onSelect: (component: any) => void }) {
    return (
      <div>
        <h3>パレット</h3>
        {COMPONENTS.map((comp, idx) => (
          <button key={idx} onClick={() => onSelect(comp)}>
            {comp.label}
          </button>
        ))}
      </div>
    );
  }
  