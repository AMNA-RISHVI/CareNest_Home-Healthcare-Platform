console.log("CARENEST SCRIPT LOADED");


document.addEventListener("DOMContentLoaded", function () {

    console.log("DOM LOADED");


    const homeButton =
        document.getElementById("homeDropdownButton");

    const homeMenu =
        document.getElementById("homeDropdownMenu");


    console.log("Home button:", homeButton);
    console.log("Home menu:", homeMenu);


    /*
    |--------------------------------------------------------------------------
    | CHECK ELEMENTS
    |--------------------------------------------------------------------------
    */

    if (!homeButton || !homeMenu) {

        console.error(
            "CareNest: Home dropdown elements NOT FOUND."
        );

        return;
    }


    /*
    |--------------------------------------------------------------------------
    | OPEN / CLOSE HOME DROPDOWN
    |--------------------------------------------------------------------------
    */

    homeButton.addEventListener("click", function (event) {

        console.log("HOME BUTTON CLICKED");

        event.preventDefault();
        event.stopPropagation();


        homeMenu.classList.toggle("show");

        homeButton.classList.toggle("active");


        console.log(
            "Dropdown open:",
            homeMenu.classList.contains("show")
        );

    });


    /*
    |--------------------------------------------------------------------------
    | CLOSE WHEN CLICKING OUTSIDE
    |--------------------------------------------------------------------------
    */

    document.addEventListener("click", function (event) {

        if (
            !homeButton.contains(event.target) &&
            !homeMenu.contains(event.target)
        ) {

            homeMenu.classList.remove("show");

            homeButton.classList.remove("active");

        }

    });


    /*
    |--------------------------------------------------------------------------
    | CLOSE AFTER SELECTING A LINK
    |--------------------------------------------------------------------------
    */

    const links =
        homeMenu.querySelectorAll("a");


    links.forEach(function (link) {

        link.addEventListener("click", function () {

            homeMenu.classList.remove("show");

            homeButton.classList.remove("active");

        });

    });

});