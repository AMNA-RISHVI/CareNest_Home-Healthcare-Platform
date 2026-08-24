document.addEventListener("DOMContentLoaded", function () {

    const patientItems =
        document.querySelectorAll(".patient-item");

    const featureItems =
        document.querySelectorAll(".feature-item");

    const contentPanels =
        document.querySelectorAll(".content-panel");


    let selectedPatient = null;

    let selectedFeature = "overview";


    /*
    =====================================================
    SELECT FIRST PATIENT
    =====================================================
    */

    if (patientItems.length > 0) {

        selectedPatient = patientItems[0];

        patientItems[0].classList.add("selected");

    }


    /*
    =====================================================
    PATIENT SELECTION
    =====================================================
    */

    patientItems.forEach(function (patient) {

        patient.addEventListener("click", function () {

            /*
            Remove selected state
            */

            patientItems.forEach(function (item) {

                item.classList.remove("selected");

            });


            /*
            Select clicked patient
            */

            patient.classList.add("selected");

            selectedPatient = patient;


            /*
            Refresh current feature
            */

            updateDashboard();

        });

    });


    /*
    =====================================================
    FEATURE SELECTION
    =====================================================
    */

    featureItems.forEach(function (feature) {

        feature.addEventListener("click", function () {

            /*
            Remove active state
            */

            featureItems.forEach(function (item) {

                item.classList.remove("active");

            });


            /*
            Activate clicked feature
            */

            feature.classList.add("active");


            selectedFeature =
                feature.dataset.feature;


            updateDashboard();

        });

    });


    /*
    =====================================================
    UPDATE DASHBOARD
    =====================================================
    */

    function updateDashboard() {

        /*
        Hide all panels
        */

        contentPanels.forEach(function (panel) {

            panel.classList.remove("active");

        });


        /*
        Family Members is a static feature
        */

        if (selectedFeature === "family") {

            const familyPanel =
                document.getElementById(
                    "family-panel"
                );

            if (familyPanel) {

                familyPanel.classList.add("active");

            }

            return;
        }


        /*
        Overview
        */

        if (selectedFeature === "overview") {

            const overviewPanel =
                document.getElementById(
                    "overview-panel"
                );

            if (overviewPanel) {

                overviewPanel.classList.add("active");

            }

            updateSelectedPatientInformation();

            return;
        }


        /*
        Appointments
        */

        if (selectedFeature === "appointments") {

            const appointmentPanel =
                document.getElementById(
                    "appointments-panel"
                );

            if (appointmentPanel) {

                appointmentPanel.classList.add("active");

            }

            return;
        }


        /*
        Health Records
        */

        if (selectedFeature === "records") {

            const recordsPanel =
                document.getElementById(
                    "records-panel"
                );

            if (recordsPanel) {

                recordsPanel.classList.add("active");

            }

            return;
        }


        /*
        Notifications
        */

        if (selectedFeature === "notifications") {

            const notificationPanel =
                document.getElementById(
                    "notifications-panel"
                );

            if (notificationPanel) {

                notificationPanel.classList.add("active");

            }

        }

    }


    /*
    =====================================================
    UPDATE SELECTED PATIENT INFORMATION
    =====================================================
    */

    function updateSelectedPatientInformation() {

        if (!selectedPatient) {

            return;

        }


        const bloodGroup =
            selectedPatient.dataset.patientBloodGroup;


        const dob =
            selectedPatient.dataset.patientDob;


        const gender =
            selectedPatient.dataset.patientGender;


        const bloodGroupElement =
            document.getElementById(
                "overview-blood-group"
            );


        const dobElement =
            document.getElementById(
                "overview-dob"
            );


        const genderElement =
            document.getElementById(
                "overview-gender"
            );


        if (bloodGroupElement) {

            bloodGroupElement.textContent =
                bloodGroup || "—";

        }


        if (dobElement) {

            dobElement.textContent =
                dob || "—";

        }


        if (genderElement) {

            genderElement.textContent =
                gender || "—";

        }

    }


    /*
    =====================================================
    INITIAL DASHBOARD
    =====================================================
    */

    updateDashboard();

});