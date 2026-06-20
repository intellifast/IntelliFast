let step=1; const steps=[...document.querySelectorAll('.onboard-step')];
const render=()=>{steps.forEach((s,i)=>s.classList.toggle('active',i===step-1));stepNo.textContent=step;stepBar.style.width=`${step*20}%`;prevBtn.disabled=step===1;nextBtn.hidden=step===5;finishBtn.hidden=step!==5;window.scrollTo({top:0,behavior:'smooth'})};
nextBtn.onclick=()=>{if(step<5){step++;render()}};prevBtn.onclick=()=>{if(step>1){step--;render()}};render();
