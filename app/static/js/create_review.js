// -----------------------------------------------
// STAR RATING — left-to-right fill via JS
// -----------------------------------------------
const starLabels = document.querySelectorAll('.star-label');
const starInputs = document.querySelectorAll('.star-input');

function setStarFill(upTo) {
    starLabels.forEach((label, idx) => {
        label.classList.toggle('filled', idx < upTo);
    });
}

// Restore checked state on page load
let checkedVal = 0;
starInputs.forEach((input, idx) => {
    if (input.checked) checkedVal = idx + 1;
});
setStarFill(checkedVal);

starLabels.forEach((label, idx) => {
    label.addEventListener('mouseenter', () => setStarFill(idx + 1));
    label.addEventListener('click', () => {
        checkedVal = idx + 1;
        starInputs[idx].checked = true;
    });
});

document.getElementById('rating-group').addEventListener('mouseleave', () => {
    setStarFill(checkedVal);
});

// -----------------------------------------------
// HOURGLASS WORKLOAD PICKER
// -----------------------------------------------
const hourglassBtns = document.querySelectorAll('.hourglass-btn');
const workloadInput = document.getElementById('workload');

hourglassBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        hourglassBtns.forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        workloadInput.value = btn.dataset.value;
        document.getElementById('workload-error').style.display = 'none';
    });
});

// Guard against submitting without a workload selection
document.querySelector('form').addEventListener('submit', function(e) {
    if (!workloadInput.value) {
        e.preventDefault();
        document.getElementById('workload-error').style.display = 'block';
        document.querySelector('.hourglass-picker').scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});