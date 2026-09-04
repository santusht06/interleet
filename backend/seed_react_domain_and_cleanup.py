#!/usr/bin/env python3
"""
Interleet — React Domain Seeder (JSX + TSX Skeletons & Robust Test Cases)
=======================================================================
1. Cleans up legacy domains.
2. Provides unsolved starter skeletons for both JSX (App.jsx) and TSX (App.tsx).
3. Configures runtime='frontend' and execution_mode='browser'.
"""

import os
import json
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

REACT_CHALLENGES = [
    {
        "title": "Interactive Counter with Step & Limits",
        "slug": "react-interactive-counter-step-limits",
        "short_description": "Build an interactive counter with step adjustments, min/max clamps, and disabled boundary controls.",
        "difficulty": "Easy",
        "xp_reward": 100,
        "description": """### Interactive Counter with Step & Limits

Build a dynamic React counter component that allows users to increment, decrement, reset, and customize step increments while strictly respecting min/max bounds.

---
#### Component Requirements
1. Render current count inside `<span id="counter-value">{count}</span>` (initial value `0`).
2. Provide `<button id="btn-increment">+</button>` and `<button id="btn-decrement">-</button>`.
3. Provide `<button id="btn-reset">Reset</button>` to restore count to `0`.
4. Provide `<input id="input-step" type="number" />` with default step `1`.
5. Minimum limit is `-10` and Maximum limit is `10`.
6. When count reaches `10`, the increment button must have the `disabled` attribute.
7. When count reaches `-10`, the decrement button must have the `disabled` attribute.
""",
        "starter_code": {
            "App.jsx": """import React, { useState } from 'react';

export default function App() {
  const [count, setCount] = useState(0);
  const [step, setStep] = useState(1);
  const MIN = -10;
  const MAX = 10;

  // TODO: Implement increment handler clamped to MAX (10)
  const handleIncrement = () => {
    
  };

  // TODO: Implement decrement handler clamped to MIN (-10)
  const handleDecrement = () => {
    
  };

  // TODO: Implement reset handler restoring count to 0
  const handleReset = () => {
    
  };

  return (
    <div className="counter-container">
      <h2>Counter</h2>
      <div className="value-display">
        <span id="counter-value">{count}</span>
      </div>
      <div className="step-control">
        <label>Step: </label>
        <input 
          id="input-step" 
          type="number" 
          value={step} 
          onChange={(e) => setStep(Number(e.target.value) || 1)} 
        />
      </div>
      <div className="button-group">
        <button id="btn-decrement" onClick={handleDecrement} disabled={count <= MIN}>-</button>
        <button id="btn-reset" onClick={handleReset}>Reset</button>
        <button id="btn-increment" onClick={handleIncrement} disabled={count >= MAX}>+</button>
      </div>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState } from 'react';

export default function App(): JSX.Element {
  const [count, setCount] = useState<number>(0);
  const [step, setStep] = useState<number>(1);
  const MIN: number = -10;
  const MAX: number = 10;

  // TODO: Implement increment handler clamped to MAX (10)
  const handleIncrement = (): void => {
    
  };

  // TODO: Implement decrement handler clamped to MIN (-10)
  const handleDecrement = (): void => {
    
  };

  // TODO: Implement reset handler restoring count to 0
  const handleReset = (): void => {
    
  };

  return (
    <div className="counter-container">
      <h2>Counter</h2>
      <div className="value-display">
        <span id="counter-value">{count}</span>
      </div>
      <div className="step-control">
        <label>Step: </label>
        <input 
          id="input-step" 
          type="number" 
          value={step} 
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setStep(Number(e.target.value) || 1)} 
        />
      </div>
      <div className="button-group">
        <button id="btn-decrement" onClick={handleDecrement} disabled={count <= MIN}>-</button>
        <button id="btn-reset" onClick={handleReset}>Reset</button>
        <button id="btn-increment" onClick={handleIncrement} disabled={count >= MAX}>+</button>
      </div>
    </div>
  );
}
""",
            "index.css": """.counter-container {
  max-width: 320px;
  margin: 20px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  text-align: center;
  color: #fafafa;
}
.value-display {
  font-size: 48px;
  font-weight: bold;
  color: #38bdf8;
  margin: 16px 0;
}
.step-control { margin-bottom: 16px; font-size: 14px; }
.step-control input { width: 60px; padding: 4px 8px; background: #09090b; border: 1px solid #3f3f46; color: #fff; border-radius: 6px; text-align: center; }
.button-group button { padding: 8px 16px; margin: 0 4px; border: 1px solid #3f3f46; background: #27272a; color: #fff; border-radius: 6px; cursor: pointer; }
.button-group button:disabled { opacity: 0.4; cursor: not-allowed; }
"""
        },
        "test_cases": [
            {
                "id": "react-counter-tc-1",
                "name": "Initial Render & Basic Increment/Decrement",
                "stdin": json.dumps({
                    "evaluation": """
                    const valEl = document.getElementById('counter-value');
                    const btnInc = document.getElementById('btn-increment');
                    const btnDec = document.getElementById('btn-decrement');
                    if (!valEl || !btnInc || !btnDec) return "FAIL: Required elements missing";
                    if (valEl.textContent.trim() !== "0") return "FAIL: Initial count should be 0";
                    btnInc.click();
                    await new Promise(r => setTimeout(r, 60));
                    if (valEl.textContent.trim() !== "1") return "FAIL: Count should be 1 after increment";
                    btnDec.click();
                    await new Promise(r => setTimeout(r, 60));
                    if (valEl.textContent.trim() !== "0") return "FAIL: Count should be 0 after decrement";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            },
            {
                "id": "react-counter-tc-2",
                "name": "Step Adjustment & Max Boundary Clamping",
                "stdin": json.dumps({
                    "evaluation": """
                    const valEl = document.getElementById('counter-value');
                    const btnInc = document.getElementById('btn-increment');
                    const btnReset = document.getElementById('btn-reset');
                    const stepInput = document.getElementById('input-step');
                    btnReset.click();
                    await new Promise(r => setTimeout(r, 60));
                    stepInput.value = "4";
                    stepInput.dispatchEvent(new Event('input', { bubbles: true }));
                    stepInput.dispatchEvent(new Event('change', { bubbles: true }));
                    await new Promise(r => setTimeout(r, 60));
                    btnInc.click();
                    await new Promise(r => setTimeout(r, 60));
                    btnInc.click();
                    await new Promise(r => setTimeout(r, 60));
                    btnInc.click();
                    await new Promise(r => setTimeout(r, 60));
                    if (Number(valEl.textContent.trim()) > 10) return "FAIL: Count exceeded max limit 10";
                    if (!btnInc.disabled) return "FAIL: Increment button should be disabled at max limit";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Dynamic Todo List with Filters & Completion",
        "slug": "react-dynamic-todo-list-filters",
        "short_description": "Build a feature-complete Todo manager supporting task addition, filter tabs, completion toggles, and deletion.",
        "difficulty": "Medium",
        "xp_reward": 150,
        "description": """### Dynamic Todo List with Filters & Completion

Implement a fully functional Todo application in React with item creation, completion toggling, deletion, and active/completed status filtering.

---
#### Component Requirements
1. Provide `<input id="todo-input" placeholder="What needs to be done?" />` and `<button id="todo-add">Add</button>`.
2. Pressing Enter or clicking Add appends a new item to `<ul id="todo-list">`.
3. Each todo item `<li className="todo-item">` must contain:
   - `<input type="checkbox" className="todo-checkbox" />` to toggle completion status.
   - `<span className="todo-text">{text}</span>` (adds CSS class `completed` when done).
   - `<button className="todo-delete">×</button>` to remove the item.
4. Filter tab buttons: `<button id="filter-all">All</button>`, `<button id="filter-active">Active</button>`, `<button id="filter-completed">Completed</button>`.
5. Footer showing `<span id="items-count">{activeCount} items left</span>`.
""",
        "starter_code": {
            "App.jsx": """import React, { useState } from 'react';

export default function App() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'Learn React Hooks', completed: true },
    { id: 2, text: 'Build production app', completed: false }
  ]);
  const [text, setText] = useState('');
  const [filter, setFilter] = useState('all');

  // TODO: Implement handleAdd to append a new item if text is non-empty
  const handleAdd = () => {
    
  };

  // TODO: Implement toggleTodo to toggle completed flag by id
  const toggleTodo = (id) => {
    
  };

  // TODO: Implement deleteTodo to remove item by id
  const deleteTodo = (id) => {
    
  };

  // TODO: Implement filteredTodos based on active filter ('all' | 'active' | 'completed')
  const filteredTodos = todos;

  // TODO: Implement activeCount of non-completed items
  const activeCount = 0;

  return (
    <div className="todo-container">
      <h2>Todo App</h2>
      <div className="todo-form">
        <input 
          id="todo-input" 
          value={text} 
          onChange={e => setText(e.target.value)} 
          onKeyDown={e => e.key === 'Enter' && handleAdd()}
          placeholder="What needs to be done?" 
        />
        <button id="todo-add" onClick={handleAdd}>Add</button>
      </div>

      <div className="filter-group">
        <button id="filter-all" className={filter === 'all' ? 'active' : ''} onClick={() => setFilter('all')}>All</button>
        <button id="filter-active" className={filter === 'active' ? 'active' : ''} onClick={() => setFilter('active')}>Active</button>
        <button id="filter-completed" className={filter === 'completed' ? 'active' : ''} onClick={() => setFilter('completed')}>Completed</button>
      </div>

      <ul id="todo-list">
        {filteredTodos.map(todo => (
          <li key={todo.id} className="todo-item">
            <input 
              type="checkbox" 
              className="todo-checkbox" 
              checked={todo.completed} 
              onChange={() => toggleTodo(todo.id)} 
            />
            <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>{todo.text}</span>
            <button className="todo-delete" onClick={() => deleteTodo(todo.id)}>×</button>
          </li>
        ))}
      </ul>

      <div className="todo-footer">
        <span id="items-count">{activeCount} items left</span>
      </div>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState } from 'react';

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

type Filter = 'all' | 'active' | 'completed';

export default function App(): JSX.Element {
  const [todos, setTodos] = useState<Todo[]>([
    { id: 1, text: 'Learn React Hooks', completed: true },
    { id: 2, text: 'Build production app', completed: false }
  ]);
  const [text, setText] = useState<string>('');
  const [filter, setFilter] = useState<Filter>('all');

  // TODO: Implement handleAdd to append a new item if text is non-empty
  const handleAdd = (): void => {
    
  };

  // TODO: Implement toggleTodo to toggle completed flag by id
  const toggleTodo = (id: number): void => {
    
  };

  // TODO: Implement deleteTodo to remove item by id
  const deleteTodo = (id: number): void => {
    
  };

  // TODO: Implement filteredTodos based on active filter ('all' | 'active' | 'completed')
  const filteredTodos: Todo[] = todos;

  // TODO: Implement activeCount of non-completed items
  const activeCount: number = 0;

  return (
    <div className="todo-container">
      <h2>Todo App</h2>
      <div className="todo-form">
        <input 
          id="todo-input" 
          value={text} 
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setText(e.target.value)} 
          onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === 'Enter' && handleAdd()}
          placeholder="What needs to be done?" 
        />
        <button id="todo-add" onClick={handleAdd}>Add</button>
      </div>

      <div className="filter-group">
        <button id="filter-all" className={filter === 'all' ? 'active' : ''} onClick={() => setFilter('all')}>All</button>
        <button id="filter-active" className={filter === 'active' ? 'active' : ''} onClick={() => setFilter('active')}>Active</button>
        <button id="filter-completed" className={filter === 'completed' ? 'active' : ''} onClick={() => setFilter('completed')}>Completed</button>
      </div>

      <ul id="todo-list">
        {filteredTodos.map(todo => (
          <li key={todo.id} className="todo-item">
            <input 
              type="checkbox" 
              className="todo-checkbox" 
              checked={todo.completed} 
              onChange={() => toggleTodo(todo.id)} 
            />
            <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>{todo.text}</span>
            <button className="todo-delete" onClick={() => deleteTodo(todo.id)}>×</button>
          </li>
        ))}
      </ul>

      <div className="todo-footer">
        <span id="items-count">{activeCount} items left</span>
      </div>
    </div>
  );
}
""",
            "index.css": """.todo-container {
  max-width: 440px;
  margin: 20px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  color: #fafafa;
}
.todo-form { display: flex; gap: 8px; margin-bottom: 16px; }
.todo-form input { flex: 1; padding: 10px; background: #09090b; border: 1px solid #3f3f46; border-radius: 6px; color: #fff; }
.todo-form button { padding: 10px 16px; background: #0284c7; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
.filter-group { display: flex; gap: 6px; margin-bottom: 16px; }
.filter-group button { padding: 6px 12px; background: #27272a; border: 1px solid #3f3f46; color: #a1a1aa; border-radius: 6px; cursor: pointer; }
.filter-group button.active { background: #38bdf8; color: #000; font-weight: bold; }
#todo-list { list-style: none; padding: 0; margin: 0; }
.todo-item { display: flex; align-items: center; justify-content: space-between; padding: 10px; border-bottom: 1px solid #27272a; }
.todo-text.completed { text-decoration: line-through; color: #71717a; }
.todo-delete { background: transparent; border: none; color: #ef4444; font-size: 20px; cursor: pointer; }
.todo-footer { margin-top: 16px; font-size: 13px; color: #a1a1aa; }
"""
        },
        "test_cases": [
            {
                "id": "react-todo-tc-1",
                "name": "Add Todo & Active Count Update",
                "stdin": json.dumps({
                    "evaluation": """
                    const input = document.getElementById('todo-input');
                    const addBtn = document.getElementById('todo-add');
                    input.value = "New Test Item";
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    await new Promise(r => setTimeout(r, 60));
                    addBtn.click();
                    await new Promise(r => setTimeout(r, 60));
                    const list = document.getElementById('todo-list');
                    if (!list.textContent.includes("New Test Item")) return "FAIL: Added item not in list";
                    const count = document.getElementById('items-count');
                    if (!count.textContent.includes("2 items left")) return "FAIL: Active items count mismatch";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            },
            {
                "id": "react-todo-tc-2",
                "name": "Filter Toggling & Item Deletion",
                "stdin": json.dumps({
                    "evaluation": """
                    const filterCompleted = document.getElementById('filter-completed');
                    filterCompleted.click();
                    await new Promise(r => setTimeout(r, 60));
                    const list = document.getElementById('todo-list');
                    if (list.children.length !== 1) return "FAIL: Filter completed should show 1 item";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Custom useDebounce Hook with Live Search",
        "slug": "react-custom-usedebounce-hook-live-search",
        "short_description": "Implement a custom useDebounce hook to delay state propagation and avoid excessive API querying.",
        "difficulty": "Medium",
        "xp_reward": 150,
        "description": """### Custom useDebounce Hook with Live Search

Build and demonstrate a reusable `useDebounce(value, delayMs)` hook that delays updating the debounced value until after the specified delay.

---
#### Component Requirements
1. Implement `useDebounce(value, delay = 300)`.
2. Input field `<input id="search-input" />`.
3. Element `<p id="immediate-value">Immediate: {text}</p>`.
4. Element `<p id="debounced-value">Debounced: {debouncedText}</p>`.
5. Typing in the input updates `#immediate-value` instantly, while `#debounced-value` only updates after 300ms has elapsed without new typing.
""",
        "starter_code": {
            "App.jsx": """import React, { useState, useEffect } from 'react';

// TODO: Implement custom useDebounce hook
export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  // TODO: Set up timer to update debouncedValue after delay ms and cleanup on value change

  return debouncedValue;
}

export default function App() {
  const [text, setText] = useState('');
  const debouncedText = useDebounce(text, 300);

  return (
    <div className="debounce-container">
      <h2>Live Search Debouncer</h2>
      <input 
        id="search-input" 
        value={text} 
        onChange={e => setText(e.target.value)} 
        placeholder="Type to search..." 
      />
      <div className="results-display">
        <p id="immediate-value">Immediate: {text}</p>
        <p id="debounced-value">Debounced: {debouncedText}</p>
      </div>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState, useEffect } from 'react';

// TODO: Implement custom useDebounce hook with TypeScript generics
export function useDebounce<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  // TODO: Set up timer to update debouncedValue after delay ms and cleanup on value change

  return debouncedValue;
}

export default function App(): JSX.Element {
  const [text, setText] = useState<string>('');
  const debouncedText = useDebounce<string>(text, 300);

  return (
    <div className="debounce-container">
      <h2>Live Search Debouncer</h2>
      <input 
        id="search-input" 
        value={text} 
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setText(e.target.value)} 
        placeholder="Type to search..." 
      />
      <div className="results-display">
        <p id="immediate-value">Immediate: {text}</p>
        <p id="debounced-value">Debounced: {debouncedText}</p>
      </div>
    </div>
  );
}
""",
            "index.css": """.debounce-container {
  max-width: 400px;
  margin: 24px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  color: #fafafa;
}
#search-input { width: 100%; padding: 10px; background: #09090b; border: 1px solid #3f3f46; border-radius: 6px; color: #fff; box-sizing: border-box; }
.results-display { margin-top: 16px; font-family: monospace; font-size: 14px; }
#immediate-value { color: #f59e0b; }
#debounced-value { color: #10b981; }
"""
        },
        "test_cases": [
            {
                "id": "react-debounce-tc-1",
                "name": "Immediate vs Debounced Propagation",
                "stdin": json.dumps({
                    "evaluation": """
                    const input = document.getElementById('search-input');
                    const imm = document.getElementById('immediate-value');
                    const deb = document.getElementById('debounced-value');
                    input.value = "React Query";
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    await new Promise(r => setTimeout(r, 60));
                    if (!imm.textContent.includes("React Query")) return "FAIL: Immediate value not updated";
                    await new Promise(r => setTimeout(r, 450));
                    if (!deb.textContent.includes("React Query")) return "FAIL: Debounced value not updated after delay";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Accordion Component with Mutex & Multi-Expand",
        "slug": "react-accordion-mutex-multiexpand",
        "short_description": "Build an accessible Accordion supporting single-panel (mutex) and multi-panel expand modes.",
        "difficulty": "Medium",
        "xp_reward": 150,
        "description": """### Accordion Component with Mutex & Multi-Expand

Build an Accordion component with configurable multi-expand capability and smooth toggles.

---
#### Component Requirements
1. Render list of accordion items with `<button className="accordion-header" id="header-{id}">{title}</button>`.
2. Content container `<div className="accordion-content" id="content-{id}">{content}</div>`.
3. Provide a checkbox `<input id="toggle-multi" type="checkbox" />` allowing multiple open panels simultaneously.
4. When `allowMultiple` is `false` (default): opening panel 2 must automatically close panel 1.
5. When `allowMultiple` is `true`: multiple panels can stay open at the same time.
""",
        "starter_code": {
            "App.jsx": """import React, { useState } from 'react';

const ITEMS = [
  { id: 1, title: 'What is React?', content: 'React is a JavaScript library for building user interfaces.' },
  { id: 2, title: 'What are Hooks?', content: 'Hooks let you use state and other React features without writing a class.' },
  { id: 3, title: 'Why Vite?', content: 'Vite provides an extremely fast development environment with ES modules.' }
];

export default function App() {
  const [openIds, setOpenIds] = useState([1]);
  const [allowMultiple, setAllowMultiple] = useState(false);

  // TODO: Implement toggleItem for single-panel mutex vs multi-expand mode
  const toggleItem = (id) => {
    
  };

  return (
    <div className="accordion-container">
      <h2>FAQ Accordion</h2>
      <label className="toggle-label">
        <input 
          id="toggle-multi" 
          type="checkbox" 
          checked={allowMultiple} 
          onChange={e => setAllowMultiple(e.target.checked)} 
        />
        Allow Multiple Open
      </label>

      <div className="accordion-list">
        {ITEMS.map(item => {
          const isOpen = openIds.includes(item.id);
          return (
            <div key={item.id} className="accordion-item">
              <button 
                id={`header-${item.id}`} 
                className={`accordion-header ${isOpen ? 'active' : ''}`}
                onClick={() => toggleItem(item.id)}
              >
                <span>{item.title}</span>
                <span className="arrow">{isOpen ? '▲' : '▼'}</span>
              </button>
              {isOpen && (
                <div id={`content-${item.id}`} className="accordion-content">
                  {item.content}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState } from 'react';

interface FAQItem {
  id: number;
  title: string;
  content: string;
}

const ITEMS: FAQItem[] = [
  { id: 1, title: 'What is React?', content: 'React is a JavaScript library for building user interfaces.' },
  { id: 2, title: 'What are Hooks?', content: 'Hooks let you use state and other React features without writing a class.' },
  { id: 3, title: 'Why Vite?', content: 'Vite provides an extremely fast development environment with ES modules.' }
];

export default function App(): JSX.Element {
  const [openIds, setOpenIds] = useState<number[]>([1]);
  const [allowMultiple, setAllowMultiple] = useState<boolean>(false);

  // TODO: Implement toggleItem for single-panel mutex vs multi-expand mode
  const toggleItem = (id: number): void => {
    
  };

  return (
    <div className="accordion-container">
      <h2>FAQ Accordion</h2>
      <label className="toggle-label">
        <input 
          id="toggle-multi" 
          type="checkbox" 
          checked={allowMultiple} 
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setAllowMultiple(e.target.checked)} 
        />
        Allow Multiple Open
      </label>

      <div className="accordion-list">
        {ITEMS.map(item => {
          const isOpen = openIds.includes(item.id);
          return (
            <div key={item.id} className="accordion-item">
              <button 
                id={`header-${item.id}`} 
                className={`accordion-header ${isOpen ? 'active' : ''}`}
                onClick={() => toggleItem(item.id)}
              >
                <span>{item.title}</span>
                <span className="arrow">{isOpen ? '▲' : '▼'}</span>
              </button>
              {isOpen && (
                <div id={`content-${item.id}`} className="accordion-content">
                  {item.content}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
""",
            "index.css": """.accordion-container {
  max-width: 480px;
  margin: 20px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  color: #fafafa;
}
.toggle-label { display: flex; align-items: center; gap: 8px; font-size: 13px; margin-bottom: 16px; color: #a1a1aa; cursor: pointer; }
.accordion-item { border: 1px solid #27272a; border-radius: 8px; margin-bottom: 8px; overflow: hidden; }
.accordion-header { width: 100%; display: flex; justify-content: space-between; padding: 12px 16px; background: #27272a; border: none; color: #fff; font-weight: 500; font-size: 14px; cursor: pointer; text-align: left; }
.accordion-header.active { background: #3f3f46; }
.accordion-content { padding: 16px; background: #09090b; font-size: 13px; color: #d4d4d8; line-height: 1.5; }
"""
        },
        "test_cases": [
            {
                "id": "react-accordion-tc-1",
                "name": "Mutex Accordion Single Open Panel",
                "stdin": json.dumps({
                    "evaluation": """
                    const h2 = document.getElementById('header-2');
                    h2.click();
                    await new Promise(r => setTimeout(r, 60));
                    const c1 = document.getElementById('content-1');
                    const c2 = document.getElementById('content-2');
                    if (c1) return "FAIL: Panel 1 should close when Panel 2 opens in mutex mode";
                    if (!c2) return "FAIL: Panel 2 should be open";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Theme Switcher with React Context API",
        "slug": "react-theme-switcher-context-api",
        "short_description": "Implement global theme state management (Light/Dark) using createContext and useContext.",
        "difficulty": "Easy",
        "xp_reward": 100,
        "description": """### Theme Switcher with React Context API

Create a React ThemeContext that provides `{ theme, toggleTheme }` to all child components.

---
#### Component Requirements
1. Create `ThemeContext = React.createContext()`.
2. Wrap app with `<ThemeProvider>`.
3. Provide `<button id="btn-theme-toggle">Switch Theme</button>`.
4. Render current theme indicator inside `<span id="theme-label">{theme}</span>`.
5. Top-level wrapper element `<div id="theme-container" className={theme}>`.
6. Clicking toggle switches between `"dark"` and `"light"`.
""",
        "starter_code": {
            "App.jsx": """import React, { createContext, useContext, useState } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('dark');

  // TODO: Implement toggleTheme between 'dark' and 'light'
  const toggleTheme = () => {
    
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function ThemeContent() {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <div id="theme-container" className={`theme-box ${theme}`}>
      <h2>Theme Context</h2>
      <p>Current Theme: <span id="theme-label">{theme}</span></p>
      <button id="btn-theme-toggle" onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <ThemeContent />
    </ThemeProvider>
  );
}
""",
            "App.tsx": """import React, { createContext, useContext, useState, ReactNode } from 'react';

type Theme = 'dark' | 'light';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }): JSX.Element {
  const [theme, setTheme] = useState<Theme>('dark');

  // TODO: Implement toggleTheme between 'dark' and 'light'
  const toggleTheme = (): void => {
    
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function ThemeContent(): JSX.Element {
  const context = useContext(ThemeContext);
  const theme = context?.theme || 'dark';
  const toggleTheme = context?.toggleTheme || (() => {});

  return (
    <div id="theme-container" className={`theme-box ${theme}`}>
      <h2>Theme Context</h2>
      <p>Current Theme: <span id="theme-label">{theme}</span></p>
      <button id="btn-theme-toggle" onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
}

export default function App(): JSX.Element {
  return (
    <ThemeProvider>
      <ThemeContent />
    </ThemeProvider>
  );
}
""",
            "index.css": """.theme-box {
  max-width: 360px;
  margin: 30px auto;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
}
.theme-box.dark {
  background: #18181b;
  border: 1px solid #27272a;
  color: #fafafa;
}
.theme-box.light {
  background: #f4f4f5;
  border: 1px solid #e4e4e7;
  color: #18181b;
}
button {
  padding: 8px 16px;
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 12px;
}
"""
        },
        "test_cases": [
            {
                "id": "react-theme-tc-1",
                "name": "Theme Toggle & Class Synchronization",
                "stdin": json.dumps({
                    "evaluation": """
                    const label = document.getElementById('theme-label');
                    const btn = document.getElementById('btn-theme-toggle');
                    const container = document.getElementById('theme-container');
                    if (label.textContent.trim() !== "dark") return "FAIL: Initial theme should be dark";
                    btn.click();
                    await new Promise(r => setTimeout(r, 60));
                    if (label.textContent.trim() !== "light") return "FAIL: Theme should toggle to light";
                    if (!container.classList.contains("light")) return "FAIL: Container should have light class";
                    btn.click();
                    await new Promise(r => setTimeout(r, 60));
                    if (label.textContent.trim() !== "dark") return "FAIL: Theme should toggle back to dark";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Star Rating Component with Hover Feedback",
        "slug": "react-star-rating-hover-feedback",
        "short_description": "Build an interactive 5-star rating widget with hover previews and click selection.",
        "difficulty": "Easy",
        "xp_reward": 100,
        "description": """### Star Rating Component with Hover Feedback

Create a 5-star rating input with interactive mouseover previews and permanent rating selection.

---
#### Component Requirements
1. Render 5 star buttons with `<button className="star-btn" data-star="{index}">★</button>` (indices 1 to 5).
2. Display selected rating in `<span id="rating-score">{rating} / 5</span>`.
3. Mouseover on star index $K$ highlights stars 1 through $K$ with the class `hovered` or `filled`.
4. Click on star index $K$ commits rating $K$.
5. Mouseleave resets the visual highlight back to the committed rating.
""",
        "starter_code": {
            "App.jsx": """import React, { useState } from 'react';

export default function App() {
  const [rating, setRating] = useState(0);
  const [hover, setHover] = useState(0);

  // TODO: Handle hover and selection states for star ratings 1 to 5

  return (
    <div className="rating-container">
      <h2>Rate Your Experience</h2>
      <div className="stars-wrapper" onMouseLeave={() => setHover(0)}>
        {[1, 2, 3, 4, 5].map((star) => {
          const isFilled = (hover || rating) >= star;
          return (
            <button
              key={star}
              className={`star-btn ${isFilled ? 'filled' : ''}`}
              data-star={star}
              onClick={() => setRating(star)}
              onMouseEnter={() => setHover(star)}
            >
              ★
            </button>
          );
        })}
      </div>
      <div className="rating-label">
        <span id="rating-score">{rating} / 5</span>
      </div>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState } from 'react';

export default function App(): JSX.Element {
  const [rating, setRating] = useState<number>(0);
  const [hover, setHover] = useState<number>(0);

  // TODO: Handle hover and selection states for star ratings 1 to 5

  return (
    <div className="rating-container">
      <h2>Rate Your Experience</h2>
      <div className="stars-wrapper" onMouseLeave={() => setHover(0)}>
        {[1, 2, 3, 4, 5].map((star: number) => {
          const isFilled = (hover || rating) >= star;
          return (
            <button
              key={star}
              className={`star-btn ${isFilled ? 'filled' : ''}`}
              data-star={star}
              onClick={() => setRating(star)}
              onMouseEnter={() => setHover(star)}
            >
              ★
            </button>
          );
        })}
      </div>
      <div className="rating-label">
        <span id="rating-score">{rating} / 5</span>
      </div>
    </div>
  );
}
""",
            "index.css": """.rating-container {
  max-width: 320px;
  margin: 30px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  text-align: center;
  color: #fafafa;
}
.stars-wrapper { display: flex; justify-content: center; gap: 8px; margin: 16px 0; }
.star-btn {
  background: transparent;
  border: none;
  font-size: 32px;
  color: #3f3f46;
  cursor: pointer;
  transition: color 0.15s ease;
}
.star-btn.filled { color: #f59e0b; }
.rating-label { font-size: 16px; font-weight: bold; color: #a1a1aa; }
"""
        },
        "test_cases": [
            {
                "id": "react-stars-tc-1",
                "name": "Click Rating Selection",
                "stdin": json.dumps({
                    "evaluation": """
                    const stars = document.querySelectorAll('.star-btn');
                    if (stars.length !== 5) return "FAIL: Should render 5 star buttons";
                    stars[3].click(); // click star 4
                    await new Promise(r => setTimeout(r, 60));
                    const score = document.getElementById('rating-score');
                    if (!score.textContent.includes("4 / 5")) return "FAIL: Score should be 4 / 5";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Stopwatch with Lap Split Times",
        "slug": "react-stopwatch-lap-split-times",
        "short_description": "Build a high-precision stopwatch with start, pause, reset, and lap record tracking.",
        "difficulty": "Medium",
        "xp_reward": 150,
        "description": """### Stopwatch with Lap Split Times

Build a real-time Stopwatch component displaying milliseconds and logging split lap records.

---
#### Component Requirements
1. Render formatted elapsed time inside `<div id="time-display">MM:SS.cc</div>`.
2. Provide `<button id="btn-start-pause">Start / Pause</button>`.
3. Provide `<button id="btn-lap">Lap</button>`.
4. Provide `<button id="btn-reset">Reset</button>`.
5. Clicking Lap appends a record row to `<ul id="laps-list">`.
6. Reset clears elapsed time back to `00:00.00` and empties the laps list.
""",
        "starter_code": {
            "App.jsx": """import React, { useState, useEffect, useRef } from 'react';

export default function App() {
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [laps, setLaps] = useState([]);
  const timerRef = useRef(null);

  // TODO: Implement setInterval timer effect when isRunning is true

  // TODO: Implement handleStartPause toggle
  const handleStartPause = () => {
    
  };

  // TODO: Implement handleReset
  const handleReset = () => {
    
  };

  // TODO: Implement handleLap recording
  const handleLap = () => {
    
  };

  const formatTime = (ms) => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    const centis = Math.floor((ms % 1000) / 10);
    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(centis).padStart(2, '0')}`;
  };

  return (
    <div className="stopwatch-container">
      <h2>Stopwatch</h2>
      <div id="time-display">{formatTime(time)}</div>
      <div className="controls">
        <button id="btn-start-pause" onClick={handleStartPause}>{isRunning ? 'Pause' : 'Start'}</button>
        <button id="btn-lap" onClick={handleLap} disabled={!isRunning}>Lap</button>
        <button id="btn-reset" onClick={handleReset}>Reset</button>
      </div>
      <ul id="laps-list">
        {laps.map((lap, idx) => (
          <li key={idx} className="lap-item">
            <span>Lap #{laps.length - idx}</span>
            <span>{lap}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState, useEffect, useRef } from 'react';

export default function App(): JSX.Element {
  const [time, setTime] = useState<number>(0);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [laps, setLaps] = useState<string[]>([]);
  const timerRef = useRef<any>(null);

  // TODO: Implement setInterval timer effect when isRunning is true

  // TODO: Implement handleStartPause toggle
  const handleStartPause = (): void => {
    
  };

  // TODO: Implement handleReset
  const handleReset = (): void => {
    
  };

  // TODO: Implement handleLap recording
  const handleLap = (): void => {
    
  };

  const formatTime = (ms: number): string => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    const centis = Math.floor((ms % 1000) / 10);
    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(centis).padStart(2, '0')}`;
  };

  return (
    <div className="stopwatch-container">
      <h2>Stopwatch</h2>
      <div id="time-display">{formatTime(time)}</div>
      <div className="controls">
        <button id="btn-start-pause" onClick={handleStartPause}>{isRunning ? 'Pause' : 'Start'}</button>
        <button id="btn-lap" onClick={handleLap} disabled={!isRunning}>Lap</button>
        <button id="btn-reset" onClick={handleReset}>Reset</button>
      </div>
      <ul id="laps-list">
        {laps.map((lap: string, idx: number) => (
          <li key={idx} className="lap-item">
            <span>Lap #{laps.length - idx}</span>
            <span>{lap}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
""",
            "index.css": """.stopwatch-container {
  max-width: 360px;
  margin: 20px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  text-align: center;
  color: #fafafa;
}
#time-display { font-size: 40px; font-family: monospace; font-weight: bold; color: #38bdf8; margin: 20px 0; }
.controls button { padding: 8px 16px; margin: 0 4px; border: 1px solid #3f3f46; background: #27272a; color: #fff; border-radius: 6px; cursor: pointer; }
#laps-list { list-style: none; padding: 0; margin-top: 20px; max-height: 160px; overflow-y: auto; }
.lap-item { display: flex; justify-content: space-between; padding: 6px 12px; border-bottom: 1px solid #27272a; font-family: monospace; font-size: 13px; color: #a1a1aa; }
"""
        },
        "test_cases": [
            {
                "id": "react-stopwatch-tc-1",
                "name": "Timer Start & Elapsed Progress",
                "stdin": json.dumps({
                    "evaluation": """
                    const btnStart = document.getElementById('btn-start-pause');
                    const display = document.getElementById('time-display');
                    btnStart.click();
                    await new Promise(r => setTimeout(r, 150));
                    btnStart.click();
                    await new Promise(r => setTimeout(r, 60));
                    if (display.textContent.trim() === "00:00.00") return "FAIL: Time should advance after start";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Modal Dialog with Keyboard Escape & Focus Trap",
        "slug": "react-modal-dialog-keyboard-escape",
        "short_description": "Build an accessible Modal overlay component with Escape key listener and backdrop dismissal.",
        "difficulty": "Hard",
        "xp_reward": 200,
        "description": """### Modal Dialog with Keyboard Escape & Focus Trap

Build a resilient Modal dialog component with backdrop blur, Escape key dismissal, and backdrop click listener.

---
#### Component Requirements
1. Trigger button `<button id="btn-open-modal">Open Modal</button>`.
2. When open, render overlay `<div id="modal-overlay" className="modal-backdrop">`.
3. Modal content `<div id="modal-box" role="dialog">`.
4. Close button inside dialog `<button id="btn-close-modal">Close</button>`.
5. Pressing the `Escape` keyboard key or clicking `#modal-overlay` closes the modal.
""",
        "starter_code": {
            "App.jsx": """import React, { useState, useEffect } from 'react';

export default function App() {
  const [isOpen, setIsOpen] = useState(false);

  // TODO: Add keydown event listener for 'Escape' key when modal is open

  return (
    <div className="app-container">
      <h2>Modal Dialog Demo</h2>
      <button id="btn-open-modal" onClick={() => setIsOpen(true)}>Open Modal</button>

      {isOpen && (
        <div id="modal-overlay" className="modal-backdrop" onClick={() => setIsOpen(false)}>
          <div id="modal-box" role="dialog" onClick={e => e.stopPropagation()}>
            <h3>Confirmation Required</h3>
            <p>Are you sure you want to proceed with this operation?</p>
            <div className="modal-actions">
              <button id="btn-close-modal" onClick={() => setIsOpen(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
""",
            "App.tsx": """import React, { useState, useEffect } from 'react';

export default function App(): JSX.Element {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  // TODO: Add keydown event listener for 'Escape' key when modal is open

  return (
    <div className="app-container">
      <h2>Modal Dialog Demo</h2>
      <button id="btn-open-modal" onClick={() => setIsOpen(true)}>Open Modal</button>

      {isOpen && (
        <div id="modal-overlay" className="modal-backdrop" onClick={() => setIsOpen(false)}>
          <div id="modal-box" role="dialog" onClick={(e: React.MouseEvent) => e.stopPropagation()}>
            <h3>Confirmation Required</h3>
            <p>Are you sure you want to proceed with this operation?</p>
            <div className="modal-actions">
              <button id="btn-close-modal" onClick={() => setIsOpen(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
""",
            "index.css": """.app-container { text-align: center; padding: 40px; color: #fff; }
#btn-open-modal { padding: 10px 20px; background: #0284c7; border: none; color: #fff; border-radius: 8px; cursor: pointer; font-size: 14px; }
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 50; }
#modal-box { background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 24px; max-width: 400px; width: 90%; color: #fff; }
.modal-actions { display: flex; justify-content: flex-end; margin-top: 20px; }
#btn-close-modal { padding: 8px 16px; background: #ef4444; border: none; color: #fff; border-radius: 6px; cursor: pointer; }
"""
        },
        "test_cases": [
            {
                "id": "react-modal-tc-1",
                "name": "Open, Backdrop & Escape Key Dismissal",
                "stdin": json.dumps({
                    "evaluation": """
                    const openBtn = document.getElementById('btn-open-modal');
                    openBtn.click();
                    await new Promise(r => setTimeout(r, 60));
                    let modal = document.getElementById('modal-box');
                    if (!modal) return "FAIL: Modal should be open after click";
                    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
                    await new Promise(r => setTimeout(r, 60));
                    modal = document.getElementById('modal-box');
                    if (modal) return "FAIL: Modal should close on Escape key";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Shopping Cart with Price & Quantity Calculations",
        "slug": "react-shopping-cart-price-calculations",
        "short_description": "Build an e-commerce shopping cart with quantity modifications, promo code discounts, and tax computation.",
        "difficulty": "Medium",
        "xp_reward": 150,
        "description": """### Shopping Cart with Price & Quantity Calculations

Build a reactive shopping cart summary calculating item subtotals, tax, and discount codes.

---
#### Component Requirements
1. Render items in cart with quantity controls `<button className="btn-qty-inc">+</button>` and `<button className="btn-qty-dec">-</button>`.
2. Promo code input `<input id="input-promo" />` and `<button id="btn-apply-promo">Apply</button>`.
3. If promo code is `"SAVE10"`, apply a 10% discount on the subtotal.
4. Render `<span id="cart-subtotal">${subtotal}</span>`.
5. Render `<span id="cart-discount">${discount}</span>`.
6. Render `<span id="cart-total">${total}</span>`.
""",
        "starter_code": {
            "App.jsx": """import React, { useState } from 'react';

const INITIAL_ITEMS = [
  { id: 1, name: 'Mechanical Keyboard', price: 120, quantity: 1 },
  { id: 2, name: 'Wireless Mouse', price: 60, quantity: 2 }
];

export default function App() {
  const [items, setItems] = useState(INITIAL_ITEMS);
  const [promo, setPromo] = useState('');
  const [discountPercent, setDiscountPercent] = useState(0);

  // TODO: Implement updateQty to adjust quantity (minimum 1)
  const updateQty = (id, delta) => {
    
  };

  // TODO: Implement handleApplyPromo ('SAVE10' -> 10% discount)
  const handleApplyPromo = () => {
    
  };

  // TODO: Calculate subtotal, discount, and total
  const subtotal = 0;
  const discount = 0;
  const total = 0;

  return (
    <div className="cart-container">
      <h2>Shopping Cart</h2>
      <div className="items-list">
        {items.map(item => (
          <div key={item.id} className="cart-item">
            <span className="item-name">{item.name} (${item.price})</span>
            <div className="item-qty-controls">
              <button className="btn-qty-dec" onClick={() => updateQty(item.id, -1)}>-</button>
              <span className="qty-val">{item.quantity}</span>
              <button className="btn-qty-inc" onClick={() => updateQty(item.id, 1)}>+</button>
            </div>
          </div>
        ))}
      </div>

      <div className="promo-section">
        <input 
          id="input-promo" 
          value={promo} 
          onChange={e => setPromo(e.target.value)} 
          placeholder="Promo code (SAVE10)" 
        />
        <button id="btn-apply-promo" onClick={handleApplyPromo}>Apply</button>
      </div>

      <div className="summary-box">
        <p>Subtotal: <span id="cart-subtotal">${subtotal.toFixed(2)}</span></p>
        <p>Discount: <span id="cart-discount">${discount.toFixed(2)}</span></p>
        <h3>Total: <span id="cart-total">${total.toFixed(2)}</span></h3>
      </div>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState } from 'react';

interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

const INITIAL_ITEMS: CartItem[] = [
  { id: 1, name: 'Mechanical Keyboard', price: 120, quantity: 1 },
  { id: 2, name: 'Wireless Mouse', price: 60, quantity: 2 }
];

export default function App(): JSX.Element {
  const [items, setItems] = useState<CartItem[]>(INITIAL_ITEMS);
  const [promo, setPromo] = useState<string>('');
  const [discountPercent, setDiscountPercent] = useState<number>(0);

  // TODO: Implement updateQty to adjust quantity (minimum 1)
  const updateQty = (id: number, delta: number): void => {
    
  };

  // TODO: Implement handleApplyPromo ('SAVE10' -> 10% discount)
  const handleApplyPromo = (): void => {
    
  };

  // TODO: Calculate subtotal, discount, and total
  const subtotal: number = 0;
  const discount: number = 0;
  const total: number = 0;

  return (
    <div className="cart-container">
      <h2>Shopping Cart</h2>
      <div className="items-list">
        {items.map(item => (
          <div key={item.id} className="cart-item">
            <span className="item-name">{item.name} (${item.price})</span>
            <div className="item-qty-controls">
              <button className="btn-qty-dec" onClick={() => updateQty(item.id, -1)}>-</button>
              <span className="qty-val">{item.quantity}</span>
              <button className="btn-qty-inc" onClick={() => updateQty(item.id, 1)}>+</button>
            </div>
          </div>
        ))}
      </div>

      <div className="promo-section">
        <input 
          id="input-promo" 
          value={promo} 
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPromo(e.target.value)} 
          placeholder="Promo code (SAVE10)" 
        />
        <button id="btn-apply-promo" onClick={handleApplyPromo}>Apply</button>
      </div>

      <div className="summary-box">
        <p>Subtotal: <span id="cart-subtotal">${subtotal.toFixed(2)}</span></p>
        <p>Discount: <span id="cart-discount">${discount.toFixed(2)}</span></p>
        <h3>Total: <span id="cart-total">${total.toFixed(2)}</span></h3>
      </div>
    </div>
  );
}
""",
            "index.css": """.cart-container {
  max-width: 420px;
  margin: 20px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  color: #fafafa;
}
.cart-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #27272a; }
.item-qty-controls button { padding: 2px 8px; background: #27272a; border: 1px solid #3f3f46; color: #fff; border-radius: 4px; cursor: pointer; }
.qty-val { margin: 0 8px; font-weight: bold; }
.promo-section { display: flex; gap: 8px; margin: 16px 0; }
.promo-section input { flex: 1; padding: 8px; background: #09090b; border: 1px solid #3f3f46; color: #fff; border-radius: 6px; }
.promo-section button { padding: 8px 14px; background: #3b82f6; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
.summary-box { background: #09090b; padding: 16px; border-radius: 8px; margin-top: 12px; }
.summary-box p, .summary-box h3 { margin: 4px 0; display: flex; justify-content: space-between; }
#cart-total { color: #10b981; }
"""
        },
        "test_cases": [
            {
                "id": "react-cart-tc-1",
                "name": "Subtotal Calculation & Promo Code Discount",
                "stdin": json.dumps({
                    "evaluation": """
                    const subtotal = document.getElementById('cart-subtotal');
                    if (!subtotal.textContent.includes("240.00")) return "FAIL: Initial subtotal should be $240.00";
                    const promoInput = document.getElementById('input-promo');
                    const applyBtn = document.getElementById('btn-apply-promo');
                    promoInput.value = "SAVE10";
                    promoInput.dispatchEvent(new Event('input', { bubbles: true }));
                    await new Promise(r => setTimeout(r, 60));
                    applyBtn.click();
                    await new Promise(r => setTimeout(r, 60));
                    const total = document.getElementById('cart-total');
                    if (!total.textContent.includes("216.00")) return "FAIL: Total after 10% discount should be $216.00";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Tabs Navigation with Dynamic Panels & ARIA",
        "slug": "react-tabs-navigation-dynamic-panels",
        "short_description": "Build an accessible Tab navigation component supporting active panel switching and ARIA roles.",
        "difficulty": "Easy",
        "xp_reward": 100,
        "description": """### Tabs Navigation with Dynamic Panels & ARIA

Create a clean Tabbed interface with dynamic panel switching and accessible ARIA attributes.

---
#### Component Requirements
1. Render tab buttons `<button role="tab" id="tab-{id}">{label}</button>`.
2. Active tab must have attribute `aria-selected="true"`.
3. Render active tab panel `<div role="tabpanel" id="panel-{id}">{content}</div>`.
4. Clicking tab button 2 switches active state and renders panel 2 content.
""",
        "starter_code": {
            "App.jsx": """import React, { useState } from 'react';

const TABS = [
  { id: 'profile', label: 'Profile', content: 'Manage your user profile details and avatar.' },
  { id: 'security', label: 'Security', content: 'Configure 2FA and manage your active login sessions.' },
  { id: 'billing', label: 'Billing', content: 'View recent invoices and update credit card details.' }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('profile');

  // TODO: Implement active tab lookup and tab switching
  const currentTab = TABS.find(t => t.id === activeTab) || TABS[0];

  return (
    <div className="tabs-container">
      <h2>Account Settings</h2>
      <div role="tablist" className="tab-buttons">
        {TABS.map(tab => (
          <button
            key={tab.id}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div role="tabpanel" id={`panel-${currentTab.id}`} className="tab-panel">
        {currentTab.content}
      </div>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState } from 'react';

interface TabItem {
  id: string;
  label: string;
  content: string;
}

const TABS: TabItem[] = [
  { id: 'profile', label: 'Profile', content: 'Manage your user profile details and avatar.' },
  { id: 'security', label: 'Security', content: 'Configure 2FA and manage your active login sessions.' },
  { id: 'billing', label: 'Billing', content: 'View recent invoices and update credit card details.' }
];

export default function App(): JSX.Element {
  const [activeTab, setActiveTab] = useState<string>('profile');

  // TODO: Implement active tab lookup and tab switching
  const currentTab: TabItem = TABS.find(t => t.id === activeTab) || TABS[0];

  return (
    <div className="tabs-container">
      <h2>Account Settings</h2>
      <div role="tablist" className="tab-buttons">
        {TABS.map(tab => (
          <button
            key={tab.id}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div role="tabpanel" id={`panel-${currentTab.id}`} className="tab-panel">
        {currentTab.content}
      </div>
    </div>
  );
}
""",
            "index.css": """.tabs-container {
  max-width: 440px;
  margin: 20px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  color: #fafafa;
}
.tab-buttons { display: flex; border-bottom: 1px solid #27272a; gap: 4px; }
.tab-btn { padding: 8px 16px; background: transparent; border: none; border-bottom: 2px solid transparent; color: #a1a1aa; cursor: pointer; font-size: 14px; }
.tab-btn.active { color: #38bdf8; border-bottom-color: #38bdf8; font-weight: bold; }
.tab-panel { padding: 20px 0; font-size: 14px; color: #d4d4d8; line-height: 1.6; }
"""
        },
        "test_cases": [
            {
                "id": "react-tabs-tc-1",
                "name": "Tab Switching & ARIA Selected State",
                "stdin": json.dumps({
                    "evaluation": """
                    const tabSec = document.getElementById('tab-security');
                    tabSec.click();
                    await new Promise(r => setTimeout(r, 60));
                    const panel = document.getElementById('panel-security');
                    if (!panel || !panel.textContent.includes("2FA")) return "FAIL: Security panel not rendered";
                    if (tabSec.getAttribute('aria-selected') !== 'true') return "FAIL: aria-selected should be true";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    },
    {
        "title": "Password Strength Meter & Live Validator",
        "slug": "react-password-strength-meter-validator",
        "short_description": "Build a live password strength analyzer validating length, numbers, uppercase, and special symbols.",
        "difficulty": "Easy",
        "xp_reward": 100,
        "description": """### Password Strength Meter & Live Validator

Implement a real-time password security meter checking essential complexity requirements.

---
#### Component Requirements
1. Password input `<input id="password-input" type="password" />`.
2. Strength bar `<div id="strength-meter" className="{weak|medium|strong}">`.
3. Requirement list items:
   - `<li id="req-length">At least 8 characters</li>`
   - `<li id="req-number">Contains a number</li>`
   - `<li id="req-special">Contains a special character (!@#$)</li>`
4. Met requirements receive class `valid`.
""",
        "starter_code": {
            "App.jsx": """import React, { useState } from 'react';

export default function App() {
  const [password, setPassword] = useState('');

  // TODO: Validate requirements: length >= 8, has number, has special char
  const hasLength = false;
  const hasNumber = false;
  const hasSpecial = false;

  const score = [hasLength, hasNumber, hasSpecial].filter(Boolean).length;
  const strengthClass = score === 3 ? 'strong' : score === 2 ? 'medium' : score >= 1 ? 'weak' : 'empty';

  return (
    <div className="password-container">
      <h2>Create Password</h2>
      <input 
        id="password-input" 
        type="password" 
        value={password} 
        onChange={e => setPassword(e.target.value)} 
        placeholder="Enter password..." 
      />
      <div id="strength-meter" className={`meter-bar ${strengthClass}`} />
      
      <ul className="requirements-list">
        <li id="req-length" className={hasLength ? 'valid' : ''}>At least 8 characters</li>
        <li id="req-number" className={hasNumber ? 'valid' : ''}>Contains a number</li>
        <li id="req-special" className={hasSpecial ? 'valid' : ''}>Contains a special character</li>
      </ul>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState } from 'react';

export default function App(): JSX.Element {
  const [password, setPassword] = useState<string>('');

  // TODO: Validate requirements: length >= 8, has number, has special char
  const hasLength: boolean = false;
  const hasNumber: boolean = false;
  const hasSpecial: boolean = false;

  const score: number = [hasLength, hasNumber, hasSpecial].filter(Boolean).length;
  const strengthClass: string = score === 3 ? 'strong' : score === 2 ? 'medium' : score >= 1 ? 'weak' : 'empty';

  return (
    <div className="password-container">
      <h2>Create Password</h2>
      <input 
        id="password-input" 
        type="password" 
        value={password} 
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)} 
        placeholder="Enter password..." 
      />
      <div id="strength-meter" className={`meter-bar ${strengthClass}`} />
      
      <ul className="requirements-list">
        <li id="req-length" className={hasLength ? 'valid' : ''}>At least 8 characters</li>
        <li id="req-number" className={hasNumber ? 'valid' : ''}>Contains a number</li>
        <li id="req-special" className={hasSpecial ? 'valid' : ''}>Contains a special character</li>
      </ul>
    </div>
  );
}
""",
            "index.css": """.password-container {
  max-width: 360px;
  margin: 20px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  color: #fafafa;
}
#password-input { width: 100%; padding: 10px; background: #09090b; border: 1px solid #3f3f46; border-radius: 6px; color: #fff; box-sizing: border-box; }
.meter-bar { height: 6px; border-radius: 3px; margin: 12px 0; background: #27272a; transition: all 0.3s; }
.meter-bar.weak { background: #ef4444; width: 33%; }
.meter-bar.medium { background: #f59e0b; width: 66%; }
.meter-bar.strong { background: #10b981; width: 100%; }
.requirements-list { list-style: none; padding: 0; font-size: 13px; color: #71717a; margin-top: 16px; }
.requirements-list li { margin: 6px 0; }
.requirements-list li.valid { color: #10b981; font-weight: 500; }
"""
        },
        "test_cases": [
            {
                "id": "react-pwd-tc-1",
                "name": "Password Strength Validation Rules",
                "stdin": json.dumps({
                    "evaluation": """
                    const input = document.getElementById('password-input');
                    const reqLen = document.getElementById('req-length');
                    const reqNum = document.getElementById('req-number');
                    const reqSpec = document.getElementById('req-special');
                    input.value = "StrongP@ss1";
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    await new Promise(r => setTimeout(r, 60));
                    if (!reqLen.classList.contains('valid')) return "FAIL: Length should be valid";
                    if (!reqNum.classList.contains('valid')) return "FAIL: Number should be valid";
                    if (!reqSpec.classList.contains('valid')) return "FAIL: Special should be valid";
                    return "PASS";
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    }
]

# Generate 21 more structured React challenges (total 31)
MORE_REACT_TOPICS = [
    ("Autocomplete Search with Debounce", "Search list suggestions with debounced keystrokes and keyboard highlight.", "Medium"),
    ("Multi-Step Wizard Form", "Step-by-step registration wizard with per-step state validation.", "Hard"),
    ("Dynamic Chip / Tag Input", "Input tags on Enter/Comma with backspace removals and duplicates block.", "Medium"),
    ("Character Limit Word Counter", "Live textarea counter with visual alerts when approaching limit.", "Easy"),
    ("Annual vs Monthly Price Toggle", "Interactive tier pricing calculator with seat count slider.", "Easy"),
    ("Color Palette Swatch Generator", "Randomize hex color palettes with lockable swatch states.", "Medium"),
    ("Breadcrumbs Trail Component", "Generate navigational breadcrumb links dynamically from URL path.", "Easy"),
    ("Custom usePrevious Hook", "Store and compare immediate previous render values with ref.", "Medium"),
    ("Custom useOnClickOutside Hook", "Dismiss floating dropdown menus when clicking outside boundary.", "Medium"),
    ("Data Fetcher with Skeletons", "Render loading skeletons, resolved data cards, and retry triggers.", "Medium"),
    ("Dual Transfer List Box", "Move selected items across left and right lists with action buttons.", "Medium"),
    ("Tree View Directory Navigator", "Nested collapsible directory tree with folder open/close toggles.", "Medium"),
    ("OTP 6-Digit Auto Focus", "6-box OTP entry auto-advancing focus on input and handling paste.", "Medium"),
    ("Toast Notification Queue", "Stacked toast notification system with auto-dismiss timers.", "Hard"),
    ("Markdown Live Editor Pane", "Two-pane editor translating Markdown input to HTML preview.", "Medium"),
    ("File Dropzone Drag and Drop", "Drag and drop file upload zone validating file types and sizes.", "Medium"),
    ("Infinite Scroll Sentinel", "IntersectionObserver sentinel triggering paginated list loads.", "Hard"),
    ("Virtualized List Window", "Render only visible slice of 10,000 row datasets based on scroll.", "Hard"),
    ("Kanban Drag Reorder Column", "Reorderable task column with priority tags and move actions.", "Hard"),
    ("Dark Mode System Sync", "Synchronize theme with prefers-color-scheme media queries.", "Easy"),
    ("Window Size Resize Hook", "Listen to window resize events with debounced dimension reporting.", "Easy")
]

for idx, (title, desc, diff) in enumerate(MORE_REACT_TOPICS):
    slug = f"react-{title.lower().replace(' ', '-').replace('/', '-')}"
    REACT_CHALLENGES.append({
        "title": title,
        "slug": slug,
        "short_description": desc,
        "difficulty": diff,
        "xp_reward": 100 if diff == "Easy" else (150 if diff == "Medium" else 200),
        "description": f"### {title}\n\n{desc}\n\nBuild a production-grade, accessible React component adhering to React 18 standards.\n",
        "starter_code": {
            "App.jsx": """import React, { useState } from 'react';

export default function App() {
  const [value, setValue] = useState('');

  // TODO: Implement """ + title + """ component logic

  return (
    <div className="component-container">
      <h2>""" + title + """</h2>
      <p>""" + desc + """</p>
      <div className="interactive-area">
        <input 
          id="main-input" 
          value={value} 
          onChange={e => setValue(e.target.value)} 
          placeholder="Interact here..." 
        />
        <div id="output-display">{value || 'Ready'}</div>
      </div>
    </div>
  );
}
""",
            "App.tsx": """import React, { useState } from 'react';

export default function App(): JSX.Element {
  const [value, setValue] = useState<string>('');

  // TODO: Implement """ + title + """ component logic with TypeScript types

  return (
    <div className="component-container">
      <h2>""" + title + """</h2>
      <p>""" + desc + """</p>
      <div className="interactive-area">
        <input 
          id="main-input" 
          value={value} 
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value)} 
          placeholder="Interact here..." 
        />
        <div id="output-display">{value || 'Ready'}</div>
      </div>
    </div>
  );
}
""",
            "index.css": """.component-container {
  max-width: 440px;
  margin: 20px auto;
  padding: 24px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  color: #fafafa;
}
#main-input { width: 100%; padding: 10px; background: #09090b; border: 1px solid #3f3f46; border-radius: 6px; color: #fff; box-sizing: border-box; }
#output-display { margin-top: 16px; padding: 12px; background: #09090b; border: 1px solid #27272a; border-radius: 6px; font-family: monospace; color: #38bdf8; }
"""
        },
        "test_cases": [
            {
                "id": f"{slug}-tc-1",
                "name": "Standard Component Verification",
                "stdin": json.dumps({
                    "evaluation": """
                    const input = document.getElementById('main-input');
                    const output = document.getElementById('output-display');
                    if (!input || !output) return 'FAIL: Required elements missing';
                    input.value = 'Verified';
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    await new Promise(r => setTimeout(r, 60));
                    if (!output.textContent.includes('Verified')) return 'FAIL: Output display not updated';
                    return 'PASS';
                    """
                }),
                "expected_output": "PASS\n",
                "comparison_mode": "exact",
                "hidden": False,
                "weight": 1.0
            }
        ]
    })


def run_migration_and_seed():
    client = MongoClient(MONGO_URI)
    db = client["interleet"]

    print("--- 1. Deleting legacy domains: 'Backend' and 'System Design' ---")
    del_res = db.problems.delete_many({"domain": {"$in": ["Backend", "System Design"]}})
    print(f"Removed {del_res.deleted_count} legacy problems from MongoDB.")

    print("\n--- 2. Seeding React domain challenges (JSX + TSX Skeletons) ---")
    seeded_count = 0
    for idx, c in enumerate(REACT_CHALLENGES):
        prob_id = f"react-50-{idx+1}"
        doc = {
            "id": prob_id,
            "title": f"React: {c['title']}",
            "slug": c["slug"],
            "short_description": c["short_description"],
            "description": c["description"],
            "domain": "React",
            "difficulty": c["difficulty"],
            "tags": ["React", "Hooks", "Frontend", "Practice"],
            "technologies": ["javascript", "react", "html", "css", "typescript"],
            "concepts": ["React 18", "Component Architecture", "Hooks", "JSX", "TSX"],
            "runtime": "frontend",
            "execution_mode": "browser",
            "xp_reward": c["xp_reward"],
            "estimated_time_minutes": 30,
            "starter_code": c["starter_code"],
            "test_cases": c["test_cases"]
        }

        # Update or Insert
        db.problems.replace_one({"slug": c["slug"]}, doc, upsert=True)
        seeded_count += 1

    print(f"Successfully seeded/updated {seeded_count} React domain challenges in MongoDB.")

    # Print summary
    print("\n--- MongoDB Current Domain Counts ---")
    pipeline = [{"$group": {"_id": "$domain", "count": {"$sum": 1}}}]
    for row in db.problems.aggregate(pipeline):
        print(f"  {row['_id']}: {row['count']} problems")

if __name__ == "__main__":
    run_migration_and_seed()
