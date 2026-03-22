// State
let userIP = 'local';
let tasks = [];
let currentMood = 'normal';

// Elements
const moodBtns = document.querySelectorAll('.mood-btn');
const taskForm = document.getElementById('task-form');
const taskTitleInput = document.getElementById('task-title');
const taskTimeInput = document.getElementById('task-time');
const focusList = document.getElementById('focus-list');
const laterList = document.getElementById('later-list');
const focusCount = document.getElementById('focus-count');
const laterCount = document.getElementById('later-count');
const emptyState = document.getElementById('empty-state');
const collapsibleHeader = document.getElementById('later-header');
const collapsibleSection = document.querySelector('.collapsible-section');
const quoteEl = document.getElementById('motivational-quote');

// Stats Elements
const statsSection = document.getElementById('stats-section');
const chartContainer = document.getElementById('chart-container');

// Focus Mode Elements
const focusOverlay = document.getElementById('focus-overlay');
const focusTaskTitle = document.getElementById('focus-task-title');
const timerMinutes = document.getElementById('timer-minutes');
const timerSeconds = document.getElementById('timer-seconds');
const focusToggleBtn = document.getElementById('focus-toggle-btn');
const focusStopBtn = document.getElementById('focus-stop-btn');
const ambientBtn = document.getElementById('ambient-sound-btn');

const quotes = [
    "Small wins matter ✨",
    "You're doing great.",
    "One step at a time.",
    "Stay calm and focus."
];

// Audio Context for Ambient Noise
let audioCtx;
let noiseNode;
let filterNode;
let isAmbientPlaying = false;

// Timer Variables
let focusTimer;
let currentFocusSeconds = 0;
let isFocusPaused = false;
let currentFocusTaskId = null;

function formatTime(totalSeconds) {
    const m = Math.floor(totalSeconds / 60);
    const s = totalSeconds % 60;
    timerMinutes.textContent = m.toString().padStart(2, '0');
    timerSeconds.textContent = s.toString().padStart(2, '0');
}

function saveState() {
    localStorage.setItem(`focus_tasks_${userIP}`, JSON.stringify(tasks));
    localStorage.setItem(`focus_mood_${userIP}`, currentMood);
}

async function init() {
    // Fetch IP to scope the session
    try {
        const res = await fetch('https://api.ipify.org?format=json');
        const data = await res.json();
        userIP = data.ip.replaceAll('.', '_').replaceAll(':', '_'); 
    } catch(err) {
        console.warn('Could not fetch IP, using default local session');
        userIP = 'local';
    }
    
    // Initialize state with IP-scoped data
    tasks = JSON.parse(localStorage.getItem(`focus_tasks_${userIP}`)) || [];
    currentMood = localStorage.getItem(`focus_mood_${userIP}`) || 'normal';

    // Set initial mood
    moodBtns.forEach(btn => {
        if(btn.dataset.mood === currentMood) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
        btn.addEventListener('click', (e) => setMood(e.target.closest('.mood-btn').dataset.mood));
    });

    taskForm.addEventListener('submit', addTask);
    collapsibleHeader.addEventListener('click', () => {
        collapsibleSection.classList.toggle('open');
    });

    focusToggleBtn.addEventListener('click', toggleFocusTimer);
    focusStopBtn.addEventListener('click', stopFocusMode);
    ambientBtn.addEventListener('click', toggleAmbientSound);

    // Initial render without enforcing strict mood sort so manual sorting persists across loads
    renderTasks();
}

function setMood(mood) {
    currentMood = mood;
    moodBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.mood === mood));
    sortTasksByMood();
    saveState();
    renderTasks();
}

function sortTasksByMood() {
    const pending = tasks.filter(t => !t.completed);
    const completed = tasks.filter(t => t.completed);
    if(currentMood === 'low') {
        pending.sort((a, b) => a.time - b.time);
    } else if (currentMood === 'high') {
        pending.sort((a, b) => b.time - a.time);
    } // normal uses sequential order, won't resorte except to original structure if we saved it
    tasks = [...pending, ...completed];
}

function getMoodLimit() {
    if(currentMood === 'low') return 2;
    if(currentMood === 'high') return 5;
    return 3; // Normal
}

function addTask(e) {
    e.preventDefault();
    const title = taskTitleInput.value.trim();
    const time = parseInt(taskTimeInput.value);

    if(!title || isNaN(time) || time <= 0) return;

    const newTask = {
        id: Date.now().toString(),
        title,
        time,
        completed: false,
        createdAt: Date.now()
    };

    tasks.push(newTask);
    sortTasksByMood(); // auto-sort when a new task is added based on current mood rules
    saveState();
    
    taskTitleInput.value = '';
    taskTimeInput.value = '';

    renderTasks();
}

// Ensure function is exposed globally for inline onclick
window.toggleComplete = function(id) {
    const task = tasks.find(t => t.id === id);
    if(task) {
        task.completed = !task.completed;
        saveState();
        if(task.completed) {
            triggerConfetti();
            quoteEl.textContent = quotes[Math.floor(Math.random() * quotes.length)];
        }
        renderTasks();
    }
}

window.deleteTask = function(id) {
    // Add slide out animation before removing
    const el = document.querySelector(`.task-item[data-id="${id}"]`);
    if(el) {
        el.style.transform = 'translateY(20px)';
        el.style.opacity = '0';
        setTimeout(() => {
            tasks = tasks.filter(t => t.id !== id);
            saveState();
            renderTasks();
        }, 300);
    } else {
        tasks = tasks.filter(t => t.id !== id);
        saveState();
        renderTasks();
    }
}

function renderTasks() {
    focusList.innerHTML = '';
    laterList.innerHTML = '';

    const pendingTasks = tasks.filter(t => !t.completed);
    const completedTasks = tasks.filter(t => t.completed);

    const limit = getMoodLimit();
    const focusItems = pendingTasks.slice(0, limit);
    const laterItems = pendingTasks.slice(limit).concat(completedTasks);

    focusCount.textContent = focusItems.length;
    laterCount.textContent = laterItems.length;

    if(tasks.length === 0) {
        emptyState.classList.remove('hidden');
        collapsibleSection.classList.add('hidden');
    } else {
        emptyState.classList.add('hidden');
        collapsibleSection.classList.remove('hidden');
    }

    focusItems.forEach(task => {
        focusList.appendChild(createTaskElement(task));
    });

    laterItems.forEach(task => {
        laterList.appendChild(createTaskElement(task));
    });

    setupDragAndDrop();
    renderGraph();
}

function renderGraph() {
    const completedTasks = tasks.filter(t => t.completed);
    
    if (completedTasks.length === 0) {
        statsSection.classList.add('hidden');
        return;
    }
    
    statsSection.classList.remove('hidden');
    chartContainer.innerHTML = '';
    
    let maxMinutes = 1; 
    const chartData = completedTasks.map(t => {
        // Fallback to estimated time if user just checked it off without Focus timer, so chart isn't empty 0.
        const mins = (t.actualTimeSpent && t.actualTimeSpent > 0) ? Math.ceil(t.actualTimeSpent / 60) : t.time;
        if (mins > maxMinutes) maxMinutes = mins;
        return {
            title: t.title,
            mins: mins
        };
    });
    
    chartData.forEach(data => {
        const heightPercent = (data.mins / maxMinutes) * 100;
        
        const barWrapper = document.createElement('div');
        barWrapper.className = 'bar-wrapper';
        
        const bar = document.createElement('div');
        bar.className = 'bar';
        setTimeout(() => {
            bar.style.height = `${Math.max(heightPercent, 2)}%`; 
        }, 50);
        
        const value = document.createElement('span');
        value.className = 'bar-value';
        value.textContent = `${data.mins}m`;
        
        const label = document.createElement('span');
        label.className = 'bar-label';
        label.textContent = data.title;
        label.title = data.title;
        
        bar.appendChild(value);
        barWrapper.appendChild(bar);
        barWrapper.appendChild(label);
        
        chartContainer.appendChild(barWrapper);
    });
}

function createTaskElement(task) {
    const li = document.createElement('li');
    li.className = `task-item slide-in ${task.completed ? 'completed' : ''}`;
    li.dataset.id = task.id;
    li.draggable = true;

    li.innerHTML = `
        <div class="checkbox ${task.completed ? 'checked' : ''}" onclick="toggleComplete('${task.id}')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        </div>
        <div class="task-content">
            <span class="task-title">${task.title}</span>
            <span class="task-meta">${task.time} min</span>
        </div>
        ${!task.completed ? `<button class="focus-btn" onclick="startFocusMode('${task.id}')">Focus</button>` : ''}
        <button class="delete-btn" onclick="deleteTask('${task.id}')" title="Delete">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
        </button>
    `;
    return li;
}

// Focus Mode Logic
window.startFocusMode = function(id) {
    const task = tasks.find(t => t.id === id);
    if(!task) return;

    currentFocusTaskId = id;
    if (task.actualTimeSpent === undefined) task.actualTimeSpent = 0;

    focusTaskTitle.textContent = task.title;
    currentFocusSeconds = task.time * 60;
    formatTime(currentFocusSeconds);
    isFocusPaused = false;
    focusToggleBtn.textContent = 'Pause';

    focusOverlay.classList.remove('hidden');
    setTimeout(() => {
        focusOverlay.classList.add('active');
    }, 10);

    clearInterval(focusTimer);
    focusTimer = setInterval(timerTick, 1000);
}

function timerTick() {
    if(!isFocusPaused && currentFocusSeconds > 0) {
        currentFocusSeconds--;
        formatTime(currentFocusSeconds);
        
        const task = tasks.find(t => t.id === currentFocusTaskId);
        if(task) {
            task.actualTimeSpent = (task.actualTimeSpent || 0) + 1;
        }

        if(currentFocusSeconds === 0) {
            clearInterval(focusTimer);
            saveState();
            triggerConfetti();
        }
    }
}

function toggleFocusTimer() {
    isFocusPaused = !isFocusPaused;
    focusToggleBtn.textContent = isFocusPaused ? 'Resume' : 'Pause';
}

function stopFocusMode() {
    clearInterval(focusTimer);
    saveState();
    focusOverlay.classList.remove('active');
    setTimeout(() => {
        focusOverlay.classList.add('hidden');
    }, 500); 
    if(isAmbientPlaying) toggleAmbientSound();
}

// Confetti Effect
function triggerConfetti() {
    const container = document.getElementById('confetti-container');
    const colors = ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ec4899'];
    for(let i=0; i<50; i++) {
        const conf = document.createElement('div');
        conf.className = 'confetti';
        conf.style.left = Math.random() * 100 + 'vw';
        conf.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        conf.style.animationDuration = (Math.random() * 2 + 1) + 's';
        conf.style.animationDelay = Math.random() * 0.5 + 's';
        container.appendChild(conf);
        setTimeout(() => conf.remove(), 3000);
    }
}

// Drag and Drop implementation
let draggedItem = null;

function setupDragAndDrop() {
    const items = document.querySelectorAll('.task-item');
    
    items.forEach(item => {
        item.addEventListener('dragstart', function(e) {
            draggedItem = this;
            setTimeout(() => this.classList.add('dragging'), 0);
        });

        item.addEventListener('dragend', function() {
            setTimeout(() => {
                this.classList.remove('dragging');
                if(draggedItem) {
                    updateSyncOrder();
                }
                draggedItem = null;
            }, 0);
        });

        item.addEventListener('dragover', function(e) {
            e.preventDefault();
            if(this !== draggedItem) {
                const bounding = this.getBoundingClientRect();
                const offset = bounding.y + (bounding.height / 2);
                if (e.clientY - offset > 0) {
                    this.style.borderBottom = '2px solid var(--primary)';
                    this.style.borderTop = '';
                } else {
                    this.style.borderTop = '2px solid var(--primary)';
                    this.style.borderBottom = '';
                }
            }
        });

        item.addEventListener('dragleave', function() {
            this.style.borderBottom = '';
            this.style.borderTop = '';
        });

        item.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderBottom = '';
            this.style.borderTop = '';
            if (this !== draggedItem && draggedItem) {
                const list = this.parentElement;
                const bounding = this.getBoundingClientRect();
                const offset = bounding.y + (bounding.height / 2);
                if (e.clientY - offset > 0) {
                    list.insertBefore(draggedItem, this.nextSibling);
                } else {
                    list.insertBefore(draggedItem, this);
                }
            }
        });
    });
}

function updateSyncOrder() {
    const focusDomItems = Array.from(focusList.querySelectorAll('.task-item'));
    const laterDomItems = Array.from(laterList.querySelectorAll('.task-item'));
    
    const newPending = [];
    const pushTask = (domItem) => {
        const id = domItem.dataset.id;
        const task = tasks.find(t => t.id === id);
        if(task && !task.completed) newPending.push(task);
    };

    focusDomItems.forEach(pushTask);
    laterDomItems.forEach(pushTask);
    
    const completedTasks = tasks.filter(t => t.completed);
    tasks = [...newPending, ...completedTasks];
    saveState();
    
    // We re-render to enforce limits (e.g., if drag-dropped from later to focus)
    // and wait a tick to prevent jitter since dragend just completed
    setTimeout(() => {
        renderTasks();
    }, 10);
}

// Ambient Sound Generator (Brown Noise)
function createBrownNoise() {
    const bufferSize = 2 * audioCtx.sampleRate;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    let lastOut = 0;
    for (let i = 0; i < bufferSize; i++) {
        let white = Math.random() * 2 - 1;
        output[i] = (lastOut + (0.02 * white)) / 1.02;
        lastOut = output[i];
        output[i] *= 3.5; // (roughly) compensate for gain
    }
    const noise = audioCtx.createBufferSource();
    noise.buffer = noiseBuffer;
    noise.loop = true;
    
    // Filter
    const filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 400;

    noise.connect(filter);
    filter.connect(audioCtx.destination);
    
    return noise;
}

function toggleAmbientSound() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    
    if(audioCtx.state === 'suspended') {
        audioCtx.resume();
    }

    if (isAmbientPlaying) {
        if(noiseNode) {
            noiseNode.stop();
            noiseNode.disconnect();
        }
        isAmbientPlaying = false;
        ambientBtn.classList.remove('active');
        ambientBtn.style.color = "var(--text-muted)";
    } else {
        noiseNode = createBrownNoise();
        noiseNode.start();
        isAmbientPlaying = true;
        ambientBtn.classList.add('active');
        ambientBtn.style.color = "var(--primary)";
    }
}

document.addEventListener('DOMContentLoaded', init);
