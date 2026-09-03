const filterButtons = document.querySelectorAll('.tab-btn');
const appointmentCards = document.querySelectorAll('.history-card');

filterButtons.forEach(button => {

    button.addEventListener('click', function () {

        // Remove active from all buttons
        filterButtons.forEach(btn => {
            btn.classList.remove('active');
        });

        // Add active to selected button
        this.classList.add('active');

        const filter = this.dataset.filter;

        appointmentCards.forEach(card => {

            const status = card.dataset.status;

            if (filter === 'all' || status === filter) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }

        });

    });

});