let activeIndex = 0;
function moveSlide(step) {
    const items = document.querySelectorAll('#coct-item');
    const totalItems = items.length;

    if (items[activeIndex]) {
        items[activeIndex].classList.remove('active');
    }

    activeIndex += step;
    if (activeIndex >= totalItems) {
        activeIndex = 0;
    } else if (activeIndex < 0) {
        activeIndex = totalItems - 1;
    }

    if (items[activeIndex]) {
        items[activeIndex].classList.add('active');
    }

    const container = document.querySelector('.container-coct-list');
    const activeElem = items[activeIndex];

    if (activeElem && container) {
        container.scrollLeft = activeElem.offsetLeft - container.offsetWidth / 2 + activeElem.offsetWidth / 2;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const firstItem = document.querySelectorAll('#coct-item')[0];
    if (firstItem) {
        firstItem.classList.add('active');
        moveSlide(0); // Центрируем первый элемент, если он существует
    }

});

/////////////////////////////// Форматирование ингредиентов
const ingredientsDiv = document.getElementById('ingredients');
if (ingredientsDiv) {
    ingredientsDiv.innerHTML = ingredientsDiv.innerHTML.replace(/мл/g, 'мл<br>');
}

//////////////////////////////// Прокрутка элемента
window.addEventListener('scroll', function() {
    var scrollValue = window.scrollY;
    var element = document.querySelector('.img2-gal-3');


    element.style.transform = 'translateY(' + (scrollValue * 0.1) + 'px)';
});

///////////////////////////////////

function showReplyForm(commentId) {
    var formId = "reply-form-" + commentId;
    var form = document.getElementById(formId);
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}
