/* Mock exam: 120-minute clock, self-grade each question (0-2.5), total /20, saved in localStorage. */
(function(){
  var KEY='mock-selfgrade',T0=7200,left=T0,timer=null;
  var tm=document.getElementById('mk_timer'),tot=document.getElementById('mk_total');if(!tm)return;
  var inputs=[].slice.call(document.querySelectorAll('input.sg'));
  var saved={};try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
  inputs.forEach(function(i){if(saved[i.dataset.q]!==undefined)i.value=saved[i.dataset.q];i.addEventListener('input',sum)});
  function f(s){return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2)}
  function sum(){var t=0,o={};inputs.forEach(function(i){var v=parseFloat(i.value);if(!isNaN(v)){v=Math.max(0,Math.min(v,parseFloat(i.max)));t+=v;o[i.dataset.q]=v}});
    tot.textContent='Total: '+(Math.round(t*100)/100)+'/20';try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
  document.getElementById('mk_start').onclick=function(){clearInterval(timer);timer=setInterval(function(){left--;tm.textContent='Time: '+f(Math.max(left,0));if(left<=0){clearInterval(timer);tm.textContent='Time is up — stop writing and self-grade.'}},1000)};
  document.getElementById('mk_stop').onclick=function(){clearInterval(timer)};
  document.getElementById('mk_reset').onclick=function(){clearInterval(timer);left=T0;tm.textContent='Time: '+f(left);inputs.forEach(function(i){i.value=''});sum()};
  sum();
})();
