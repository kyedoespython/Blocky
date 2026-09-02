const block = document.querySelector('.drag-block');
let isDragging = false;
let offsetX = 0;
let offsetY = 0;

block.addEventListener('mousedown', e => {
    isDragging = true;
    offsetX = e.clientX - block.offsetLeft;
    offsetY = e.clientY - block.offsetTop;
    block.style.cursor = 'grabbing';
});

document.addEventListener('mousemove', e => {
    if (!isDragging) return;
    block.style.left = (e.clientX - offsetX) + 'px';
    block.style.top = (e.clientY - offsetY) + 'px';
});

document.addEventListener('mouseup', () => {
    isDragging = false;
    block.style.cursor = 'grab';
});
