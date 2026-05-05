const receiveMenuData = async (endpoint, name) => {
    const response = await fetch(endpoint);
    const data = await response.json();
    return data;

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