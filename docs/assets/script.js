const $=s=>document.querySelector(s);
const reels=[...document.querySelectorAll('.reel')];
const symbols=['🍒','🍋','🔔','⭐','7'];
const spin=$('#spin'),recharge=$('#recharge'),amount=$('#amount'),info=$('#message');
const balance=$('#balance'),history=$('#history'),bet=10;
const storageKey='tragamonedas-tfi-pages-v1';
let busy=false;
function fresh(){return {saldo:100,historial:[],inicio:new Date().toISOString()};}
function read(){try{let v=JSON.parse(localStorage.getItem(storageKey));return v&&Number.isSafeInteger(v.saldo)&&v.saldo>=0&&Array.isArray(v.historial)?v:fresh();}catch{return fresh();}}
let state=read();
function message(value,error=false){info.textContent=value;info.classList.toggle('notice',error);}
function save(){try{localStorage.setItem(storageKey,JSON.stringify(state));}catch{message('No se pudo guardar el progreso en este navegador.',true);}}
function updateBalance(){balance.textContent=state.saldo.toLocaleString('es-AR');spin.disabled=busy||state.saldo<bet;}
function showHistory(){history.replaceChildren();const items=state.historial.slice(-15).reverse();if(!items.length){let d=document.createElement('div');d.className='empty';d.textContent='Todavía no hay jugadas.';history.append(d);return;}
items.forEach((item,i)=>{const row=document.createElement('div');row.className='history-item';const left=document.createElement('div');const icons=document.createElement('b');icons.textContent=item.rodillos.join(' ');const details=document.createElement('small');details.textContent='Tirada '+(state.historial.length-i)+' · saldo '+item.saldo;left.append(icons,details);const prize=document.createElement('strong');prize.textContent=item.premio?'+'+item.premio:'Sin premio';row.append(left,prize);history.append(row);});}
function choice(){return symbols[Math.floor(Math.random()*symbols.length)];}
function premio(r){if(r[0]===r[1]&&r[1]===r[2])return bet*10;if(r[0]===r[1]||r[1]===r[2]||r[0]===r[2])return bet;return 0;}
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
spin.addEventListener('click',async()=>{if(busy||state.saldo<bet)return;busy=true;spin.disabled=true;recharge.disabled=true;amount.disabled=true;message('Girando rodillos...');
const r=[choice(),choice(),choice()],p=premio(r);state.saldo=state.saldo-bet+p;state.historial.push({rodillos:r,premio:p,saldo:state.saldo,fecha:new Date().toISOString()});save();
const interval=setInterval(()=>reels.forEach(el=>el.textContent=choice()),75);reels.forEach(el=>el.classList.add('spinning'));
try{await pause(900);clearInterval(interval);for(let i=0;i<3;i++){reels[i].classList.remove('spinning');reels[i].textContent=r[i];await pause(180);}updateBalance();showHistory();message(p>bet?'¡PREMIO MAYOR! Ganaste '+p+' fichas.':p===bet?'Dos iguales: recuperaste tu apuesta.':'Sin premio esta vez. ¡Probá de nuevo!');}finally{clearInterval(interval);busy=false;recharge.disabled=false;amount.disabled=false;updateBalance();}});
$('#recharge-form').addEventListener('submit',e=>{e.preventDefault();if(busy)return;const q=Number(amount.value);if(!Number.isSafeInteger(q)||q<1||q>100000){message('Ingresá un entero entre 1 y 100000.',true);return;}state.saldo+=q;save();updateBalance();message('Cargaste '+q+' fichas.');});
$('#download-history').addEventListener('click',()=>{const stamp=state.inicio.replace(/[:T]/g,'-').slice(0,16);const lines=state.historial.map(x=>x.rodillos.join(' | ')+' | Premio: '+x.premio+' | Saldo: '+x.saldo);const blob=new Blob([lines.join('\n')+'\n'],{type:'text/plain;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='historial_partida_'+stamp+'.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
$('#bet').textContent=bet;updateBalance();showHistory();