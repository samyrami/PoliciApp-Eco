import React from 'react';

interface ChatResponseProps {
  response: {
    respuesta: string;
    resumen: string;
  } | null;
}

const ChatResponse: React.FC<ChatResponseProps> = ({ response }) => {
  if (!response) return null;

  return (
    <div className="mt-6 w-full max-w-2xl mx-auto">
      <div className="bg-gray-800/70 rounded-lg p-4 space-y-4">
        <div>
          <h3 className="text-lg font-semibold text-ecoapp-green mb-2">Respuesta:</h3>
          <p className="text-white whitespace-pre-wrap">{response.respuesta}</p>
        </div>
        {response.resumen && (
          <div>
            <h3 className="text-lg font-semibold text-ecoapp-green mb-2">Resumen:</h3>
            <p className="text-white whitespace-pre-wrap">{response.resumen}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatResponse; 