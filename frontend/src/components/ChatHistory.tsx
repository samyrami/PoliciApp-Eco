import React from 'react';

interface Message {
  query: string;
  response: {
    respuesta: string;
    resumen: string;
  };
  timestamp: Date;
  streaming?: boolean;
}

interface ChatHistoryProps {
  messages: Message[];
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages }) => {
  // Helper function to safely render content
  const renderContent = (content: any): string => {
    if (typeof content === 'string') {
      return content;
    }
    // If it's an object, convert to string or return empty
    if (typeof content === 'object' && content !== null) {
      // For objects with Campo and Descripción properties
      if (content.Campo && content.Descripción) {
        return `${content.Campo}: ${content.Descripción}`;
      }
      // For other objects, try to stringify
      try {
        return JSON.stringify(content);
      } catch (e) {
        return '[Object]';
      }
    }
    // If it's anything else, convert to string
    return String(content);
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      {messages.map((message, index) => (
        <div key={index} className="space-y-4">
          {/* Mensaje del usuario */}
          <div className="flex justify-end">
            <div className="bg-ecoapp-green/20 rounded-lg p-3 max-w-[80%]">
              <p className="text-white">{message.query}</p>
              <span className="text-xs text-gray-400">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>

          {/* Respuesta del sistema */}
          <div className="flex justify-start">
            <div className="bg-gray-800/70 rounded-lg p-4 max-w-[80%]">
              <p className="text-white whitespace-pre-wrap">
                {renderContent(message.response.respuesta)}
                {message.streaming && (
                  <span className="inline-block ml-1 animate-pulse">▋</span>
                )}
              </p>
              {message.response.resumen && !message.streaming && (
                <div className="mt-2 pt-2 border-t border-gray-700">
                  <p className="text-sm text-gray-300">{renderContent(message.response.resumen)}</p>
                </div>
              )}
              <span className="text-xs text-gray-400">
                {new Date(message.timestamp).toLocaleTimeString()}
                {message.streaming && " (generando...)"}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatHistory; 