document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    if (!form) {
        return;
    }

    form.addEventListener("submit", function (event) {

        const confirmed = confirm(
            "Are you sure you want to permanently delete this health record?"
        );

        if (!confirmed) {

            event.preventDefault();

            return;

        }

        const button = form.querySelector(
            'button[type="submit"]'
        );

        if (button) {

            button.disabled = true;

            button.innerHTML = "Deleting...";

        }

    });

});