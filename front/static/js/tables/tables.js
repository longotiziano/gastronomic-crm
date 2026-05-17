import { obtainRId, loadTableData } from "../utils.js";
import { tableSearcher } from "../btns/searcher.js";
import { apiFetch } from "../utils.js";
import { initEditBtns } from "../btns/edit.js";

import configData from '../../../../config/config.json' with { type: 'json' };
const debug = configData.debug_mode;

/**
 * received the table's container, it's data and it's columns, creates the HTML of the table
 * 
 * @param {Element} tableContainer
 * @param {Array} data
 * @param {Array} cols
 */
const renderTable = (tableContainer, data, cols) => {
    // making the columns
    const htmlCols = cols.map(col => `<th>${col}</th>`).join('');
    const htmlHeader = `<tr>${htmlCols}</tr>`;
    // making the rows 
    const htmlRows = data.map(row => {
        const rowData = cols.map(col => `<td>${row[col]}</td>`).join('');
        return `<tr>${rowData}<td class="edit-btn"></td></tr>`;
    }).join('');
    // inserting the HTML
    tableContainer.innerHTML = `
        <table>
            <thead>${htmlHeader}</thead>
            <tbody>${htmlRows}</tbody>
        </table>
    `;
    initEditBtns(tableContainer);
};

/**
 * 
 * 
 * @returns {string}
 */
const renderPagination = (prev, next) => {
    // botones de prev/next con los offsets
};

export const initTables = () => {
    const tables = document.querySelectorAll('.table-container');
    tables.forEach(table => {
        if (debug) console.log(`Initializing table -> Table: ${table.outerHTML}`);
        const searcher = table.parentElement.querySelector('.searcher > input');
        if (debug) console.log(searcher.outerHTML);
        const tableModel = table.dataset.tablemodel;
        const cols = configData.models[tableModel].cols_displayed;
        if (debug) console.log(`Columns finded -> Columns: ${cols} | Function: ${initTables.name}`);
        // creates the table for the first time
        loadTableData(table, 0, "", true, (container, data) => renderTable(container, data, cols));
        tableSearcher(searcher, (lookedName) => {
            loadTableData(table, 0, lookedName, true, (container, data) => renderTable(container, data, cols));
        });
    });
};