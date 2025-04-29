import { useState } from "react";

export function IntegrationBuilder({ onSave }: { onSave: (integration: any) => void }) {
  const [triggerApi, setTriggerApi] = useState('');
  const [actionApi, setActionApi] = useState('');

  const handleSave = () => {
    const integration = {
      trigger_api: triggerApi,
      trigger_method: "POST",
      trigger_payload: {},
      action_api: actionApi,
      action_method: "POST",
      action_payload_template: {}
    };
    onSave(integration);
  };

  return (
    <div>
      <h3>API統合ビルダー</h3>
      <input value={triggerApi} onChange={(e) => setTriggerApi(e.target.value)} placeholder="トリガーAPIエンドポイント" />
      <input value={actionApi} onChange={(e) => setActionApi(e.target.value)} placeholder="アクションAPIエンドポイント" />
      <button onClick={handleSave}>保存</button>
    </div>
  );
}
