import { StrictMode, useCallback, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { SnapRail, type SnapRailController } from '/home/maynkudu/Code/Projects/modulo/src/registry/snap-rail/SnapRail';
declare global { interface Window { rails: Record<string,SnapRailController>; commits: string[]; cancellations: number; fixture: { unmount:()=>void; mount:()=>void }; } }
window.rails={};window.commits=[];window.cancellations=0;
const detents=[{id:'left',label:'Left',position:0},{id:'center',label:'Center',position:50},{id:'right',label:'Right',position:100}];
function Fixture() {
  const [selectedId,setSelectedId]=useState('center'),[reduced,setReduced]=useState(false),[disabled,setDisabled]=useState(false),[accept,setAccept]=useState(true);
  const mainReady=useCallback((controller:SnapRailController|null)=>{if(controller)window.rails.main=controller;else delete window.rails.main;},[]);
  const secondaryReady=useCallback((controller:SnapRailController|null)=>{if(controller)window.rails.secondary=controller;else delete window.rails.secondary;},[]);
  const onlyReady=useCallback((controller:SnapRailController|null)=>{if(controller)window.rails.only=controller;else delete window.rails.only;},[]);
  return <main><h1>Snap rail fixture</h1><section aria-label="Controlled fixture"><SnapRail ariaLabel="Main snap position" detents={detents} selectedId={selectedId} onSelectionChange={id=>{if(accept)setSelectedId(id);}} reducedMotion={reduced} disabled={disabled} onSelectionCommit={id=>window.commits.push(id)} onSelectionCancel={()=>window.cancellations++} onReady={mainReady}/></section>
    <div className="controls"><label><input type="checkbox" checked={reduced} onChange={event=>setReduced(event.currentTarget.checked)}/> Reduce motion</label><label><input type="checkbox" checked={disabled} onChange={event=>setDisabled(event.currentTarget.checked)}/> Disable rail</label><label><input type="checkbox" checked={accept} onChange={event=>setAccept(event.currentTarget.checked)}/> Accept selection</label><button onClick={()=>window.rails.main.replay()}>Play sequence</button><button onClick={()=>setSelectedId('left')}>Select left</button><button onClick={()=>setSelectedId('right')}>Select right</button></div>
    <section aria-label="Uncontrolled fixture"><h2>Independent uncontrolled rail</h2><SnapRail ariaLabel="Secondary snap position" detents={detents} defaultSelectedId="center" onReady={secondaryReady}/></section>
    <section aria-label="One detent fixture"><h2>One detent</h2><SnapRail ariaLabel="Only snap position" detents={[{id:'only',label:'Only',position:7}]} onReady={onlyReady}/></section></main>;
}
const host=document.getElementById('root');if(!host)throw new Error('Fixture host missing');
let root=createRoot(host);
const mount=()=>root.render(<StrictMode><Fixture/></StrictMode>);
window.fixture={unmount(){root.unmount();},mount(){root=createRoot(host);mount();}};
mount();
