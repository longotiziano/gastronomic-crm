import configData from '../../../config/config.json' with { type: 'json' };
const DEFAULT_RESTAURANT = configData.default_values.default_restaurant;
const API_URL = configData.api_url;
const debug = configData.debug_mode;

/**
 * Receives:
 * - a NodeList
 * Returns:
 * - an object with IDs as keys, and another object with the index and element
 * 
 * @param {NodeList}
 * @returns {Object}
 */
export const createIndexObject = (elements) => {
    const indexObject = {};
    elements.forEach((elem, i) => {
        indexObject[elem.id] = { index: i, element: elem };
    });
    return indexObject;
}

/**
 * Returns the rId selected in the URL. If there isn't a value, provides the default one.
 * @returns {Number}
 */
export const obtainRId = () => {
    const rId = new URLSearchParams(window.location.search).get('restaurant') ?? DEFAULT_RESTAURANT;
    return rId;
}

/**
 * async function to fetch data from the API. It throws an error if the response is not ok, and returns the JSON response if it is.
 * 
 * @param {String} endpoint - the API endpoint to fetch from
 * @param {Object} options - the options to pass to the fetch function 
 * @returns {Promise} - a promise that resolves to the JSON response from the API
 * @throws {Error} - if the response from the API is not ok, it throws an error with the message from the API or a default message with the status code
 */
export const apiFetch = async (endpoint, options = {}) => {
    const url = `${API_URL}${endpoint}`;
    const { body, ...restOptions } = options;

    const isFormData = body instanceof FormData;
    if (debug && isFormData) {
        console.log(`FormData: ${isFormData} | Content:`);
        for (let [key, value] of body.entries()) {
            console.log(`Key: ${key} | Value: ${value}`);
        }
    }

    const res = await fetch(url, {
        headers: isFormData ? {} : { "Content-Type": "application/json" },
        ...restOptions,
        body: isFormData ? body : body ? JSON.stringify(body) : undefined
    });

    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.message || `Error ${res.status}`);
    }

    return res.json();
}

/**
 * received a container, the offset and the looked name, returns it's endpoint' data
 * 
 * @param {Element} container 
 * @param {Number} offset (optional) if the endpoint supports pagination, the offset will be added as a param to the endpoint
 * @param {string} lookedName (optional) if the searcher is used, the looked name will be added as a param to the endpoint
 * @param {boolean} requiresRId (optional) if the endpoint requires the restaurant id as a param, it will be added automatically
 * @param {Function} renderCallback (optional) a function to call with the container and loaded data
 * @returns {Array}
 */
export const loadTableData = async (container, offset = 0, lookedName = "", requiresRId = false, renderCallback = null) => {
    const params = new URLSearchParams();
    if (requiresRId) params.append('r_id', obtainRId());
    if (offset) params.append('offset', offset);
    if (lookedName) params.append('looked_name', lookedName);

    const endpoint = container.dataset.endpoint;
    const tableModel = container.dataset.tablemodel;
    
    const queryString = params.toString()
    const endpointParams = queryString ? `${endpoint}?${queryString}` : endpoint
    if (debug) console.log(`Endpoint with params -> Endpoint: ${endpointParams} | Function: ${loadTableData.name}`);
    const data = await apiFetch(endpointParams);
    
    const dataArray = data.data[tableModel];
    if (debug) dataArray.map(obj => console.log(obj));
    if (renderCallback) renderCallback(container, dataArray);
    return dataArray;
}