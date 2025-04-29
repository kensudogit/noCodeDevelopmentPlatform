import { useState } from "react";

export function WorkflowBuilder({ onSave }: { onSave: (workflow: any) => void }) {
  const [ifField, setIfField] = useState('');
  const [ifOperator, setIfOperator] = useState('==');
  const [ifValue, setIfValue] = useState('');
  const [thenAction, setThenAction] = useState('send_email');
  const [elseAction, setElseAction] = useState('notify_admin');

  const handleSave = () => {
    const workflow = {
      if: { field: ifField, operator: ifOperator, value: ifValue },
      then: { action: thenAction, params: {} },
      else: { action: elseAction, params: {} }
    };
    onSave(workflow);
  };

  return (
    <div>
      <h3>ワークフロービルダー</h3>
      <div>
        <label>IF フィールド名</label>
        <input value={ifField} onChange={(e) => setIfField(e.target.value)} />
      </div>
      <div>
        <label>演算子</label>
        <select value={ifOperator} onChange={(e) => setIfOperator(e.target.value)}>
          <option value="==">==</option>
          <option value=">">{'>'}</option>
          <option value="<">{'<'}</option>
        </select>
      </div>
      <div>
        <label>値</label>
        <input value={ifValue} onChange={(e) => setIfValue(e.target.value)} />
      </div>
      <div>
        <label>THENアクション</label>
        <select value={thenAction} onChange={(e) => setThenAction(e.target.value)}>
          <option value="send_email">メール送信</option>
          <option value="post_slack">Slack通知</option>
        </select>
      </div>
      <div>
        <label>ELSEアクション</label>
        <select value={elseAction} onChange={(e) => setElseAction(e.target.value)}>
          <option value="notify_admin">管理者通知</option>
          <option value="none">何もしない</option>
        </select>
      </div>

      <button onClick={handleSave}>ワークフローを保存</button>
    </div>
  );
}
