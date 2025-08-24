function TaskItem({ task, onToggleTask, onDeleteTask }) {
  return (
    <li className={`task-item ${task.completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggleTask(task.id)}
        className="task-checkbox"
      />
      <span className="task-name">{task.name}</span>
      <button
        onClick={() => onDeleteTask(task.id)}
        className="delete-btn"
      >
        Delete
      </button>
    </li>
  );
}

export default TaskItem;