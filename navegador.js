// Cria um contexto de áudio
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

// Função para tocar um som
function playSound(frequency, duration) {
    // Cria um oscilador
    const oscillator = audioContext.createOscillator();
    oscillator.type = 'sine'; // Tipo de onda: sine, square, sawtooth, triangle
    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime); // Define a frequência

    // Cria um ganho (controlador de volume)
    const gainNode = audioContext.createGain();
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime); // Define o volume

    // Conecta o oscilador ao ganho e o ganho ao destino (alto-falantes)
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    // Inicia o oscilador
    oscillator.start();
    
    // Para o oscilador após a duração especificada
    oscillator.stop(audioContext.currentTime + duration);

    // Retorna o oscilador para poder pará-lo externamente
    return oscillator;
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

let arquivoBaixado = false;

function timer() {
    const gol_eye = document.getElementsByClassName('ovm-GoalEventAlert_Text');
    if (gol_eye.length > 0 && !arquivoBaixado) {
        clearInterval(bombs); // Pare de verificar enquanto processa o download
        let times_gol = gol_eye[0].parentElement.parentElement;  // Get the match div
        let times_go2 = gol_eye[0].parentElement.parentElement.parentElement;

        const nome = times_gol.innerText;  // Pega o nome do time que fez gol
        const nome2 = times_go2.innerText;        
        if (times_gol) {
            console.log('Gol encontrado.');
            console.log(nome);
            const posicao = times_gol.getBoundingClientRect().toJSON();
            const jsonString = JSON.stringify({
                'nome': nome,
                'nome2': nome2
            });

            const blob = new Blob([jsonString], { type: 'application/json' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            console.log('Enviando informação');
            a.download = 'position.json';
            a.click();
            
            // Toca o som quando um gol é detectado e o arquivo é baixado, se o som estiver habilitado
            if (soundEnabled) {
                playSound(440, 0.5);
                playSound(293.6, 0.5)
            }

            arquivoBaixado = true; // Marque o arquivo como baixado
            setTimeout(() => {
                arquivoBaixado = false; // Redefina a variável para permitir futuros downloads
                bombs = window.setInterval(timer, 1000); // Reinicie a verificação após o atraso
            }, 5000); // Atraso de 5 segundos (ajuste conforme necessário)
        }
        else {
            console.log('Gol não encontrado');
            bombs = window.setInterval(timer, 1000); // Reinicie a verificação se o gol não for encontrado
        }
    }
    else {
        console.log('Aguardando gol...');
    }
}

let bombs = window.setInterval(timer, 1000); // Inicie a verificação a cada 1 segundo

// Informações para o usuário no console
console.log("Monitor de gols iniciado. Use ligar() para habilitar o som e desligar() para desabilitar o som.");