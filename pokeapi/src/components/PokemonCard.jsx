import React from 'react';

const PokemonCard = ({ pokemon }) => {
  return (
    <div className="pokemon-card">
      <img
        src={pokemon.sprites.other['official-artwork'].front_default}
        alt={pokemon.name}
      />
      <h2>{pokemon.name.toUpperCase()}</h2>
      <p><strong>Tipo:</strong> {pokemon.types.map((type) => type.type.name).join(', ')}</p>
      <p><strong>Altura:</strong> {pokemon.height / 10} m</p>
      <p><strong>Peso:</strong> {pokemon.weight / 10} kg</p>
    </div>
  );
};

export default PokemonCard;