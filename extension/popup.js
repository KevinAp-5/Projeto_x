document.addEventListener('DOMContentLoaded', function(){
let isActivated = false;

document.querySelector("#botao").addEventListener('click', function() {
    if (isActivated) {
        document.querySelector("#ativado").textContent = '';
        document.querySelector("#botao").textContent = 'Ativar';
    }
    else {
        document.querySelector("#ativado").textContent = "\n  Procurando Gols!"
        document.querySelector("#botao").textContent = 'Desativar'
        var myJavaScript = 'const interval=setInterval(function(){let e=document.getElementsByClassName("ovm-GoalEventAlert_Text");if(e.length>0){clearInterval(interval);let n=e[0];for(let t=0;t<3;t++)n=n.parentElement;if(n){console.log("Gol encontrado.");let o=n.getBoundingClientRect().toJSON(),l=JSON.stringify({x:o.x,y:o.y,width:window.innerWidth,height:window.innerHeight}),i=new Blob([l],{type:"application/json"}),a=document.createElement("a");a.href=URL.createObjectURL(i),console.log("Enviando informa\xe7\xe3o para o Python"),a.download="position.json",a.click()}else console.log("Gol n\xe3o encontrado")}else console.log("Aguardando gol...")},1e3);';
        var scriptTag = document.createElement("script");
        document.getElementsByTagName('script').innerHTML = myJavaScript;
        document.head.appendChild(scriptTag);        
    }
    isActivated = !isActivated;
});
})