function change() {
    // Get colour to change to
    const colour = document.getElementById("backgroundColour").value;
    // Get the link element that links to the stylesheet
    const link = document.querySelector('link[href="/static/styles.css"]');
    // Get the stylesheet object
    const sheet = link.sheet;
    // Add a new rule to the stylesheet
    sheet.insertRule(`body { background-color: ${colour}; }`, 0);
}

document.addEventListener("DOMContentLoaded", () => {
    // dynamic slider (does not work at all)
    function dynamicVolume() {
        const text = document.getElementsByTagName("small");
        var slider = document.getElementById("volume");
        text.innerHTML = slider.value;
    }
    // audio object for all audio elements
    var audio = new Audio();
    const volume = JSON.parse(document.querySelector("#volume").dataset.volume);
    audio.volume = volume / 100;
    const startTime = JSON.parse(document.querySelector("#startTime").dataset.time);
    const breakTime = JSON.parse(document.querySelector("#breakTime").dataset.time);
    let time = startTime * 60;
    // let time = 10;
    const countdownElements = document.getElementsByClassName("countdownElement");
    // tells you whether we are currently doing a pomdoro or a break
    let pomodoro = true;
    // auto break on or off
    let autoBreak = JSON.parse(document.querySelector("#autoBreak").dataset.status);
    // auto pomodoro on or off
    let autoPomodoro = JSON.parse(document.getElementById('autoPomodoro').dataset.status);
    function updateCountdown() {
        const minutes = Math.floor(time / 60);
        let seconds = time % 60;
        if (seconds < 10) {
            seconds = '0' + seconds;
        }
        for (var i = 0; i < countdownElements.length; i++) {
            countdownElements[i].innerHTML = `${minutes}:${seconds}`;
        }
        time --;
        // if the timer is done
        if (time == -1) {
            if (pomodoro) {
                if (!autoBreak) {
                    // clears a timer set with the setInterval() method
                    clearInterval(timer);
                    running = false;
                    button.innerHTML = 'Start!';
                    button.classList.remove('btn-danger');
                    button.classList.add('btn-primary');
                }
                document.getElementsByTagName('h1')[0].innerHTML = 'Break Time 😁';
                for (var i = 0; i < countdownElements.length; i++) {
                    countdownElements.innerHTML = `${breakTime}:00`;
                }
                time = breakTime * 60;
                // time = 10;
                pomodoro = false;
            }
            else {
                if (!autoPomodoro) {
                    // clears a timer set with the setInterval() method
                    clearInterval(timer);
                    running = false;
                    button.innerHTML = 'Start!';
                    button.classList.remove('btn-danger');
                    button.classList.add('btn-primary');
                }
                document.getElementsByTagName('h1')[0].innerHTML = 'Pymodoro';
                for (var i = 0; i < countdownElements.length; i++) {
                    countdownElements.innerHTML = `${startTime}:00`;
                }
                time = startTime * 60;
                pomodoro = true;
            }
            audio.src = '/static/audio/'+JSON.parse(document.querySelector("#alarm").dataset.alarm)+'.wav';
            audio.play();
        }
    }
    let button = document.getElementById("startstop");
    let running = false;
    var timer = null;
    button.addEventListener("click", () => {
        audio.src = '/static/audio/switch.wav';
        audio.play();
        if (!running) {
            // start timer
            // set interval calls updateCountdown every 1000 ms
            timer = setInterval(updateCountdown, 1000);
            running = true;
            button.innerHTML = 'Stop!';
            button.classList.remove('btn-primary')
            button.classList.add('btn-danger')
        }
        else if (running) {
            // stop timer
            // clears a timer set with the setInterval() method
            clearInterval(timer);
            running = false;
            button.innerHTML = 'Start!';
            button.classList.remove('btn-danger');
            button.classList.add('btn-primary');
        }
    });
});