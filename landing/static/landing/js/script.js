console.log("CARENEST SCRIPT LOADED");

document.addEventListener("DOMContentLoaded", function () {

    console.log("DOM LOADED");

    const exploreButton = document.getElementById("exploreDropdown");
    const exploreMenu = document.getElementById("exploreMenu");

    console.log("Explore button:", exploreButton);
    console.log("Explore menu:", exploreMenu);

    if (!exploreButton) {
        console.error("EXPLORE BUTTON NOT FOUND");
        return;
    }

    if (!exploreMenu) {
        console.error("EXPLORE MENU NOT FOUND");
        return;
    }

    exploreButton.addEventListener("click", function (event) {

        event.preventDefault();

        console.log("EXPLORE CLICKED");

        exploreMenu.classList.toggle("show");

        console.log(
            "Menu classes:",
            exploreMenu.className
        );

    });

});