/**
 * disables all buttons and selects the clicked one 
 * 
 * 
 * @param {Element} clickedBtn 
 * @param {NodeList} allBtns 
 */
export const selectOption = (clickedBtn, allBtns) => {
    allBtns.forEach(btn => {btn.classList.remove('active')});
    clickedBtn.classList.add('active');
    console.log(`Selected button: ${clickedBtn.textContent}`)
};

/**
 * applies the selectOption function for the childrens' buttons of every ".selectables" class
 *
 * Also, looks for the selectable's data and displays it in the URL, putting just the clicked button's data
 */
export const initSelectables = () => {
    const selectables = document.querySelectorAll(".selectables");
    selectables.forEach(container => {
        const dataParam = container.dataset.name;
        console.log(`Obtained container's data name: ${dataParam}`)
        const btns = container.querySelectorAll("button")
        btns.forEach(btn => {
            btn.addEventListener("click", () => {
                selectOption(btn, btns);
                const url = new URL(window.location.href);
                const btnData = btn.dataset[dataParam];
                console.log(`Displaying selectable's value: ${btnData}`);
                url.searchParams.set(dataParam, btnData);
                window.history.pushState({}, '', url.toString());   
            })
        })
    })
};