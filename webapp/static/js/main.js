import { showSection, initDisplayMenus } from './nav.js';
import { createIndexObject } from './utils.js';
import { selectOption, initSelectables } from './selectables.js';

const btnsSection = document.querySelectorAll('.section-ul button');
const sectionsList = document.querySelectorAll('main > div'); 
const sections = createIndexObject(sectionsList)

initSelectables()
initDisplayMenus()

btnsSection.forEach(btn => {
    btn.addEventListener('click', () => {
        selectOption(btn, btnsSection);
        showSection(sections, btn.dataset.section);
    });
});