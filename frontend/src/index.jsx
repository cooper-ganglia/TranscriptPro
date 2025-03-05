import React from 'react';
import { createRoot } from 'react-dom/client';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import App from './App';

const root = createRoot(document.getElementById('root'));
root.render(
  <DndProvider backend={HTML5Backend}>
    <App />
  </DndProvider>
);