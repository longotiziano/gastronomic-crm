import configData from '../../../../config.json' with { type: 'json' };
import { obtainRId } from "../utils.js";
import { tableSearcher } from "../btns/searcher.js";

const API_URL = configData.api_url;

/**
 * received the table's container, the offset and the looked name, returns it's endpoint' data
 * 
 * @param {Element} tableContainer
 * @param {Number} offset
 * @param {string} lookedName
 * @returns {Object}
 */
const loadTableData = (tableContainer, offset, lookedName) => {
    const rId = obtainRId();
    const endpoint = `${API_URL}${tableContainer.endpoint}`;
    const res = await fetch(`${endpoint}?offset=${offset}&looked_name=${lookedName}&restaurant=${rId}`);
    const data = await res.json();
    return data;
}

/**
 * received the table's container, it's data and it's columns, creates the HTML of the table
 * 
 * @param {Element} tableContainer
 * @param {Object} data
 * @param {Array} cols
 */
const renderTable = (tableContainer, data, cols) => {
    const rows = sales.map(sale => `
        <tr>
            <td>${sale.product_name}</td>
            <td>${sale.product_category}</td>
            <td>${sale.price}</td>
        </tr>
    `).join('');

    document.getElementById('container').innerHTML = `
        <table>
            <thead><tr><th>Nombre</th><th>Categoria</th><th>Precio</th></tr></thead>
            <tbody>${rows}</tbody>
        </table>
    `;
};

/**
 * combines loadTableData() and renderTable()
 */
const createTable = (tableContainer, offset, lookedName, cols) => {
    const tableData = loadTableData(tableContainer, offset, lookedName);
    renderTable(tableContainer, tableDat, cols)
}

/**
 * 
 * 
 * @returns {string}
 */
const renderPagination = (prev, next) => {
    // botones de prev/next con los offsets
};

const initTables = () => {
    const tables = document.querySelectorAll('tables');
    tables.forEach(table => function() {
        const searcher = table.parentElement.querySelector('searcher');
        const cols = configData.models.dataset.tablemodel.cols_displayed;
        // creates the table for the first time
        createTable(tableContainer, 0, "", cols);
        tableSearcher(searcher, (lookedName) => {
            createTable(tableContainer, 0, lookedName, cols);
        });
    });
};