const $ = (selector) => document.querySelector(selector);
const reels = [...document.querySelectorAll('.reel')];
const symbols = ['🍒','🍋','🔔','⭐','7'];
const spin = $('#spin');
const recharge = $('#recharge');
const amount = $('#amount');
const info = $('#message');
const balance = $('#balance');
const history = $('#history');
let busy = false;
let currentBalance = 100;
let bet = 10;
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
function message(value, error=false){ info.textContent=value; info.classList.toggle('notice',error); }
function updateBalance(value){currentBalance=value;balance.textContent=value.toLocaleString('es-AR');spin.disabled=busy || currentBalance<bet;}
async function api(path, payload){
  const res = await fetch(path,{method:payload?'POST':'GET',headers:{'Content-Type':'application/json'},body:payload?JSON.stringify(payload):undefined});
  let data;try{data=await res.json();}catch{throw Error('No se pudo leer la respuesta del servidor.');}
  if(!res.ok)throw Error(data.error || 'No se pudo completar la operación.');return data;
}
function showHistory(items){
  history.replaceChildren();
  if(!items.length){const e=document.createElement('div');e.className='empty';e.textContent='Todavía no hay jugadas en esta sesión.';history.append(e);return;}
  items.forEach((item,i)=>{
    const row=document.createElement('div');row.className='history-item';
    const left=document.createElement('div');const icons=document.createElement('b');icons.textContent=item.rodillos.join(' ');
    const details=document.createElement('small');details.textContent='Tirada '+(items.length-i)+' · saldo '+item.saldo;
    left.append(icons,details);const prize=document.createElement('strong');prize.textContent=item.premio?'+'+item.premio:'Sin premio';row.append(left,prize);history.append(row);
  });
}
async function load(){try{const data=await api('/api/estado');bet=data.apuesta;$('#bet').textContent=bet;updateBalance(data.saldo);showHistory(data.historial);}catch(err){message(err.message,true);spin.disabled=true;}}
spin.addEventListener('click',async()=>{
  if(busy || currentBalance<bet)return;
  busy=true;spin.disabled=true;recharge.disabled=true;amount.disabled=true;message('Girando rodillos...');
  const interval=setInterval(()=>reels.forEach(r=>r.textContent=symbols[Math.floor(Math.random()*symbols.length)]),75);
  reels.forEach(r=>r.classList.add('spinning'));
  try{
    const started=Date.now();const data=await api('/api/girar',{});
    await pause(Math.max(0,900-(Date.now()-started)));
    clearInterval(interval);
    for(let i=0;i<3;i++){reels[i].classList.remove('spinning');reels[i].textContent=data.rodillos[i];await pause(180);}
    updateBalance(data.saldo);showHistory(data.historial);
    message(data.premio>bet?'¡PREMIO MAYOR! Ganaste '+data.premio+' fichas.':data.premio===bet?'Dos iguales: recuperaste tu apuesta.':'Sin premio esta vez. ¡Probá de nuevo!');
  }catch(err){clearInterval(interval);reels.forEach(r=>r.classList.remove('spinning'));message(err.message,true);await load();}
  finally{busy=false;spin.disabled=currentBalance<bet;recharge.disabled=false;amount.disabled=false;}
});
$('#recharge-form').addEventListener('submit',async(e)=>{
  e.preventDefault();if(busy)return;
  const quantity=Number(amount.value);
  if(!Number.isInteger(quantity)||quantity<=0||quantity>100000){message('Ingresá un entero entre 1 y 100000.',true);return;}
  recharge.disabled=true;
  try{const data=await api('/api/cargar',{cantidad:quantity});updateBalance(data.saldo);message('Cargaste '+quantity+' fichas.');}catch(err){message(err.message,true);}
  finally{recharge.disabled=false;}
});
load();