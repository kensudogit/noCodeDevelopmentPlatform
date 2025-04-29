import React from 'react';
import { useEffect, useState } from "react";

function useOptions(apiUrl: string) {
  const [options, setOptions] = useState<any[]>([]);

  useEffect(() => {
    if (apiUrl) {
      fetch(apiUrl)
        .then(res => res.json())
        .then(data => setOptions(data));
    }
  }, [apiUrl]);

  return options;
}

export function DynamicForm({ layout, formData, setFormData, errors, setErrors }: { 
  layout: any[], 
  formData: any, 
  setFormData: (data: any) => void,
  errors: any,
  setErrors: (errors: any) => void
}) {
  const handleChange = (fieldName: string, value: any) => {
    setFormData({ ...formData, [fieldName]: value });
    const field = layout.find(f => f.field === fieldName);
    if (field?.validations) {
      const error = validateField(value, field.validations);
      setErrors({ ...errors, [fieldName]: error });
    }
  };

  function runCustomScript(script: string, value: any): string | null {
    try {
      // 注意：evalは安全対策を別途必要（ここは簡易版）
      const func = new Function('value', script);
      return func(value);
    } catch (e) {
      return "カスタムスクリプトエラー";
    }
  }
    
  if (field?.custom_script) {
    const error = runCustomScript(field.custom_script, value);
    if (error) {
      setErrors({ ...errors, [fieldName]: error });
    }
  }

  return (
    <form>
      {layout.map((field, idx) => {
        if (!evaluateCondition(formData, field.visibility_condition)) {
          return null;
        }
        if (field.type === "SelectBox") {
          const options = useOptions(field.options_api);
          return (
            <select
              key={idx}
              value={formData[field.field] || ""}
              onChange={(e) => handleChange(field.field, e.target.value)}
            >
              <option value="">選択してください</option>
              {options.map((opt, idx) => (
                <option key={idx} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          );
        }
        // 他タイプは以前と同様
      })}
    </form>
  );
}
