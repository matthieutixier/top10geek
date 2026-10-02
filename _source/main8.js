(function(){
  try{
    var btn=document.getElementById('navToggle'), nav=document.getElementById('topnav');
    btn.addEventListener('click',function(){var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false');});
  }catch(e){}

  var DATA=window.T10G||{}, L=DATA.laptops||{};
  var card=document.getElementById('detailCard');
  if(!card) return;
  var chart=document.getElementById('bubbleChart'), list=document.getElementById('topList');
  function $(id){return document.getElementById(id);}
  function fill(el,arr){el.innerHTML='';arr.forEach(function(s){var sp=document.createElement('span');sp.className='s';sp.textContent=s;el.appendChild(sp);});}

  function select(id,opts){
    var d=L[id]; if(!d) return;
    $('detailName').textContent=d.short;
    $('detailRef').textContent=d.ref;
    var p=$('detailPress');
    if(d.press){ p.className='score big-press'; p.innerHTML='<span class="pn">'+d.press.avg+'</span><span class="pd">/10</span><span class="pc">presse · '+d.press.n+' note'+(d.press.n>1?'s':'')+(d.press.gamme?' · gamme':'')+'</span>'; }
    else { p.className='score big-press none'; p.innerHTML='<span class="pn">—</span><span class="pc">'+d.ntests+' test'+(d.ntests>1?'s':'')+' · sans note</span>'; }
    $('detailRating').textContent=d.rating; $('mR').hidden=!d.rating;
    [['mA','mAk','mAv'],['mB','mBk','mBv']].forEach(function(ids,i){ var kv=d.m[i]; $(ids[0]).hidden=(!kv[1]||kv[1]==='n.c.'); $(ids[1]).textContent=kv[0]; $(ids[2]).textContent=kv[1]; });
    $('detailPrice').textContent=d.price;
    $('detailVerdict').textContent=d.verdict;
    var b=$('detailBadge'); b.textContent=d.badge; b.className='fbadge'+(d.badge==='Le choix de la bande'?'':' alt');
    $('detailCatLabel').textContent=d.catLabel;
    $('detailArt').className='art art-photo cat-'+d.cat;
    $('detailArtImg').src=d.img?(DATA.root+'assets/img/p/'+d.img):(DATA.root+'assets/img/badge-'+d.badgeImg+'.webp');
    $('detailArtImg').alt=d.short;
    $('detailCatImg').src=DATA.root+'assets/img/badge-'+d.badgeImg+'.webp';
    var ob=$('detailOffers'); ob.innerHTML='';
    (d.offers||[]).forEach(function(o){var a=document.createElement('a');a.className='offer';a.href=o[2];a.target='_blank';a.rel='nofollow sponsored noopener';
      [['o-m',o[0]],['o-c',o[3]||''],['o-p',o[1]],['o-go','Voir →']].forEach(function(x){var e=document.createElement(x[0]==='o-p'?'b':'span');e.className=x[0];e.textContent=x[1];a.appendChild(e);});ob.appendChild(a);});
    fill($('detailStrengths'),d.strengths);
    fill($('detailWeak'),d.weak.length?d.weak:['Aucun défaut majeur relevé par la presse']);
    $('detailCta').href=d.url; if(d.offers&&d.offers.length){ $('detailCta').textContent="Voir l'offre chez "+d.offers[0][0]+' →'; }
    $('detailMore').href=DATA.root+d.purl;
    if(chart) chart.querySelectorAll('.bubble').forEach(function(c){c.classList.toggle('selected',c.getAttribute('data-id')===id);});
    if(!(opts&&opts.skipScroll)){ card.scrollIntoView({behavior:'smooth',block:window.innerWidth<=900?'start':'nearest'}); }
  }
  if(chart) chart.querySelectorAll('.bubble').forEach(function(c){
    c.addEventListener('click',function(){select(c.getAttribute('data-id'));});
    c.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();select(c.getAttribute('data-id'));}});
  });

  // Filtre par usage (pages comparatif)
  var pills=document.querySelectorAll('#usageFilter .pill[data-filter]');
  pills.forEach(function(p){p.addEventListener('click',function(){
    var cat=p.getAttribute('data-filter'), firstId=null;
    chart.querySelectorAll('.bubble').forEach(function(c){var off=cat!=='all'&&c.getAttribute('data-cat')!==cat;c.classList.toggle('dimmed',off);});
    for(var id in L){ if(cat==='all'||L[id].cat===cat){ firstId=id; break; } }
    pills.forEach(function(x){x.setAttribute('aria-pressed',x===p?'true':'false');});
    if(firstId) select(firstId,{skipScroll:true});
  });});

  // Filtre par budget (pages usage)
  var bp=document.querySelectorAll('#budgetFilter .pill');
  bp.forEach(function(p){p.addEventListener('click',function(){
    var f=p.getAttribute('data-budget-filter'), shown=0, firstId=null;
    if(chart) chart.querySelectorAll('.bubble').forEach(function(c){c.classList.toggle('dimmed',f!=='all'&&c.getAttribute('data-budget')!==f);});
    document.querySelectorAll('.fiche').forEach(function(a){var ok=(f==='all'||a.getAttribute('data-budget')===f);a.hidden=!ok;if(ok){shown++; if(!firstId) firstId=a.id;}});
    // le message « aucun modèle » n'existe dans la page que s'il y a lieu de l'afficher
    var en=$('emptyNote');
    if(!shown&&!en&&list){ en=document.createElement('p'); en.id='emptyNote'; en.className='empty-note'; en.textContent='Aucun modèle de cette sélection dans cette tranche de prix.'; list.parentNode.insertBefore(en,list); }
    if(en) en.hidden=shown>0;
    bp.forEach(function(x){x.setAttribute('aria-pressed',x===p?'true':'false');});
    if(firstId) select(firstId,{skipScroll:true});
  });});

  // Tri des fiches
  var sortSel=$('sortBy');
  if(sortSel&&list){ sortSel.addEventListener('change',function(){
    var k=sortSel.value, items=Array.prototype.slice.call(list.querySelectorAll('.fiche'));
    function n(a,key){return parseFloat(a.getAttribute('data-'+key));}
    items.sort(function(a,b){
      var byRank=n(a,'rank')-n(b,'rank');
      if(k==='price-asc') return (n(a,'price')-n(b,'price'))||byRank;
      if(k==='price-desc') return (n(b,'price')-n(a,'price'))||byRank;
      if(k==='press') return (n(b,'press')-n(a,'press'))||byRank;
      if(k==='tests') return (n(b,'tests')-n(a,'tests'))||byRank;
      return byRank;
    });
    items.forEach(function(a){list.appendChild(a);});
  }); }

  select(DATA.first,{skipScroll:true});
})();
