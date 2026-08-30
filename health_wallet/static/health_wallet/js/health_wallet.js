/* =========================================================
   CARENEST
   HEALTH WALLET - ALL RECORDS JAVASCRIPT
========================================================= */


document.addEventListener(
    "DOMContentLoaded",
    function () {


        /* =================================================
           ADD RECORD MODAL
        ================================================== */

        const addRecordModal =
            document.getElementById(
                "addRecordModal"
            );


        const openAddRecordMenu =
            document.getElementById(
                "openAddRecordMenu"
            );


        const closeAddRecordMenu =
            document.getElementById(
                "closeAddRecordMenu"
            );


        if (openAddRecordMenu) {

            openAddRecordMenu.addEventListener(
                "click",
                function () {

                    addRecordModal.classList.add(
                        "show"
                    );

                    document.body.style.overflow =
                        "hidden";

                }
            );

        }


        if (closeAddRecordMenu) {

            closeAddRecordMenu.addEventListener(
                "click",
                function () {

                    closeModal(
                        addRecordModal
                    );

                }
            );

        }


        /* =================================================
           DELETE MODAL
        ================================================== */

        const deleteModal =
            document.getElementById(
                "deleteModal"
            );


        const closeDeleteModal =
            document.getElementById(
                "closeDeleteModal"
            );


        const cancelDelete =
            document.getElementById(
                "cancelDelete"
            );


        const deleteRecordForm =
            document.getElementById(
                "deleteRecordForm"
            );


        const deleteRecordName =
            document.getElementById(
                "deleteRecordName"
            );


        const deleteButtons =
            document.querySelectorAll(
                ".delete-record-button"
            );


        /* =================================================
           OPEN DELETE MODAL
        ================================================== */

        deleteButtons.forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        const deleteUrl =
                            button.dataset.deleteUrl;


                        const recordName =
                            button.dataset.recordName;


                        if (!deleteUrl) {

                            console.error(
                                "Delete URL is missing."
                            );

                            return;

                        }


                        deleteRecordForm.action =
                            deleteUrl;


                        if (recordName) {

                            deleteRecordName.textContent =
                                '"' +
                                recordName +
                                '"';

                        }


                        deleteModal.classList.add(
                            "show"
                        );


                        document.body.style.overflow =
                            "hidden";

                    }
                );

            }
        );


        /* =================================================
           CLOSE DELETE MODAL
        ================================================== */

        if (closeDeleteModal) {

            closeDeleteModal.addEventListener(
                "click",
                function () {

                    closeModal(
                        deleteModal
                    );

                }
            );

        }


        if (cancelDelete) {

            cancelDelete.addEventListener(
                "click",
                function () {

                    closeModal(
                        deleteModal
                    );

                }
            );

        }


        /* =================================================
           CLOSE MODALS WHEN CLICKING OUTSIDE
        ================================================== */

        document.querySelectorAll(
            ".modal-overlay"
        ).forEach(
            function (overlay) {

                overlay.addEventListener(
                    "click",
                    function (event) {

                        if (
                            event.target ===
                            overlay
                        ) {

                            closeModal(
                                overlay
                            );

                        }

                    }
                );

            }
        );


        /* =================================================
           ESC KEY
        ================================================== */

        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Escape"
                ) {

                    document.querySelectorAll(
                        ".modal-overlay.show"
                    ).forEach(
                        function (modal) {

                            closeModal(
                                modal
                            );

                        }
                    );

                }

            }
        );


        /* =================================================
           FILTER BUTTON LOADING STATE
        ================================================== */

        document.querySelectorAll(
            ".filter-button"
        ).forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        button.classList.add(
                            "loading"
                        );

                    }
                );

            }
        );


        /* =================================================
           FILE LINKS
        ================================================== */

        document.querySelectorAll(
            ".file-link"
        ).forEach(
            function (link) {

                link.addEventListener(
                    "click",
                    function () {

                        link.classList.add(
                            "opening"
                        );

                    }
                );

            }
        );


        /* =================================================
           HELPER
        ================================================== */

        function closeModal(
            modal
        ) {

            if (!modal) {

                return;

            }


            modal.classList.remove(
                "show"
            );


            /*
                Only restore page scrolling
                if no other modal is open.
            */

            const activeModal =
                document.querySelector(
                    ".modal-overlay.show"
                );


            if (!activeModal) {

                document.body.style.overflow =
                    "";

            }

        }


    }
);