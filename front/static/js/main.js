import { initSections } from './nav.js';
import { initSelectables } from './btns/selectables.js';
import { initUploaders } from './btns/uploaders.js';
import { initTables } from './tables/tables.js';
import { initDisplayMenus } from './menus.js';

initSelectables();
initDisplayMenus();
initSections();
initUploaders();
initTables();