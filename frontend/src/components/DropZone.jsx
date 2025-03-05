import React, { useState } from 'react';
import { useDrop } from 'react-dnd';

const DropZone = ({ onDrop }) => {
  const [status, setStatus] = useState('Drop a video file here');
  const [{ isOver }, drop] = useDrop(() => ({
    accept: 'video/*',
    drop: (item) => {
      setStatus('Processing...');
      onDrop(item.files[0].path);
    },
    collect: (monitor) => ({ isOver: !!monitor.isOver() }),
  }));

  return (
    <div
      ref={drop}
      className={`p-10 rounded-xl bg-white/10 backdrop-blur-lg text-white text-2xl font-bold transition-all shadow-lg ${
        isOver ? 'scale-105 bg-white/20' : ''
      }`}
    >
      {status}
    </div>
  );
};
export default DropZone;