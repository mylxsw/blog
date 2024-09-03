import React from 'react';

interface ChatBoxProps {
  type: 'info' | 'warning' | 'error' | 'success';
  children: React.ReactNode;
}

const ChatBox: React.FC<ChatBoxProps> = ({ type, children }) => {
  return (
    <div className={`border-dashed border-2 border-gray-200 rounded-lg p-4 mt-4`}>
        {children}
    </div>
  );
};

export default ChatBox;