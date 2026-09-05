

document.addEventListener("DOMContentLoaded", function () {

    const dateGrid = document.getElementById("dateGrid");
    const timeGrid = document.getElementById("timeGrid");

    const selectedDateInput =
        document.getElementById("selected_date");

    const selectedTimeInput =
        document.getElementById("selected_time");


    // ==========================================
    // CREATE AVAILABLE DATES
    // ==========================================

    function generateDates() {

        dateGrid.innerHTML = "";

        const today = new Date();

        // Show next 30 days
        for (let i = 0; i < 30; i++) {

            const date = new Date(today);

            date.setDate(today.getDate() + i);


            // JavaScript:
            // Sunday = 0
            // Monday = 1
            // Tuesday = 2
            // ...
            // Saturday = 6

            const javascriptDay = date.getDay();


            // Convert JavaScript day
            // to Django day

            const djangoDay =
                javascriptDay === 0
                    ? 6
                    : javascriptDay - 1;


            // Check professional availability
            const isAvailable =
                availabilityData.some(
                    availability =>
                        availability.day === djangoDay
                );


            // Professional does not work
            // on this day
            if (!isAvailable) {
                continue;
            }


            // Create date button
            const button =
                document.createElement("button");

            button.type = "button";
            button.className = "date-btn";


            const dayName =
                date.toLocaleDateString(
                    "en-US",
                    { weekday: "short" }
                );


            const monthName =
                date.toLocaleDateString(
                    "en-US",
                    { month: "short" }
                );


            const dateNumber =
                date.getDate();


            button.innerHTML = `
                <span class="day-name">
                    ${dayName}
                </span>

                <span class="date-number">
                    ${dateNumber}
                </span>

                <span class="month-name">
                    ${monthName}
                </span>
            `;


            // Create YYYY-MM-DD
            const formattedDate =
                date.getFullYear() +
                "-" +
                String(
                    date.getMonth() + 1
                ).padStart(2, "0") +
                "-" +
                String(
                    date.getDate()
                ).padStart(2, "0");


            button.dataset.date =
                formattedDate;


            // When date is clicked
            button.addEventListener(
                "click",
                function () {

                    // Remove old selection
                    document
                        .querySelectorAll(".date-btn")
                        .forEach(btn => {
                            btn.classList.remove("active");
                        });


                    // Select this date
                    this.classList.add("active");


                    // Save selected date
                    selectedDateInput.value =
                        this.dataset.date;


                    // Generate times
                    generateTimes(
                        this.dataset.date
                    );
                }
            );


            dateGrid.appendChild(button);
        }


        // No dates
        if (dateGrid.children.length === 0) {

            dateGrid.innerHTML = `
                <div class="no-times">
                    No available dates
                </div>
            `;
        }
    }


    // ==========================================
    // CREATE AVAILABLE TIMES
    // ==========================================

    function generateTimes(dateString) {

        timeGrid.innerHTML = "";

        selectedTimeInput.value = "";


        const date =
            new Date(
                dateString + "T00:00:00"
            );


        const javascriptDay =
            date.getDay();


        const djangoDay =
            javascriptDay === 0
                ? 6
                : javascriptDay - 1;


        // Find availability for selected day
        const matchingAvailability =
            availabilityData.filter(
                availability =>
                    availability.day === djangoDay
            );


        // No availability
        if (matchingAvailability.length === 0) {

            timeGrid.innerHTML = `
                <div class="no-times">
                    No available times
                </div>
            `;

            return;
        }


        // Create time slots
        matchingAvailability.forEach(
            availability => {

                let startMinutes =
                    timeToMinutes(
                        availability.start
                    );


                const endMinutes =
                    timeToMinutes(
                        availability.end
                    );


                while (
                    startMinutes < endMinutes
                ) {

                    const time =
                        minutesToTime(
                            startMinutes
                        );


                    const button =
                        document.createElement("button");


                    button.type = "button";

                    button.className =
                        "time-btn";

                    button.textContent =
                        time;

                    button.dataset.time =
                        time;


                    // Time click
                    button.addEventListener(
                        "click",
                        function () {

                            document
                                .querySelectorAll(
                                    ".time-btn"
                                )
                                .forEach(btn => {
                                    btn.classList.remove(
                                        "active"
                                    );
                                });


                            this.classList.add(
                                "active"
                            );


                            selectedTimeInput.value =
                                this.dataset.time;
                        }
                    );


                    timeGrid.appendChild(button);


                    // Use professional's slot
                    startMinutes +=
                        availability.slot;
                }
            }
        );
    }


    // ==========================================
    // TIME → MINUTES
    // ==========================================

    function timeToMinutes(time) {

        const parts =
            time.split(":");

        const hours =
            Number(parts[0]);

        const minutes =
            Number(parts[1]);

        return (
            hours * 60 +
            minutes
        );
    }


    // ==========================================
    // MINUTES → TIME
    // ==========================================

    function minutesToTime(minutes) {

        const hours =
            Math.floor(minutes / 60);

        const mins =
            minutes % 60;


        return (
            String(hours).padStart(2, "0") +
            ":" +
            String(mins).padStart(2, "0")
        );
    }


    // ==========================================
    // START
    // ==========================================

    generateDates();

});