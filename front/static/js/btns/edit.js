import configData from '../../../../config/config.json' with { type: 'json' };
const debug = configData.debug_mode;

export const initEditBtns = (container) => {
    const editBtns = container.querySelectorAll('.edit-btn');
    if (debug) console.log(`Initializing edit buttons -> Buttons: ${editBtns.length} | Function: ${initEditBtns.name}`);
    editBtns.forEach(btn => {
        if (debug) console.log('Initializing edit button:', btn.outerHTML);
        btn.innerHTML = '<svg data-lucide="pencil"></svg>';
    });
    lucide.createIcons();
};