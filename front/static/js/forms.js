import { apiFetch } from "./utils.js";
import { showFile, receiveFile } from "./btns/uploaders.js";

export const initForms = () => {
    const forms = document.querySelectorAll('form[data-endpoint]');
    forms.forEach(form => {
        const endpoint = form.dataset.endpoint;
        const formId = form.id;
        // look for a button with type submit and form attribute equal to the form id
        const submitBtn = document.querySelector('button[type="submit"][form="' + formId + '"]');
    })
}