import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import PokemonCard from './components/PokemonCard';
import './App.css';

function App() {
  const [pokemonList, setPokemonList] = useState([]);
  const containerRef = useRef(null);

  useEffect(() => {
    const fetchPokemon = async () => {
      try {
        const response = await axios.get('https://pokeapi.co/api/v2/pokemon?limit=151');
        const results = response.data.results;

        const pokemonData = await Promise.all(
          results.map(async (pokemon) => {
            const details = await axios.get(pokemon.url);
            return details.data;
          })
        );

        setPokemonList(pokemonData);
      } catch (error) {
        console.error('Error unable to fetch Pokemon data:', error);
      }
    };

    fetchPokemon();
  }, []);

  const scroll = (direction) => {
    if (containerRef.current) {
      const { current: container } = containerRef;
      const scrollAmount = direction === 'left' ? -250 : 250;
      container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  return (
    <div className="app">
      <h1>Pokedex</h1>
      
      <div className="pokemon-container" ref={containerRef}>
        {pokemonList.map((pokemon) => (
          <PokemonCard key={pokemon.id} pokemon={pokemon} />
        ))}
      </div>

      <div className="navigation">
        <button onClick={() => scroll('left')}>Previous</button>
        <button onClick={() => scroll('right')}>Next</button>
      </div>
    </div>
  );
}

export default App;