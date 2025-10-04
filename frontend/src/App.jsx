import React from 'react'
import CustomerSearch from './components/CustomerSearch'
import UploadCSV from './components/UploadCSV'


export default function App(){
return (
<div style={{padding:20}}>
<h1>Customer Journey MVP</h1>
<UploadCSV />
<CustomerSearch />
</div>
)
}