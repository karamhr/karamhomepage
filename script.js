const header=document.querySelector('.site-header');
const menu=document.querySelector('.menu-button');
window.addEventListener('scroll',()=>header?.classList.toggle('scrolled',scrollY>24),{passive:true});
menu?.addEventListener('click',()=>{const open=header.classList.toggle('menu-open');menu.setAttribute('aria-expanded',String(open))});
document.querySelectorAll('.nav a').forEach(a=>a.addEventListener('click',()=>{header?.classList.remove('menu-open');menu?.setAttribute('aria-expanded','false')}));
const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target)}}),{threshold:.14});
document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));
const art=document.querySelector('.labor-art');
document.querySelector('.motion-hero')?.addEventListener('mousemove',e=>{if(!art||matchMedia('(prefers-reduced-motion: reduce)').matches)return;const r=e.currentTarget.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;art.style.setProperty('--mx',`${x*13}px`);art.style.setProperty('--my',`${y*13}px`)});
const form=document.querySelector('.form');
if(form)form.addEventListener('submit',e=>{e.preventDefault();form.reset();const n=document.querySelector('.notice');if(n){n.style.display='block';n.scrollIntoView({behavior:'smooth',block:'center'})}});
const footer=document.querySelector('footer.footer');
if(footer){footer.classList.add('footer-rich');footer.innerHTML=`<div class="wrap footer-rich-main"><div class="footer-identity"><a class="brand" href="index.html"><span class="brand-mark">K</span><span>노무법인 <b>가람경영컨설팅</b><small>MANAGEMENT CONSULTING</small></span></a><a class="footer-phone" href="tel:031-755-0052"><span aria-hidden="true">☎</span>031-755-0052</a></div><div class="office-list"><p><b>성남</b><i>ㅣ</i>경기도 성남시 분당구 성남대로916번길 7, 서일빌딩 401호</p><p><b>수원</b><i>ㅣ</i>경기도 수원시 장안구 장안로418-41</p><p><b>마포</b><i>ㅣ</i>서울특별시 마포구 만리재로 15, 제일빌딩 603호</p></div></div><div class="wrap footer-rich-meta"><span>대표 노무사 김기호</span><span>사업자등록번호 129-85-28418</span><span>© 2026 KARAM MANAGEMENT CONSULTING. ALL RIGHTS RESERVED.</span></div>`;}
