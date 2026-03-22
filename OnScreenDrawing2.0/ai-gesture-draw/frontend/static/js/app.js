document.addEventListener('DOMContentLoaded', () => {
    const videoFeed = document.getElementById('videoFeed');
    const modeBadge = document.getElementById('modeBadge');
    const modeText = document.getElementById('modeText');
    const colorIndicator = document.getElementById('colorIndicator');
    const colorName = document.getElementById('colorName');
    const sizeBar = document.getElementById('sizeBar');
    const sizeValue = document.getElementById('sizeValue');
    const toggleGuide = document.getElementById('toggleGuide');
    const guidePanel = document.getElementById('guidePanel');
    const fpsValue = document.getElementById('fpsValue');

    let isGuideCollapsed = false;

    // Toggle Side Panel
    toggleGuide.addEventListener('click', () => {
        isGuideCollapsed = !isGuideCollapsed;
        guidePanel.classList.toggle('collapsed', isGuideCollapsed);
        toggleGuide.textContent = isGuideCollapsed ? '?' : '»';
    });

    // Polling State
    async function updateState() {
        try {
            const response = await fetch('/state');
            const data = await response.json();

            if (data.error) return;

            // Update Mode
            modeText.textContent = data.mode;

            // Clean classes
            modeBadge.className = 'glass-badge'; // Reset
            if (data.mode === 'DRAW') {
                modeBadge.classList.add('mode-draw');
                modeBadge.querySelector('.icon').textContent = '✏️';
            } else if (data.mode === 'CLEAR') {
                modeBadge.classList.add('mode-clear');
                modeBadge.querySelector('.icon').textContent = '🧹';
            } else if (data.mode === 'PAUSED') {
                modeBadge.classList.add('mode-paused');
                modeBadge.querySelector('.icon').textContent = '⏸️';
            } else if (data.mode === 'COLOR') {
                modeBadge.querySelector('.icon').textContent = '🎨';
            } else if (data.mode === 'SIZE') {
                modeBadge.querySelector('.icon').textContent = '📏';
            } else if (data.mode === 'MOVE') {
                modeBadge.querySelector('.icon').textContent = '✊';
            } else {
                modeBadge.classList.add('mode-neutral');
                modeBadge.querySelector('.icon').textContent = '✋';
            }

            // Update Color
            // Color data is Name, need mapping for visuals if backend sends Name? 
            // Backend sends Name "Red", "Blue" etc.
            // HTML colors are standard.
            colorIndicator.style.backgroundColor = data.color.toLowerCase();
            colorName.textContent = data.color;

            // Update Size
            // Max size 50
            const pct = (data.size / 50) * 100;
            sizeBar.style.width = `${pct}%`;
            sizeValue.textContent = `${data.size}px`;

            // FPS
            fpsValue.textContent = data.fps;

        } catch (e) {
            console.error("Error polling state:", e);
        }
    }

    // Poll every 100ms
    setInterval(updateState, 100);
});
