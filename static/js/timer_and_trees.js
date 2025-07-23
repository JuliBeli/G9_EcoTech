document.addEventListener('DOMContentLoaded', () => {
    const timerSelect = document.getElementById('timer');
    const startButton = document.getElementById('start-timer');
    const countdownDisplay = document.getElementById('countdown');
    const treeImage = document.getElementById('tree-image');

    const treeStages = [
        '/static/images/tree-stage-1.png',
        '/static/images/tree-stage-2.png',
        '/static/images/tree-stage-3.png',
        '/static/images/tree-stage-4.png',
        '/static/images/tree-stage-5.png'
    ];

    startButton.addEventListener('click', () => {
        const duration = parseInt(timerSelect.value);
        let remainingTime = duration;

        const interval = setInterval(() => {
            if (remainingTime <= 0) {
                clearInterval(interval);
                countdownDisplay.textContent = "Time's up!";
                return;
            }

            const minutes = Math.floor(remainingTime / 60);
            const seconds = remainingTime % 60;

            countdownDisplay.textContent = `Time remaining: ${minutes} minutes ${seconds} seconds`;

            const stageIndex = Math.floor((treeStages.length - 1) * (1 - remainingTime / duration));
            treeImage.src = treeStages[stageIndex];

            remainingTime--;
        }, 1000);
    });
});