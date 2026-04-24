import { API_URL } from './config.js';

/**
 * received an uploader element and a file's name, changes the visibility between the upload button and the file's name
 * 
 * @param {Element} uploader  
 * @param {string} fileName
 */
export const showFile = (uploader, fileName) => {
    const divFiles = uploader.querySelector(':scope > div');
    const uploadSvg = divFiles.querySelector(':scope > svg');
    const fileContainer = divFiles.querySelector(':scope > div');
    const fileSpan = fileContainer.querySelector(':scope > span');
    fileContainer.style.visibility = 'visible';
    uploadSvg.style.visibility = 'hidden';
    fileSpan.textContent = fileName;
};

/**
 * receives an uploader and links it to it's input, allowing file's insertion.
 * 
 * for the inserted file, executes the provided callback with the file.
 * 
 * @param {Element} uploader 
 * @param {Function} onFile 
 */
export const receiveFile = (uploader, onFile) => {
    const inputId = uploader.dataset.uploaderid;
    const input = document.getElementById(inputId);
    const trigger = uploader.querySelector('.actionable');    
    trigger.addEventListener('click', () => input.click());
    
    input.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            console.log(`File detected on the uploader -> Input ID: ${inputId} | File's name: ${file.name}`)
            onFile(file);
        }
    });
}

/**
 * receives the file and sends the 
 * 
 * for the inserted file, executes the provided callback with the file.
 * 
 * @param {Element} uploader 
 * @param {Function} onFile 
 */
export const sendEndpointFile = async (file, endpoint) => {
    const rId = new URLSearchParams(window.location.search).get('restaurant');
    const formData = new FormData();
    formData.append('file', file)
    formData.append('r_id', rId)
    for (let [key, value] of formData.entries()) {
    console.log(`${key}:`, value);
    }
    try {
        const res = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        console.log(data);
    } catch (error) {
        console.error('Error al subir el archivo:', error);
    }
};

/**
 * looks for every object with class .upload and applies:
 * - receiveFile()
 * - showFile() -> (in case of success)
 */
export const initUploaders = () => {
    document.querySelectorAll('.upload').forEach(uploader => {
        receiveFile(uploader, (file) => {
            showFile(uploader, file.name);
            const endpoint = `${API_URL}${uploader.dataset.endpoint}`;
            sendEndpointFile(file, endpoint);
            })
    });
};