/**
 * disables all buttons and selects the clicked one 
 * @param {Element} clickedBtn 
 * @param {NodeList} allBtns 
 */
export const selectOption = (clickedBtn, allBtns) => {
  allBtns.forEach(btn => btn.classList.remove('active'));
  clickedBtn.classList.add('active');
  console.log(`Selected button: ${clickedBtn.textContent}`)
};

/**
 * applies the selectOption function for the childrens' buttons of every ".selectables" class
 */
export const initSelectables = () => {
    const selectables = document.querySelectorAll(".selectables");
    selectables.forEach(container => {
        const btns = container.querySelectorAll("button")
        btns.forEach(btn => {
            btn.addEventListener("click", () => selectOption(btn, btns))
        })
    })
};