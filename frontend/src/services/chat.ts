import api from '../lib/api';

export interface ChatResponse {
  respuesta: string;
  resumen: string;
}

export interface StreamingChunk {
  content: string | ChatResponse;
  done: boolean;
}

export const chatService = {
  sendMessage: async (message: string): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat', { query: message });
    return response.data;
  },
  
  streamMessage: (message: string, onChunk: (chunk: StreamingChunk) => void) => {
    // Usar EventSource para conectar con el endpoint de streaming
    const eventSource = new EventSource(`${api.defaults.baseURL}/chat/stream?query=${encodeURIComponent(message)}`);
    
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as StreamingChunk;
        onChunk(data);
        
        if (data.done) {
          eventSource.close();
        }
      } catch (e) {
        console.error('Error parsing SSE message:', e);
      }
    };
    
    eventSource.onerror = (error) => {
      console.error('Error en SSE:', error);
      onChunk({
        content: { respuesta: 'Error al conectar con el servidor', resumen: '' },
        done: true
      });
      eventSource.close();
    };
    
    // Return function to close the connection
    return () => eventSource.close();
  },
  
  uploadDocument: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
