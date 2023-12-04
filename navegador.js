let arquivoBaixado = false;

function timer() {
    const gol_eye = document.getElementsByClassName('ovm-GoalEventAlert_Text');
    if (gol_eye.length > 0 && !arquivoBaixado) {
        clearInterval(bombs); // Pare de verificar enquanto processa o download
        let times_gol = gol_eye[0].parentElement.parentElement;  // Get the match div

        const nome = times_gol.textContent;  // Pega o nome do time que fez gol
        if (times_gol) {
            console.log('Gol encontrado.');
            console.log(nome)
            const posicao = times_gol.getBoundingClientRect().toJSON();
            const jsonString = JSON.stringify({
                'nome': nome
            });

            const blob = new Blob([jsonString], { type: 'application/json' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            console.log('Enviando informação para o Python');
            a.download = 'position.json';
            a.click();
            
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
