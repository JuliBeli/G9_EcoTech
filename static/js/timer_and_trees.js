document.addEventListener('DOMContentLoaded', () => {
    const timerSelect = document.getElementById('timer');
    const startButton = document.getElementById('start-timer');
    const countdownDisplay = document.getElementById('countdown');
    const treeImage = document.getElementById('tree-image');

    if (!timerSelect || !startButton || !countdownDisplay || !treeImage) {
        console.error('One or more required elements are missing in the DOM.');
        return;
    }

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

    timerSelect.addEventListener('change', () => {
        // retrieve selected value and convert it to integer
        const duration = parseInt(timerSelect.value);
        // map the selected duration to a corresponding stage of tree
        const stageIndex = durationToStage[duration];
        // update the image to the corresponding stage
        treeImage.src = treeStages[stageIndex];
    });

    // when the start timer button is clicked, trigger the callback function
    startButton.addEventListener('click', () => {
        // retrieve selected duration and convert it to integer
        const duration = parseInt(timerSelect.value);
        let remainingTime = duration * 60; // Convert minutes to seconds

        // Reset tree image to stage 1
        treeImage.src = treeStages[0];

        // create a timer
        const interval = setInterval(() => {
            // check if the remaining time has reached zero
            if (remainingTime <= 0) {
                // if it has, clear this interval
                clearInterval(interval);
                // dispaly a message
                countdownDisplay.textContent = "Time's up!";
                return;
            }
            //convert the remaining time to minutes and seconds for display
            const minutes = Math.floor(remainingTime / 60);
            const seconds = remainingTime % 60;

            countdownDisplay.textContent = `Time remaining: ${minutes} minutes ${seconds} seconds`;

            // Gradually update tree image based on remaining time
            const elapsedTime = duration * 60 - remainingTime; // Time elapsed in seconds
            // elapsed time:the number of seconds that have passed
            // duration*60: converts the total duration from minutes to seconds
            // division: the fraction of time elapsed
            // multiply: scale it to the corresponding tree stage
            // floor: round the value down to the nearest integer
            const stageIndex = Math.floor((elapsedTime / (duration * 60)) * (treeStages.length - 1));
            treeImage.src = treeStages[stageIndex];
            // decremented by one second at the end of each interval
            remainingTime--;
        }, 1000);
    });
});