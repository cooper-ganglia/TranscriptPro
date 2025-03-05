import React from 'react';
import DropZone from './components/DropZone';
import ffmpeg from 'fluent-ffmpeg';

const App = () => {
  const handleDrop = (filePath) => {
    ffmpeg(filePath)
      .noVideo()
      .audioChannels(1)
      .audioFrequency(16000)
      .format('wav')
      .save('output.wav')
      .on('end', () => console.log('Audio extracted!'))
      .on('error', (err) => console.error('FFmpeg error:', err));
  };

  return (
    <div className="h-screen bg-gradient-to-br from-blue-900 to-gray-900 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-6">ProTranscript</h1>
        <DropZone onDrop={handleDrop} />
      </div>
    </div>
  );
};
export default App;