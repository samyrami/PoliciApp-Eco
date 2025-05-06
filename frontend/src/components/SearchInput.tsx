import React, { useState, useEffect, useRef } from 'react';
import { ArrowRight } from 'lucide-react';
import { chatService, type ChatResponse, type StreamingChunk } from '../services/chat';
import { useToast } from '@/hooks/use-toast';
import ChatResponseComponent from './ChatResponse';
import ChatHistory from './ChatHistory';

interface Message {
  query: string;
  response: ChatResponse;
  timestamp: Date;
  streaming?: boolean;
}

const SearchInput: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentStreamingText, setCurrentStreamingText] = useState('');
  const { toast } = useToast();
  const streamCleanupRef = useRef<() => void | null>(null);

  // Cleanup streaming on unmount
  useEffect(() => {
    return () => {
      if (streamCleanupRef.current) {
        streamCleanupRef.current();
      }
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) {
      toast({
        title: "Error",
        description: "Por favor ingresa un mensaje",
        variant: "destructive",
      });
      return;
    }

    try {
      setLoading(true);
      const currentQuery = query;
      setQuery(''); // Limpiar input inmediatamente
      
      // Crear mensaje temporal con streaming
      const tempMessage: Message = {
        query: currentQuery,
        response: { respuesta: '', resumen: '' },
        timestamp: new Date(),
        streaming: true
      };
      
      setMessages(prev => [...prev, tempMessage]);
      setCurrentStreamingText('');
      
      // Iniciar streaming
      streamCleanupRef.current = chatService.streamMessage(currentQuery, (chunk: StreamingChunk) => {
        if (chunk.done) {
          // Actualizar con la respuesta final
          const finalResponse = chunk.content as ChatResponse;
          setMessages(prev => 
            prev.map((msg, idx) => 
              idx === prev.length - 1 
                ? { ...msg, response: finalResponse, streaming: false }
                : msg
            )
          );
          setCurrentStreamingText('');
          setLoading(false);
        } else {
          // Actualizar texto de streaming
          const newText = chunk.content as string;
          setCurrentStreamingText(prev => prev + newText);
          
          // Actualizar mensaje temporal
          setMessages(prev => 
            prev.map((msg, idx) => 
              idx === prev.length - 1 
                ? { ...msg, response: { ...msg.response, respuesta: msg.response.respuesta + newText } }
                : msg
            )
          );
        }
      });
      
    } catch (error) {
      console.error('Error:', error);
      toast({
        title: "Error",
        description: "No se pudo enviar el mensaje",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  return (
    <div className="w-full space-y-6 p-4">
      {/* Historial de mensajes */}
      <ChatHistory messages={messages} />

      {/* Formulario de entrada */}
      <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto sticky bottom-4">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="¿En qué puedo ayudarte?"
            className={`w-full bg-gray-800/70 text-white rounded-full py-3 px-6 pr-12 
              focus:outline-none focus:ring-2 focus:ring-ecoapp-green
              transition-all duration-200 ${loading ? 'opacity-70' : ''}`}
            disabled={loading}
          />
          <button 
            type="submit"
            className={`absolute right-1 top-1/2 -translate-y-1/2 
              bg-gray-700 hover:bg-gray-600 p-2 rounded-full text-gray-300
              transition-all duration-200 ${loading ? 'animate-pulse' : ''}`}
            disabled={loading}
          >
            <ArrowRight size={20} />
          </button>
        </div>
        {loading && (
          <div className="text-center mt-2 text-sm text-gray-400">
            Procesando tu mensaje...
          </div>
        )}
      </form>
    </div>
  );
};

export default SearchInput;
