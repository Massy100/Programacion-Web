import React from 'react';

const PokemonCard = ({ pokemon }) => {
  return (
    <div className="pokemon-card">
      <img
        src={pokemon.sprites.other['official-artwork'].front_default}
        alt={pokemon.name}
      />
      <h2>{pokemon.name.toUpperCase()}</h2>
      <p><strong>Type:</strong> {pokemon.types.map((type) => type.type.name).join(', ')}</p>
      <p><strong>Height:</strong> {pokemon.height / 10} m</p>
      <p><strong>Weight:</strong> {pokemon.weight / 10} kg</p>
      <p><strong>Skills:</strong> {pokemon.abilities.map((ability) => ability.ability.name).join(', ')}</p>
    </div>
  );
};

export default PokemonCard;