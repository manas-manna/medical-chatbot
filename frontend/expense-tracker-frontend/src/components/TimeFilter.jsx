import React from 'react';

const TimeFilter = ({ selectedRange, onRangeChange }) => (
  <div className="flex gap-4 my-4">
    <button onClick={() => onRangeChange('7d')} className={`px-4 py-2 rounded ${selectedRange === '7d' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>Last 7 Days</button>
    <button onClick={() => onRangeChange('30d')} className={`px-4 py-2 rounded ${selectedRange === '30d' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>Last 30 Days</button>
  </div>
);

export default TimeFilter;
