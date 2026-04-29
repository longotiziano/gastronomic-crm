import { API_URL } from "./config.js"; 
import { obtainRId } from "./utils.js";

export const loadProducts = async (offset = 0, term = "") => {
    const rId = obtainRId();
    const res = await fetch(`${API_URL}/sales/show_products?offset=${offset}&looked_name=${term}&restaurant=${rId}`);
    const data = await res.json();
    const productsData = data.data.products;
    console.log(`show_products request done -> Status code: ${res.status} | data: ${Object.entries(data.data.products)}`);
    Object.entries(productsData).forEach(([key, value]) => {
    console.log(key, value);
    });
    renderTable(data.data.products);
    renderPagination(data.prev_offset, data.next_offset);
};

const renderTable = (sales) => {
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

const renderPagination = (prev, next) => {
    // botones de prev/next con los offsets
};