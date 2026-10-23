/* Local what-if expiry models only. No quotes, network, orders or storage. */
(function () {
  'use strict';
  function validate(p) {
    if (!['call','put'].includes(p.option_type) || !['debit','credit'].includes(p.kind)) throw Error('Unsupported vertical');
    for (const key of ['long_strike','short_strike','premium','fees','quantity','multiplier']) if (!Number.isFinite(p[key])) throw Error('Enter finite values in every input.');
    const width = Math.abs(p.long_strike-p.short_strike);
    const debit = p.option_type === 'call' ? p.long_strike < p.short_strike : p.long_strike > p.short_strike;
    if (Math.min(p.long_strike,p.short_strike)<=0 || !width || debit !== (p.kind==='debit')) throw Error('Invalid vertical legs.');
    if (p.premium<0 || p.premium>width || p.fees<0) throw Error('Premium must be between zero and strike width; total fees must be nonnegative.');
    if (![p.quantity,p.multiplier].every(x=>Number.isInteger(x)&&x>=1)) throw Error('Quantity and multiplier must be positive whole numbers.');
  }
  function payoff(p,s) {
    const sign=p.option_type==='call'?1:-1;
    return (Math.max(sign*(s-p.long_strike),0)-Math.max(sign*(s-p.short_strike),0))*p.quantity*p.multiplier;
  }
  function pnl(p,s) {return payoff(p,s)+(p.kind==='credit'?1:-1)*p.premium*p.quantity*p.multiplier-p.fees;}
  function summary(p) {
    validate(p);
    const lo=Math.min(p.long_strike,p.short_strike),hi=Math.max(p.long_strike,p.short_strike),a=pnl(p,lo),b=pnl(p,hi);
    const best=Math.max(a,b),worst=Math.min(a,b);let breakeven=null;
    if(a*b<0) breakeven={type:'point',value:lo-a*(hi-lo)/(b-a)};
    else if(Math.abs(a)<1e-9) breakeven={type:'region',minimum:0,maximum:lo};
    else if(Math.abs(b)<1e-9) breakeven={type:'region',minimum:hi,maximum:null};
    return {best,worst,max_profit:Math.max(0,best),max_loss:Math.max(0,-worst),breakeven};
  }
  function breakevenText(b) {
    if(!b) return 'None under these assumptions';
    if(b.type==='point') return b.value.toFixed(2);
    return b.maximum===null ? `Underlying ≥ ${b.minimum.toFixed(2)} (zero-P&L region)` : `Underlying 0–${b.maximum.toFixed(2)} (zero-P&L region)`;
  }
  function chart(p) {
    validate(p);
    const lo=Math.min(p.long_strike,p.short_strike),hi=Math.max(p.long_strike,p.short_strike),w=hi-lo;
    const xs=[Math.max(0,lo-w),lo,hi,hi+w];
    const values=[0,...xs.map(s=>pnl(p,s)),...xs.map(s=>payoff(p,s))];
    let bottom=Math.min(...values),top=Math.max(...values),pad=Math.max((top-bottom)*.15,1);bottom-=pad;top+=pad;
    const x=s=>56+(s-xs[0])/(xs[3]-xs[0])*370,y=v=>208-(v-bottom)/(top-bottom)*170;
    const path=fn=>xs.map((s,i)=>(i?'L':'M')+x(s).toFixed(2)+','+y(fn(p,s)).toFixed(2)).join(' ');
    return {payoff_path:path(payoff),pnl_path:path(pnl),zero_y:y(0),top,bottom,minimum:xs[0],maximum:xs[3]};
  }
  if (typeof module !== 'undefined' && module.exports) module.exports={payoff,pnl,summary,chart};
  if (typeof document === 'undefined') return;
  const money=x=>'USD '+x.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
  for(const box of document.querySelectorAll('.pnl-profile')) {
    const original=JSON.parse(box.dataset.profile),plot=box.querySelector('.pnl-plot');
    function update() {
      const p={...original};
      try {
        for(const input of box.querySelectorAll('input[data-field]')) {
          if(!input.value.trim()) throw Error('Enter every assumption; a blank input is not zero.');
          p[input.dataset.field]=Number(input.value);
        }
        const r=summary(p),g=chart(p),svg=box.querySelector('svg');plot.hidden=false;
        svg.querySelector('.pnl-line').setAttribute('d',g.pnl_path);
        svg.querySelector('.payoff-line').setAttribute('d',g.payoff_path);
        svg.querySelector('.pnl-axis').setAttribute('y1',g.zero_y);svg.querySelector('.pnl-axis').setAttribute('y2',g.zero_y);
        svg.querySelector('[data-label="top"]').textContent=g.top.toFixed(0);
        svg.querySelector('[data-label="bottom"]').textContent=g.bottom.toFixed(0);
        box.querySelector('[data-result="profit"]').textContent=money(r.max_profit);
        box.querySelector('[data-result="loss"]').textContent=money(r.max_loss);
        box.querySelector('[data-result="breakeven"]').textContent=breakevenText(r.breakeven);
        const comparison=original.cap===null?'Cap unset':r.max_loss<=original.cap?'Within model cap':'EXCEEDS model cap';
        box.querySelector('[data-result="eligibility"]').textContent=comparison+' under assumed inputs; executable eligibility UNVERIFIED. Actual premium, fees, multiplier, listing and opening confirmation still require verification.';
        box.querySelector('[data-result="regime"]').textContent=r.best<0?'All modeled expiry outcomes lose money.':'';
        box.querySelector('[data-result="error"]').textContent='';
      } catch(e) {
        plot.hidden=true;
        box.querySelector('[data-result="regime"]').textContent='';
        for(const key of ['profit','loss','breakeven'])box.querySelector(`[data-result="${key}"]`).textContent='Unavailable';
        box.querySelector('[data-result="eligibility"]').textContent='Model invalid; no risk-cap conclusion.';
        box.querySelector('[data-result="error"]').textContent=e.message;
      }
    }
    box.addEventListener('input',update);update();
  }
})();
