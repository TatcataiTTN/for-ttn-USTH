/* Written mock papers: every .paper has its own clock, self-grade inputs and total, saved in localStorage (key = data-key). */
(function(){
  [].forEach.call(document.querySelectorAll('section.paper'),function(sec){
    var KEY=sec.getAttribute('data-key')||'mock',T0=parseInt(sec.getAttribute('data-seconds')||'7200',10),left=T0,timer=null;
    var tm=sec.querySelector('.mk_timer'),tot=sec.querySelector('.mk_total');if(!tm||!tot)return;
    var inputs=[].slice.call(sec.querySelectorAll('input.sg'));
    var saved={};try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
    inputs.forEach(function(i){if(saved[i.dataset.q]!==undefined)i.value=saved[i.dataset.q];i.addEventListener('input',sum)});
    function f(s){return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2)}
    function sum(){var t=0,o={};inputs.forEach(function(i){var v=parseFloat(i.value);if(!isNaN(v)){v=Math.max(0,Math.min(v,parseFloat(i.max)));t+=v;o[i.dataset.q]=v}});
      tot.textContent='Total: '+(Math.round(t*100)/100)+'/'+(tot.dataset.max||'25');try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
    sec.querySelector('.mk_start').onclick=function(){clearInterval(timer);timer=setInterval(function(){left--;tm.textContent='Time: '+f(Math.max(left,0));if(left<=0){clearInterval(timer);tm.textContent='Time is up — stop writing and self-grade.'}},1000)};
    sec.querySelector('.mk_stop').onclick=function(){clearInterval(timer)};
    sec.querySelector('.mk_reset').onclick=function(){clearInterval(timer);left=T0;tm.textContent='Time: '+f(left);inputs.forEach(function(i){i.value=''});sum()};
    sum();
  });
})();
