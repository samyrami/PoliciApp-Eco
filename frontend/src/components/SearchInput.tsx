
import React, { useState } from 'react';
import { ArrowRight } from 'lucide-react';

const SearchInput: React.FC = () => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Búsqueda enviada:', query);
    // Aquí iría la lógica de procesamiento de la búsqueda
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="¿En qué puedo ayudarte?"
          className="w-full bg-gray-800/70 text-white rounded-full py-3 px-6 pr-12 focus:outline-none focus:ring-2 focus:ring-ecoapp-green"
        />
        <button 
          type="submit"
          className="absolute right-1 top-1/2 -translate-y-1/2 bg-gray-700 hover:bg-gray-600 p-2 rounded-full text-gray-300"
        >
          <ArrowRight size={20} />
        </button>
      </div>
    </form>
  );
};

export default SearchInput;
