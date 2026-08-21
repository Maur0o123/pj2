const inputs = document.querySelectorAll('input');
const selects = document.querySelectorAll('select');

inputs.forEach(ctrl => {
    ctrl.dataset.value = ctrl.value;
    ctrl.addEventListener('input', e => {
        if (ctrl.value != ctrl.dataset.value) {
            ctrl.classList.add('changed');
        } else {
            ctrl.classList.remove('changed');
        }
    });
});

selects.forEach(ctrl => {
    ctrl.dataset.value = ctrl.value;
    ctrl.addEventListener('change', e => {
        if (ctrl.value != ctrl.dataset.value) {
            ctrl.classList.add('changed');
        } else {
            ctrl.classList.remove('changed');
        }
    });
});

try {
    form.onsubmit = e => {
        window.onbeforeunload = null; 
    };
} catch (e) {
}