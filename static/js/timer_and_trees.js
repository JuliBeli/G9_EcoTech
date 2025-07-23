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

    const durationToStage = {
        20: 0,  // 20 minutes -> stage 1
        40: 1,  // 40 minutes -> stage 2
        60: 2,  // 1 hour -> stage 3
        90: 3,  // 90 minutes -> stage 4
        120: 4  // 2 hours -> stage 5
    };

    // Update tree image based on selected time
    timerSelect.addEventListener('change', () => {
        const duration = parseInt(timerSelect.value);
        const stageIndex = durationToStage[duration];
        treeImage.src = treeStages[stageIndex];
    });

    startButton.addEventListener('click', () => {
        const duration = parseInt(timerSelect.value);
        let remainingTime = duration * 60; // Convert minutes to seconds

        // Reset tree image to stage 1
        treeImage.src = treeStages[0];

        const interval = setInterval(() => {
            if (remainingTime <= 0) {
                clearInterval(interval);
                countdownDisplay.textContent = "Time's up!";
                return;
            }

            const minutes = Math.floor(remainingTime / 60);
            const seconds = remainingTime % 60;

            countdownDisplay.textContent = `Time remaining: ${minutes} minutes ${seconds} seconds`;

            // Gradually update tree image based on remaining time
            const elapsedTime = duration * 60 - remainingTime; // Time elapsed in seconds
            const stageIndex = Math.floor((elapsedTime / (duration * 60)) * (treeStages.length - 1));
            treeImage.src = treeStages[stageIndex];

            remainingTime--;
        }, 1000);
    });
});