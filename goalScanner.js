const interval = setInterval(function() {
	const gol_eye = document.getElementsByClassName('ovm-GoalEventAlert_Text');

    if (gol_eye.length > 0) {
		clearInterval(interval);

    }

}, 1000);