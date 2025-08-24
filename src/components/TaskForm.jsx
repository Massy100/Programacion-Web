import { useState } from 'react';

function TaskForm({ onAddTask }) {
  const [taskName, setTaskName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (taskName.trim() === '') return;
    
    onAddTask({
      id: Date.now(),
      name: taskName.trim(),
      completed: false
    });
    
    setTaskName('');
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input
        type="text"
        placeholder="New task"
        value={taskName}
        onChange={(e) => setTaskName(e.target.value)}
        className="task-input"
      />
      <button type="submit" className="add-btn">
        Add
      </button>
    </form>
  );
}

export default TaskForm;