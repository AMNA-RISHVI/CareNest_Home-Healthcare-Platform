document.addEventListener("DOMContentLoaded", function () {

    const messages =
        document.querySelectorAll(".alert-message");


    messages.forEach(function (message) {

        setTimeout(function () {

            message.style.transition =
                "opacity 0.4s ease, transform 0.4s ease";

            message.style.opacity = "0";

            message.style.transform =
                "translateX(40px)";


            setTimeout(function () {

                message.remove();

            }, 400);

        }, 4000);

    });

});