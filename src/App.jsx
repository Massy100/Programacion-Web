import { useState } from 'react';
import useLocalStorage from './hooks/useLocalStorage';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import FilterButtons from './components/FilterButtons';
import './App.css';

function App() {
  const [tasks, setTasks] = useLocalStorage('tasks', []);
  const [filter, setFilter] = useState('all');

  const addTask = (task) => {
    setTasks([...tasks, task]);
  };

  const toggleTask = (taskId) => {
    setTasks(tasks.map(task =>
      task.id === taskId ? { ...task, completed: !task.completed } : task
    ));
  };

  const deleteTask = (taskId) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  return (
    <div className="app">
      <h1>Tasks Manager</h1>
      <TaskForm onAddTask={addTask} />
      <FilterButtons currentFilter={filter} onFilterChange={setFilter} />
      <TaskList
        tasks={tasks}
        filter={filter}
        onToggleTask={toggleTask}
        onDeleteTask={deleteTask}
      />
      {tasks.length > 0 && (
        <p className="task-counter">
          {tasks.filter(t => !t.completed).length} to-do list out of {tasks.length} total tasks
        </p>
      )}
    </div>
  );
}

export default App;