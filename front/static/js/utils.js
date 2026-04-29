import { API_URL, DEFAULT_RESTAURANT } from "./config.js";

/**
 * Receives:
 * - a NodeList
 * Returns:
 * - an object with IDs as keys, and another object with the index and element
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