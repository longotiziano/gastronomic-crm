import configData from '../../../../config/config.json' with { type: 'json' };
import { apiFetch, loadTableData } from "../utils.js";

const debug = configData.debug_mode;

const renderMenu = (menuUl, data, col) => {
    if (debug) console.log(`Data received -> Data: ${JSON.stringify(data)}`);
    const name = menuUl.dataset.name;
    const htmlList = data.map(row => `<li><button data-${name}="${row[col]}">${row[col]}</button></li>`).join('');
    // inserting the HTML
    menuUl.innerHTML = htmlList;
};

/**
 * Looks for every div with ".menu" class and allows expanding and collapsing the menu
 */
export const initDisplayMenus = () => {
    const menus = document.querySelectorAll(".menu");
    menus.forEach(menu => {
        
        const desplegable = menu.querySelector(".desplegable");

        const menuUl = desplegable.querySelector("ul");
        const tableModel = menuUl.dataset.tablemodel;
        const col = configData.models[tableModel].cols_displayed;

        loadTableData(menuUl, 0, "", false, (menuUl, data) => renderMenu(menuUl, data, col));
        
        const btn = menu.querySelector(":scope > button");
        btn.addEventListener("click", () => desplegable.classList.toggle("active"));
        })
};

