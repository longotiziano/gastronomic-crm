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