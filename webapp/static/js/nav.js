/**
 * disables all buttons and selects the clicked one
 * @param {Element} clickedBtn 
 * @param {NodeList} allBtns 
 */
export const changeSection = (clickedBtn, allBtns) => {
  allBtns.forEach(btn => btn.classList.remove('active'));
  
  clickedBtn.classList.add('active');
  console.log(`Selected section: ${clickedBtn.textContent}`)
};

/**
 * Receives:
 * - a section object
 * - An ID
 * And hides all the nodes, excepting for the introduced ID
 * @param {Object} sections 
 * @param {string} name 
 */
export const showSection = (sections, name) => {
    console.log("Object received -> ", sections);
    const newIndex = sections[name].index;

    Object.values(sections).forEach(({ index, element }) => {
        console.log("Removing the classes for the following element -> ", element)
        element.classList.remove('active', 'left');
        if (index < newIndex) element.classList.add('left');
    });

    sections[name].element.classList.add('active');
};

/**
 * Receives:
 */