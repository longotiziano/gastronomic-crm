import { API_URL } from './config.js';

/**
 * received the file's container, the upload's svg, the file's span, the introduced file's name and the input element toggles the file's visibility
 * 
 * ### "show" parameter:
 * - if the "show" parameter is true, then it will show the file
 * - if false, will reset the upload button, including the input's value
 * 
 * @param {Element} uploader  
 * @param {string} fileName
 * @param {boolean} show
 */
export const showFile = (uploader, fileName, show) => {
    const divFiles = uploader.querySelector(':scope > div');
    const fileContainer = divFiles.querySelector(':scope > div');
    const uploadSvg = divFiles.querySelector(':scope > svg');
    const fileSpan = fileContainer.querySelector(':scope > span');
    // input
    const inputId = uploader.dataset.uploaderid;
    const input = document.getElementById(inputId);
    if (show) {
        fileContainer.style.visibility = 'visible';
        uploadSvg.style.visibility = 'hidden';
        fileSpan.textContent = fileName;
    } else if (!show) {
        fileContainer.style.visibility = 'hidden';
        uploadSvg.style.visibility = 'visible';
        fileSpan.textContent = "";        
        input.value = "";
    }
};

/**
 * receives the input element, the uploader's file trigger (not the submit button) and links it to it's input, allowing file's insertion.
 * 
 * for the inserted file, executes the provided callback with the file.
 * 
 * @param {Element} input 
 * @param {Element} trigger 
 * @param {Function} onFile 
 */
export const receiveFile = (input, trigger, onFile) => {
    trigger.onclick = () => input.click();
    input.onchange = function() {
        const file = this.files[0];
        if (file) {
            onFile(file);
        }
    };
};

/**
 * if the "submit" button is clicked, then submits the file to the received endpoint
 * 
 * Also receives the uploader to change to reset the uploader in case of success
 * 
 * @param {Element} submitBtn 
 * @param {File} file 
 * @param {string} endpoint
 * @param {Element} uploader 
 */
export const sendEndpointFile = (submitBtn, file, endpoint, uploader) => {
    const rId = new URLSearchParams(window.location.search).get('restaurant');
    // overwrite previous onclick to ensure only one file is sent per click
    submitBtn.onclick = async function() {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('r_id', rId);
        try {
            submitBtn.disabled = true; // Visual feedback
            const res = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });
            if (!res.ok) throw new Error(`Server error: ${res.status}`);
            const data = await res.json();
            console.log('Upload successful:', data);
            alert('Upload complete!');
            showFile(uploader, file.name, false);
        } catch (error) {
            console.error('Upload failed:', error);
        } finally {
            submitBtn.disabled = false;
        }
    };
};

/**
 * inits the uploaders buttons
 */
export const initUploaders = () => {
    document.querySelectorAll('.upload').forEach(uploader => {
        // general and default
        const divFiles = uploader.querySelector(':scope > div');
        const trigger = uploader.querySelector('div.actionable');
        // inside file's container after changes
        const fileContainer = divFiles.querySelector(':scope > div');
        const cancelSvg = fileContainer.querySelector(':scope > svg');
        // input
        const inputId = uploader.dataset.uploaderid;
        const input = document.getElementById(inputId);
        // submit
        const submitBtn = uploader.querySelector("button.actionable");

        receiveFile(input, trigger, (file) => {
            showFile(uploader, file.name, true);
            const endpoint = `${API_URL}${uploader.dataset.endpoint}`;
            sendEndpointFile(submitBtn, file, endpoint, uploader);
            cancelSvg.onclick = function (e) {
                e.stopPropagation();
                showFile(uploader, "", false);
            }
            });
    });
}