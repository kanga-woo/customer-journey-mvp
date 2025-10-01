import React, {useState} from 'react'
import axios from 'axios'
import JourneyViewer from './JourneyViewer'


export default function CustomerSearch(){
const [id, setId] = useState('')
const [events, setEvents] = useState(null)


async function lookup(){
try{
const res = await axios.get(`/api/customers/${encodeURIComponent(id)}/journey`)
setEvents(res.data.events)
}catch(e){
alert('error fetching')
}
}


return (
<div>
<input value={id} onChange={e=>setId(e.target.value)} placeholder="customer_id or email" />
<button onClick={lookup}>Lookup</button>
{events && <JourneyViewer events={events} />}
</div>
)
}
