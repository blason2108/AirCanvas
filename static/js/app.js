const socket = io();

let currentTool = 'pen';
let currentColor = '#FF6B6B';

document.querySelectorAll('.tool-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentTool = btn.dataset.tool;
        socket.emit('set_tool', { tool: currentTool });
        document.getElementById('toolStatus').textContent = `Tool: ${currentTool.charAt(0).toUpperCase() + currentTool.slice(1)}`;
        playClickSound();
    });
});

document.querySelectorAll('.color-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        currentColor = btn.dataset.color;
        socket.emit('set_color', { color: currentColor });
        document.getElementById('customColor').value = currentColor;
    });
});

document.getElementById('customColor').addEventListener('input', (e) => {
    currentColor = e.target.value;
    socket.emit('set_color', { color: currentColor });
});

document.getElementById('brushSize').addEventListener('input', (e) => {
    const size = parseInt(e.target.value);
    document.getElementById('sizeValue').textContent = size;
    socket.emit('set_size', { size: size });
});

document.getElementById('undoBtn').addEventListener('click', () => {
    socket.emit('undo');
    playClickSound();
});

document.getElementById('redoBtn').addEventListener('click', () => {
    socket.emit('redo');
    playClickSound();
});

document.getElementById('clearBtn').addEventListener('click', () => {
    if (confirm('Clear the canvas?')) {
        socket.emit('clear');
        playClickSound();
    }
});

document.getElementById('exportBtn').addEventListener('click', () => {
    playClickSound();
    setTimeout(() => {
        window.location.href = '/export';
    }, 150);
});

socket.on('action_response', (data) => {
    console.log(`${data.action}: ${data.success ? 'success' : 'failed'}`);
    if (data.success) {
        flashButton(data.action);
    }
});

function playClickSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.1);
}

function flashButton(action) {
    const btnMap = {
        'undo': 'undoBtn',
        'redo': 'redoBtn', 
        'clear': 'clearBtn'
    };
    const btn = document.getElementById(btnMap[action]);
    if (btn) {
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btn.style.transform = '';
        }, 100);
    }
}

document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
        e.preventDefault();
        if (e.shiftKey) {
            socket.emit('redo');
        } else {
            socket.emit('undo');
        }
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'y') {
        e.preventDefault();
        socket.emit('redo');
    }
});