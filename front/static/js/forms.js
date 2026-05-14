import { apiFetch } from "./utils.js";
import { showFile, receiveFile } from "./btns/uploaders.js";

export const initForms = () => {
    const forms = document.querySelectorAll('form[data-endpoint]');
    forms.forEach(form => {
        const endpoint = form.dataset.endpoint;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            try {
                const formData = new FormData(form);
                const data = await apiFetch(endpoint, {
                    method: 'POST',
                    body: formData
                });
                console.log('Success:', data);
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
}