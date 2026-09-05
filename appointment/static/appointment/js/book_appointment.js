document.addEventListener("DOMContentLoaded", function () {

    const dateGrid = document.getElementById("dateGrid");
    const timeGrid = document.getElementById("timeGrid");
    const selectedDateInput = document.getElementById("selected_date");
    const selectedTimeInput = document.getElementById("selected_time");

    
    // ==========================================
    // HELPER FUNCTIONS  !!!
    // ==========================================

    function timeToMinutes(timeStr) {
        const [hours, minutes] = timeStr.split(':').map(Number);
        return hours * 60 + minutes;
    }

    function minutesToTime(minutes) {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return String(hours).padStart(2, '0') + ':' + String(mins).padStart(2, '0');
    }

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

            const javascriptDay = date.getDay();
            const djangoDay = javascriptDay === 0 ? 6 : javascriptDay - 1;

            // Check professional availability
            const isAvailable = availabilityData.some(
                availability => availability.day === djangoDay
            );

            if (!isAvailable) {
                continue;
            }

            // Create date button
            const button = document.createElement("button");
            button.type = "button";
            button.className = "date-btn";

            const dayName = date.toLocaleDateString("en-US", { weekday: "short" });
            const monthName = date.toLocaleDateString("en-US", { month: "short" });
            const dateNumber = date.getDate();

            button.innerHTML = `
                <span class="day-name">${dayName}</span>
                <span class="date-number">${dateNumber}</span>
                <span class="month-name">${monthName}</span>
            `;

            const formattedDate = date.getFullYear() +
                "-" + String(date.getMonth() + 1).padStart(2, "0") +
                "-" + String(date.getDate()).padStart(2, "0");

            button.dataset.date = formattedDate;

            button.addEventListener("click", function () {
                document.querySelectorAll(".date-btn").forEach(btn => {
                    btn.classList.remove("active");
                });
                this.classList.add("active");
                selectedDateInput.value = this.dataset.date;
                generateTimes(this.dataset.date);
            });

            dateGrid.appendChild(button);
        }

        if (dateGrid.children.length === 0) {
            dateGrid.innerHTML = `
                <div class="no-times">No available dates</div>
            `;
        }

        // Auto-select first available date
        const firstDateBtn = dateGrid.querySelector('.date-btn');
        if (firstDateBtn) {
            firstDateBtn.click();
        }
    }

    // ==========================================
    // CREATE AVAILABLE TIMES
    // ==========================================

    function generateTimes(dateString) {

        timeGrid.innerHTML = "";
        selectedTimeInput.value = "";

        const date = new Date(dateString + "T00:00:00");
        const javascriptDay = date.getDay();
        const djangoDay = javascriptDay === 0 ? 6 : javascriptDay - 1;

        const matchingAvailability = availabilityData.filter(
            availability => availability.day === djangoDay
        );

        if (matchingAvailability.length === 0) {
            timeGrid.innerHTML = `
                <div class="no-times">No available times</div>
            `;
            return;
        }

        matchingAvailability.forEach(availability => {

            let startMinutes = timeToMinutes(availability.start);
            const endMinutes = timeToMinutes(availability.end);
            const slotDuration = availability.slot || 30;

            while (startMinutes < endMinutes) {

                const time = minutesToTime(startMinutes);

                const button = document.createElement("button");
                button.type = "button";
                button.className = "time-btn";
                button.textContent = time;
                button.dataset.time = time;

                button.addEventListener("click", function (event) {
                    event.preventDefault();
                    timeGrid.querySelectorAll(".time-btn").forEach(btn => {
                        btn.classList.remove("active");
                    });
                    this.classList.add("active");
                    selectedTimeInput.value = this.dataset.time;
                    console.log("Selected time:", this.dataset.time);
                });

                timeGrid.appendChild(button);
                startMinutes += slotDuration;
            }
        });

        if (timeGrid.children.length === 0) {
            timeGrid.innerHTML = `
                <div class="no-times">No available times</div>
            `;
        }
    }

    // ==========================================
    // INITIALIZE
    // ==========================================

    if (typeof availabilityData !== 'undefined' && availabilityData.length > 0) {
        generateDates();
    } else {
        dateGrid.innerHTML = `
            <div class="no-times">No availability data found</div>
        `;
        console.warn("No availability data found");
    }

    // ==========================================
    // "Book for" 
    // ==========================================

    const bookForSelect = document.getElementById('book_for');
    const submitButton = document.querySelector('.btn-submit');

    if (bookForSelect && submitButton) {
        bookForSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const text = selectedOption.text;
            if (text && text !== 'Select Patient') {
                submitButton.textContent = `Book for ${text}`;
            } else {
                submitButton.textContent = 'Book Appointment';
            }
        });
    }

    // ==========================================
    // FORM VALIDATION
    // ==========================================

    if (submitButton) {
        submitButton.addEventListener('click', function(e) {
            const selectedDate = selectedDateInput.value;
            const selectedTime = selectedTimeInput.value;
            if (!selectedDate || !selectedTime) {
                e.preventDefault();
                alert('Please select both a date and time before booking.');
            }
        });
    }

});