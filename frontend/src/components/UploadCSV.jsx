import { useState } from 'react';

export default function UploadCSV() { 
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('');   
    const [loading, setLoading] = useState(false);

    const handleUpload = async () => {  
        if (!file) {
            setStattus('Please select a file first.');
            return;
        }

    const  formData = new FormData();
    formData.append('file', file);  
    setLoading(true);
    setStatus('Uploading...');  

    try {   
        const  res = await fetch("http://localhost:8000/upload", {
            method: 'POST', 
            body: formData     
        });
        if  (!res.ok) {
            throw new Error(`Upload failed`);
        } 
        const  data = await res.json();
        setStatus(`Upload successful: ${data.filename}  with ${data.rows} rows`);
    } catch (err) {
        console.error(err);
        setStatus(`Upload failed. Check backend logs.`);
    }   
 };

 return (
    <div>
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />    
        <button onClick={handleUpload} disabled={loading}>
            {loading ? 'Uploading...' : 'Upload CSV'}
        </button>
        <p>{status}</p>
    </div>
 );
}