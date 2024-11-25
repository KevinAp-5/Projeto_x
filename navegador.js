
// Cria um único contexto de áudio
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

// Função para tocar um som
function playSound(frequency, duration) {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);

    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.start();
    oscillator.stop(audioContext.currentTime + duration);
}

// Variável global para controlar o som
let soundEnabled = true;

function ligar() {
    soundEnabled = true;
    console.log("Som habilitado.");
}

function desligar() {
    soundEnabled = false;
    console.log("Som desabilitado.");
}

// Função para verificar gols
let arquivoBaixado = false;

function verificarGol() {
    try {
        const gol_eye = document.getElementsByClassName('ovm-GoalEventAlert_Text');
        if (gol_eye.length > 0 && !arquivoBaixado) {
            const times_gol = gol_eye[0].parentElement.parentElement;
            const times_go2 = gol_eye[0].parentElement.parentElement.parentElement;

            const nome = times_gol ? times_gol.innerText : 'Desconhecido';
            const nome2 = times_go2 ? times_go2.innerText : 'Desconhecido';

            console.log('Gol detectado:', { nome, nome2 });

            const jsonString = JSON.stringify({ nome, nome2 });
            const blob = new Blob([jsonString], { type: 'application/json' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'position.json';
            a.click();

            if (soundEnabled) {
                playSound(440, 0.5);
                setTimeout(() => playSound(293.6, 0.5), 300);
            }

            arquivoBaixado = true;
            setTimeout(() => {
                arquivoBaixado = false;
                console.log('Pronto para verificar novos eventos.');
            }, 10000); // Aguarde 10 segundos antes de permitir novo download
        } else {
            console.log('Nenhum gol detectado.');
        }
    } catch (err) {
        console.error('Erro ao verificar gol:', err);
    } finally {
        // Reinicia o timer com atraso aleatório para evitar padrões detectáveis
        const delay = Math.floor(Math.random() * 2000) + 1000; // Entre 1 e 3 segundos
        setTimeout(verificarGol, delay);
    }
}

// Inicia o monitoramento
(function iniciarMonitoramento() {
    console.log("Monitor de gols iniciado.");
    verificarGol();
})();
