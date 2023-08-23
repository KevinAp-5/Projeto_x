const interval = setInterval(function() {
    const gol_eye = document.getElementsByClassName('ovm-GoalEventAlert_Text');

    if (gol_eye.length > 0) {
        clearInterval(interval);

        let times_gol = gol_eye[0];  // Get the match div
        for (let i = 0; i < 3; i++) {
            times_gol = times_gol.parentElement;
        }

        if (times_gol) {
            console.log('Gol encontrado.')
            const posicao = times_gol.getBoundingClientRect().toJSON();
            const jsonString = JSON.stringify({
                'x': posicao.x,
                'y': posicao.y,
                'width': window.innerWidth,
                'height': window.innerHeight
            })
        }
    }

}, 1000);