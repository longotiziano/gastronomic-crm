import { changeSection, showSection } from './nav.js';
import { createIndexObject } from './utils.js';

const btns = document.querySelectorAll('.section-ul button');
const sectionsList = document.querySelectorAll('main > div'); 
const sections = createIndexObject(sectionsList)

btns.forEach(btn => {
    btn.addEventListener('click', () => {
        changeSection(btn, btns);
        showSection(sections, btn.dataset.section);
    });
});