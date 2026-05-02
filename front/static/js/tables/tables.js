import configData from '../../../../config.json' with { type: 'json' };
import { obtainRId } from "../utils.js";
import { tableSearcher } from "../btns/searcher.js";

const API_URL = configData.api_url;
const debug = configData.debug_mode;

/**
 * received the table's container, the offset and the looked name, returns it's endpoint' data
 * 
 * @param {Element} tableContainer
 * @param {Number} offset
 * @param {string} lookedName
 * @returns {Array}
 */
const loadTableData = async (tableContainer, offset, lookedName) => {
    const rId = obtainRId();
    const endpoint = `${API_URL}${tableContainer.dataset.endpoint}`;
    const tableModel = tableContainer.dataset.tablemodel;

    const res = await fetch(`${endpoint}?offset=${offset}&looked_name=${lookedName}&restaurant=${rId}`);
    const data = await res.json();

    const dataArray = data.data[tableModel];
    if (debug) dataArray.map(obj => console.log(obj));
    return dataArray;
}

/**
 * received the table's container, it's data and it's columns, creates the HTML of the table
 * 
 * @param {Element} tableContainer
 * @param {Array} data
 * @param {Array} cols
 */
const renderTable = (tableContainer, data, cols) => {
    if (debug) console.log(`Data received -> Data: ${JSON.stringify(data)}`);
    // making the columns
    const htmlCols = cols.map(col => `<th>${col}</th>`).join('');
    const htmlHeader = `<tr>${htmlCols}</tr>`;
    // making the rows
    const htmlRows = data.map(row => {
        const rowData = cols.map(col => `<td>${row[col]}</td>`).join('');
        return `<tr>${rowData}</tr>`;
    }).join('');
    // inserting the HTML
    tableContainer.innerHTML = `
        <table>
            <thead>${htmlHeader}</thead>
            <tbody>${htmlRows}</tbody>
        </table>
    `;
};

/**
 * combines loadTableData() and renderTable()
 * 
 * @param {Element} tableContainer
 * @param {Number} offset
 * @param {string} lookedName
 * @param {Array} cols
 */
const createTable = async (tableContainer, offset, lookedName, cols) => {
    const tableData = await loadTableData(tableContainer, offset, lookedName);
    renderTable(tableContainer, tableData, cols)
}

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
        const searcher = table.parentElement.querySelector('.searcher');
        if (debug) console.log(searcher.outerHTML);
        const tableModel = table.dataset.tablemodel;
        const cols = configData.models[tableModel].cols_displayed;
        console.log(`Columns finded -> Columns: ${cols} | Function: ${initTables.name}`);
        // creates the table for the first time
        createTable(table, 0, "", cols);
        tableSearcher(searcher, (lookedName) => {
            createTable(table, 0, lookedName, cols);
        });
    });
};