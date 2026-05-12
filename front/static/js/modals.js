export function initModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        const openBtn = document.getElementById(modal.dataset.openby);
        const closeBtn = modal.querySelector('.x-btn');
        const cancelBtn = modal.querySelector('.btn-cancel');
        const submitBtn = modal.querySelector('.btn-submit');
        const modalOverlay = modal.parentElement;
        if (openBtn) {
            openBtn.addEventListener('click', () => {
                modalOverlay.classList.add('active');
            });
        }
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modalOverlay.classList.remove('active');
            });
        }
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                modalOverlay.classList.remove('active');
            });
        }
        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                modalOverlay.classList.remove('active');
            });
        }
        if (modalOverlay) {
            modalOverlay.addEventListener('click', (e) => {
                if (e.target === modalOverlay) {
                    modalOverlay.classList.remove('active');
                }
        });
    }
    });
}