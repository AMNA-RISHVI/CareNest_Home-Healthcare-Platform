document.addEventListener("DOMContentLoaded", function () {

    const timelineCards = document.querySelectorAll(
        ".timeline-card"
    );


    timelineCards.forEach(function (card) {

        card.addEventListener("click", function () {

            card.classList.toggle(
                "timeline-card-expanded"
            );

        });

    });

});