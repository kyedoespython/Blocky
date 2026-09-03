document.addEventListener("DOMContentLoaded", function () {

    const portal = document.querySelector(".portal");
    const number = document.querySelector(".slide-number");
    const title = document.querySelector(".portal-content h2");
    const description = document.querySelector(".portal-content p");

    const slides = [
        {
            title: "Build",
            description: "Create your database structure quickly and keep everything organised."
        },
        {
            title: "Connect",
            description: "Connect your project to the tools and services you already use."
        },
        {
            title: "Scale",
            description: "Start simple and build a foundation that can grow with your project."
        }
    ];

    let current = 0;
    let locked = false;

    function changeSlide(direction) {

        if (locked) {
            return;
        }

        const next = current + direction;

        if (next < 0 || next >= slides.length) {
            return;
        }

        locked = true;

        portal.style.opacity = "0";
        portal.style.transform =
            "translate(-50%, -50%) scale(0.85)";

        setTimeout(function () {

            current = next;

            title.textContent = slides[current].title;
            description.textContent = slides[current].description;

            number.textContent =
                "0" + (current + 1) + " / 03";

            portal.style.transform =
                "translate(-50%, -50%) scale(1)";

            portal.style.opacity = "1";

        }, 300);

        setTimeout(function () {
            locked = false;
        }, 850);
    }

    window.addEventListener("wheel", function (event) {

        if (event.deltaY > 0) {
            changeSlide(1);
        }

        if (event.deltaY < 0) {
            changeSlide(-1);
        }

    });

});