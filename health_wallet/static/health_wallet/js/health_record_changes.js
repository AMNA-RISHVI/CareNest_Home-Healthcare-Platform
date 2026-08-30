document.addEventListener("DOMContentLoaded", function () {

    const filterForm = document.querySelector(
        ".filter-card form"
    );

    if (!filterForm) {
        return;
    }

    const selects = filterForm.querySelectorAll(
        "select"
    );

    selects.forEach(function (select) {

        select.addEventListener(
            "change",
            function () {

                // Automatically submit when
                // the user changes a filter.

                filterForm.submit();

            }
        );

    });

});