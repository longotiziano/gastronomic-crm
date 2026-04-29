import { initDisplayMenus, initSections } from './nav.js';
import { initSelectables } from './selectables.js';
import { initUploaders } from './uploaders.js';
import { loadProducts } from './tables.js'

initSelectables();
initDisplayMenus();
initSections();
initUploaders();
loadProducts();