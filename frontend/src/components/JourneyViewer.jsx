import React from 'react'

export default function JourneyViewer({events}){
return (
<div style={{marginTop:20}}>
<h3>Recent events</h3>
<ul>
{events.map((e,idx)=> (
<li key={idx}><strong>{e.event_type}</strong> — {e.timestamp}</li>
))}
</ul>
</div>
)
}
