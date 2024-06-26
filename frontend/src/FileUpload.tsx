import React, { useState } from 'react';
import axios from 'axios';

const FileUpload: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [newHeaders, setNewHeaders] = useState<string[]>([]);
    const [csvData, setCsvData] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
            setNewHeaders([]);
        }
    };

    const handleHeaderChange = (index: number, value: string) => {
        const headers = [...newHeaders];
        headers[index] = value;
        setNewHeaders(headers);
    };

    const addHeaderField = () => {
        setNewHeaders([...newHeaders, ""]);
    };

    const handleFileUpload = async () => {
        if (!file || newHeaders.length === 0) {
            alert("Please upload a file and add at least one new header.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        newHeaders.forEach((header) => {
            formData.append('new_headers', header);
        });

        try {
            const response = await axios.post('/upload/', formData, {
                responseType: 'blob',
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const responseText = await (await fetch(url)).text();
            setCsvData(responseText);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    const displayCSV = (csv: string) => {
        const rows = csv.split('\n');
        return (
            <table>
                <tbody>
                    {rows.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                            {row.split(',').map((col, colIndex) => (
                                <td key={colIndex}>{col}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    return (
        <div>
            <h1>Upload and Process CSV</h1>
            <input type="file" onChange={handleFileChange} />
            <div>
                <h2>Enter New Headers</h2>
                {newHeaders.map((header, index) => (
                    <input
                        key={index}
                        type="text"
                        placeholder={`Header ${index + 1}`}
                        value={header}
                        onChange={(e) => handleHeaderChange(index, e.target.value)}
                    />
                ))}
                <button onClick={addHeaderField}>+</button>
            </div>
            <button onClick={handleFileUpload}>Upload</button>
            <h2>Processed CSV</h2>
            {csvData && displayCSV(csvData)}
        </div>
    );
};

export default FileUpload;