const block = document.querySelector(".drag-block");

let isDragging = false;

let offsetX = 0;
let offsetY = 0;

block.addEventListener("mousedown", function (event) {

    isDragging = true;

    const rect = block.getBoundingClientRect();

    offsetX = event.clientX - rect.left;
    offsetY = event.clientY - rect.top;

    block.style.transform = "none";

    block.style.cursor = "grabbing";

});

document.addEventListener("mousemove", function (event) {

    if (!isDragging) {
        return;
    }

    block.style.left = (event.clientX - offsetX) + "px";
    block.style.top = (event.clientY - offsetY) + "px";

});

document.addEventListener("mouseup", function () {

    isDragging = false;

    block.style.cursor = "grab";

});
