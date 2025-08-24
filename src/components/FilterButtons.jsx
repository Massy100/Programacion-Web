function FilterButtons({ currentFilter, onFilterChange }) {
  const filters = [
    { key: 'all', label: 'All' },
    { key: 'active', label: 'Active' },
    { key: 'completed', label: 'Completed' }
  ];

  return (
    <div className="filter-buttons">
      {filters.map(filter => (
        <button
          key={filter.key}
          onClick={() => onFilterChange(filter.key)}
          className={currentFilter === filter.key ? 'active' : ''}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}

export default FilterButtons;