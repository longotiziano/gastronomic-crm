import { initSections } from './nav.js';
import { initSelectables } from './btns/selectables.js';
import { initUploaders } from './btns/uploaders.js';
import { initTables } from './tables/tables.js';
import { initDisplayMenus } from './tables/menus.js';
import { initModals } from './modals.js';
import { initForms } from './forms.js';

initDisplayMenus();
initSections();
initUploaders();
initTables();
initSelectables();
initModals();
initForms();