
import React from 'react';
import PoliceLogo from '../components/PoliceLogo';
import GovlabLogo from '../components/GovlabLogo';
import SearchInput from '../components/SearchInput';

const Index = () => {
  return (
    <div className="min-h-screen bg-ecoapp-dark flex flex-col">
      {/* Barra superior */}
      <header className="w-full border-b border-red-500 py-2">
        <div className="container flex justify-between items-center">
          <button className="text-white">
            <span className="sr-only">Menú</span>
            &gt;
          </button>
          <button className="text-white">
            <span className="sr-only">Más opciones</span>
            ⋮
          </button>
        </div>
      </header>

      {/* Contenido principal */}
      <main className="flex-1 flex flex-col">
        {/* Logotipos */}
        <div className="container py-12 flex flex-col md:flex-row items-center justify-center gap-8 md:gap-12">
          <PoliceLogo />
          <GovlabLogo />
        </div>

        {/* Título y descripción */}
        <div className="container text-center px-4 mb-12">
          <h1 className="text-white text-5xl font-bold mb-4">EcoPoliciApp</h1>
          <p className="text-white text-lg">
            Asistente virtual para procedimientos ambientales y protección de recursos naturales
          </p>
        </div>

        {/* Buscador */}
        <div className="container mt-auto mb-24 px-4">
          <SearchInput />
        </div>
      </main>
    </div>
  );
};

export default Index;
