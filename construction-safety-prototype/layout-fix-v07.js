(function(){
  const baseFloor = floorScene;
  const baseLadder = ladderScene;
  const baseEdge = edgeScene;

  function layoutOverlay(kind, variantB){
    const side = variantB ? 'B' : 'A';
    let objects = '';
    if(kind === 'floor'){
      objects = variantB
        ? `<g filter="url(#shadow)"><g transform="translate(125 365)"><rect width="132" height="20" rx="3" fill="#8a5c36"/><rect y="25" width="132" height="20" rx="3" fill="#9b6a40"/><rect y="50" width="132" height="20" rx="3" fill="#78502f"/></g><g transform="translate(690 340) rotate(-8)"><rect width="115" height="12" rx="6" fill="#8296a4"/><rect y="18" width="115" height="12" rx="6" fill="#6f8290"/><rect y="36" width="115" height="12" rx="6" fill="#91a2ad"/></g></g>`
        : `<g filter="url(#shadow)"><g transform="translate(655 360)"><rect width="115" height="25" rx="4" fill="#7c8790"/><rect x="10" y="30" width="115" height="25" rx="4" fill="#69757f"/></g><g transform="translate(115 338) rotate(7)"><rect width="150" height="14" rx="5" fill="#a77845"/><rect y="21" width="150" height="14" rx="5" fill="#8d6037"/></g></g>`;
    } else if(kind === 'ladder'){
      objects = variantB
        ? `<g filter="url(#shadow)"><g transform="translate(105 365)"><rect width="135" height="24" rx="4" fill="#87603d"/><rect y="30" width="135" height="24" rx="4" fill="#6f4e33"/></g><g transform="translate(760 350)"><path d="M12 0L31 54H-7Z" fill="#efae35"/><rect x="-2" y="49" width="29" height="7" rx="3" fill="#f3c15a"/></g></g>`
        : `<g filter="url(#shadow)"><g transform="translate(690 375) rotate(-5)"><rect width="135" height="12" rx="6" fill="#7f93a1"/><rect y="19" width="135" height="12" rx="6" fill="#687c89"/><rect y="38" width="135" height="12" rx="6" fill="#94a4ae"/></g><rect x="125" y="350" width="95" height="58" rx="5" fill="#6a747e" stroke="#9aa5ae"/></g>`;
    } else {
      objects = variantB
        ? `<g filter="url(#shadow)"><g transform="translate(145 368)"><rect width="150" height="19" rx="3" fill="#875c39"/><rect y="24" width="150" height="19" rx="3" fill="#9c7046"/></g><g transform="translate(345 392)"><rect width="115" height="38" rx="5" fill="#5e6a74"/><path d="M10 10h95M10 22h95" stroke="#8a969f" stroke-width="3"/></g></g>`
        : `<g filter="url(#shadow)"><g transform="translate(205 372) rotate(5)"><rect width="155" height="12" rx="6" fill="#8093a0"/><rect y="19" width="155" height="12" rx="6" fill="#6d808d"/></g><rect x="390" y="398" width="92" height="35" rx="5" fill="#72513a"/></g>`;
    }
    return `${objects}<g transform="translate(320 88)"><rect width="260" height="31" rx="15" fill="#0b2639" fill-opacity=".96" stroke="#43d0ee" stroke-opacity=".65"/><circle cx="18" cy="15.5" r="5" fill="#43d0ee"/><text x="32" y="19" font-size="9" fill="#e1f8ff" font-weight="800">LAYOUT VARIANT ${side} · HAZARD STATE PRESERVED</text></g>`;
  }

  function inject(markup, kind, variantB){
    const subtitle = `layout variant ${variantB ? 'B' : 'A'} — non-hazard objects relocated`;
    return markup
      .replace('baseline hazard exposed', subtitle)
      .replace('baseline ladder on unstable support', subtitle)
      .replace('baseline exposed perimeter', subtitle)
      .replace('</svg>', `${layoutOverlay(kind, variantB)}</svg>`);
  }

  floorScene = function(mode, toolRight){
    const out = baseFloor(mode, toolRight);
    return mode === 'move' ? inject(out, 'floor', toolRight) : out;
  };
  ladderScene = function(mode, toolRight){
    const out = baseLadder(mode, toolRight);
    return mode === 'move' ? inject(out, 'ladder', toolRight) : out;
  };
  edgeScene = function(mode, toolRight){
    const out = baseEdge(mode, toolRight);
    return mode === 'move' ? inject(out, 'edge', toolRight) : out;
  };

  const baseState = stateForMode;
  stateForMode = function(){
    const a = baseState();
    if(a && S.scene && S.mode === 'move'){
      a.transform = `Layout perturbation · Variant ${S.toolRight ? 'B' : 'A'}`;
      a.relation = 'PRESERVE';
    }
    return a;
  };

  const baseButtons = updateVariantButtons;
  updateVariantButtons = function(){
    baseButtons();
    const c = config();
    if(!c) return;
    $('vMoveTitle').textContent = 'Generate layout variant';
    $('vMoveText').textContent = `Relocate toolbox and non-hazard materials while preserving the ${c.family} safety meaning.`;
  };

  const baseApply = apply;
  apply = function(m){
    baseApply(m);
    if(m === 'move' && S.scene){
      const c = config();
      log('Layout variant', `Variant ${S.toolRight ? 'B' : 'A'} instantiated: toolbox and non-hazard materials were relocated; ${c.hazard} remains ${c.baseJudgment}.`);
      toast(`Layout variant ${S.toolRight ? 'B' : 'A'} generated`);
    }
  };

  const version = [...document.querySelectorAll('.meta span')].find(x => x.textContent.includes('Validator'));
  if(version) version.innerHTML = 'Validator <b>v0.7</b>';
  if(S.hazardKey) updateVariantButtons();
  renderScene();
})();
