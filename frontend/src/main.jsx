import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import { TextField, Button } from '@mui/material';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <div>
      <TextField label="Field Name" variant="outlined" />
      <Button variant="contained">追加</Button>
    </div>
  </StrictMode>
);
