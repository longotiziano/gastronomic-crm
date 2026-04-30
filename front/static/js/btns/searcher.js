const DEBOUNCE_TIMER = 300;

/**
 * Receives an input, and executes the callback with the text inserted for every DEBOUNCE_TIMER mils
 * 
 * @param {Element} input
 * @param {Function} callback
 */
export const tableSearcher = (input, callback) => {
    let debounceTimer;
    input.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            callback(e.target.value);
        }, DEBOUNCE_TIMER);
    });
};