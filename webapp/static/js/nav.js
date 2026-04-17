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
 * Looks for every div with ".menu" class and allows expanding and collapsing the menu
 */
export const initDisplayMenus = () => {
    const menus = document.querySelectorAll(".menu");
    menus.forEach(menu => {
        const btn = menu.querySelector(":scope > button");
        const desplegable = menu.querySelector(":scope > div");
        btn.addEventListener("click", () => desplegable.classList.toggle("active"));
        })
    };