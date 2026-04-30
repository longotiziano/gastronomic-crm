import { initDisplayMenus, initSections } from './nav.js';
import { initSelectables } from './btns/selectables.js';
import { initUploaders } from './btns/uploaders.js';
import { loadProducts } from './tables/tables.js'

initSelectables();
initDisplayMenus();
initSections();
initUploaders();
loadProducts();