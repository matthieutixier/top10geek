(function(){
  try{
    var btn=document.getElementById('navToggle'), nav=document.getElementById('topnav');
    btn.addEventListener('click',function(){var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false');});
  }catch(e){}

  var DATA=window.T10G||{}, L=DATA.laptops||{};
  var card=document.getElementById('detailCard');
  if(!card) return;
  var chart=document.getElementById('bubbleChart'), table=document.getElementById('dataTable');
  function $(id){return document.getElementById(id);}
  function fill(el,arr){el.innerHTML='';arr.forEach(function(s){var sp=document.createElement('span');sp.className='s';sp.textContent=s;el.appendChild(sp);});}

  function select(id,opts){
    var d=L[id]; if(!d) return;
    $('detailName').textContent=d.short;
    $('detailRef').textContent=d.ref;
    var p=$('detailPress');
    if(d.press){ p.className='score big-press'; p.innerHTML='<span class="pn">'+d.press.avg+'</span><span class="pd">/10</span><span class="pc">presse · '+d.press.n+' test'+(d.press.n>1?'s':'')+(d.press.gamme?' · gamme':'')+'</span>'; }
    else { p.className='score big-press none'; p.innerHTML='<span class="pn">—</span><span class="pc">pas encore testé</span>'; }
    $('detailRating').textContent=d.rating;
    $('mIdx').hidden=!d.idxv; if(d.idxv){ $('detailIdxBar').style.width=(d.idxv*10)+'%'; $('mIdx').title="Indice d'équipement : "+d.idx+'/10'; }
    $('mWeight').hidden=(d.weight==='n.c.'); $('detailWeight').textContent=d.weight;
    $('mAuton').hidden=(d.auton==='n.c.'); $('detailAuton').textContent=d.auton;
    $('detailPrice').textContent=d.price;
    $('detailVerdict').textContent=d.verdict;
    var b=$('detailBadge'); b.textContent=d.badge; b.className='fbadge'+(d.badge==='Le choix de la bande'?'':' alt');
    $('detailCatLabel').textContent=d.catLabel;
    $('detailArt').className='art cat-'+d.cat;
    $('detailArtImg').src=DATA.root+'assets/img/badge-'+d.slug+'.webp';
    fill($('detailStrengths'),d.strengths);
    fill($('detailWeak'),d.weak.length?d.weak:[d.tested?'Aucun défaut majeur relevé par la presse':'Défauts non documentés : pas encore de test presse']);
    $('detailCta').href=d.url;
    $('detailMore').href=DATA.root+'pc-portable/'+d.slug+'/index.html#'+id;
    if(chart) chart.querySelectorAll('.bubble').forEach(function(c){c.classList.toggle('selected',c.getAttribute('data-id')===id);});
    if(table) table.querySelectorAll('tbody tr').forEach(function(r){r.classList.toggle('selected',r.getAttribute('data-id')===id);});
    if(!(opts&&opts.skipScroll)){ card.scrollIntoView({behavior:'smooth',block:window.innerWidth<=900?'start':'nearest'}); }
  }
  if(chart) chart.querySelectorAll('.bubble').forEach(function(c){
    c.addEventListener('click',function(){select(c.getAttribute('data-id'));});
    c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();select(c.getAttribute('data-id'));}});
  });
  if(table) table.querySelectorAll('tbody tr').forEach(function(r){
    r.addEventListener('click',function(){select(r.getAttribute('data-id'),{skipScroll:true});});
    r.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();select(r.getAttribute('data-id'),{skipScroll:true});}});
  });

  // Filtre par usage (accueil)
  var pills=document.querySelectorAll('#usageFilter .pill[data-filter]');
  pills.forEach(function(p){p.addEventListener('click',function(){
    var cat=p.getAttribute('data-filter');
    chart.querySelectorAll('.bubble').forEach(function(c){c.classList.toggle('dimmed',cat!=='all'&&c.getAttribute('data-cat')!==cat);});
    table.querySelectorAll('tbody tr').forEach(function(r){r.classList.toggle('row-hidden',cat!=='all'&&r.getAttribute('data-cat')!==cat);});
    pills.forEach(function(x){x.setAttribute('aria-pressed',x===p?'true':'false');});
  });});

  // Filtre par budget (pages usage)
  var bp=document.querySelectorAll('#budgetFilter .pill');
  bp.forEach(function(p){p.addEventListener('click',function(){
    var f=p.getAttribute('data-budget-filter'), shown=0, firstId=null;
    chart.querySelectorAll('.bubble').forEach(function(c){c.classList.toggle('dimmed',f!=='all'&&c.getAttribute('data-budget')!==f);});
    table.querySelectorAll('tbody tr').forEach(function(r){r.classList.toggle('row-hidden',f!=='all'&&r.getAttribute('data-budget')!==f);});
    document.querySelectorAll('.fiche').forEach(function(a){var ok=(f==='all'||a.getAttribute('data-budget')===f);a.hidden=!ok;if(ok){shown++; if(!firstId) firstId=a.id;}});
    var en=$('emptyNote'); if(en) en.hidden=shown>0;
    bp.forEach(function(x){x.setAttribute('aria-pressed',x===p?'true':'false');});
    if(firstId) select(firstId,{skipScroll:true});
  });});

  // Tri du tableau
  try{
    var tbody=table.querySelector('tbody'), st={key:null,dir:1};
    function val(r,k){
      if(k==='name') return r.querySelector('.name-cell').textContent.trim().toLowerCase();
      if(k==='cat') return r.getAttribute('data-cat');
      return parseFloat(r.getAttribute('data-'+k));
    }
    table.querySelectorAll('th[data-sort]').forEach(function(th){th.addEventListener('click',function(){
      var k=th.getAttribute('data-sort'); st.dir=(st.key===k)?-st.dir:(k==='price'||k==='name'||k==='cat'?1:-1); st.key=k;
      table.querySelectorAll('th[data-sort]').forEach(function(h){h.removeAttribute('aria-sort');});
      th.setAttribute('aria-sort',st.dir===1?'ascending':'descending');
      var rows=Array.prototype.slice.call(tbody.querySelectorAll('tr'));
      rows.sort(function(a,b){var va=val(a,k),vb=val(b,k);
        if(k==='rating'||k==='press'){ if(va===-1&&vb!==-1) return 1; if(vb===-1&&va!==-1) return -1; }
        return va<vb?-st.dir:(va>vb?st.dir:0);});
      rows.forEach(function(r){tbody.appendChild(r);});
    });});
  }catch(e){}

  select(DATA.first,{skipScroll:true});
})();
