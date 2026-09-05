
  

        function closeWidget() {
            document.getElementById('ratingWidget').style.display = 'none';
        }

        document.getElementById('reviewForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const selectedRating = document.querySelector('input[name="rating"]:checked');
            const statusMsg = document.getElementById('statusMessage');

            if (!selectedRating) {
                statusMsg.className = 'status-msg alert alert-danger';
                statusMsg.innerText = 'Please select a star rating first!';
                statusMsg.style.display = 'block';
                return;
            }

            const ratingValue = selectedRating.value;

            statusMsg.className = 'status-msg alert alert-success';
            statusMsg.innerText = `Thank you! Rated ${ratingValue} Stars for professional`;
            statusMsg.style.display = 'block';

            setTimeout(() => {
                document.getElementById('reviewForm').reset();
                statusMsg.style.display = 'none';
            }, 3000);
        });
