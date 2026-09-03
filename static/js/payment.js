const paymentForm = document.getElementById("payment-form");
const payButton = document.getElementById("pay-button");
const paymentResult = document.getElementById("payment-result");


paymentForm.addEventListener("submit", async function (event) {

    event.preventDefault();


    const paymentMethod =
        document.getElementById("payment-method").value;


    if (!paymentMethod) {

        showResult(
            "Please select a payment method.",
            "error"
        );

        return;
    }


    payButton.disabled = true;
    payButton.textContent = "Processing...";


    /*
        Temporary test values.

        Later these will come from the
        logged-in user and selected plan.
    */

    const userId = 1;
    const planId = 1;


    try {

        const response = await fetch(
            "/payments/fake-payment/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    user_id: userId,
                    plan_id: planId,
                    payment_method: paymentMethod
                })
            }
        );


        const data = await response.json();


        if (response.ok) {

            showResult(
                `
                <strong>Payment Successful!</strong>
                <br><br>
                Transaction ID:
                ${data.transaction_id}
                <br>
                Invoice ID:
                ${data.invoice_id}
                `,
                "success"
            );

            payButton.textContent = "Payment Complete";

        } else {

            showResult(
                data.error || "Payment failed.",
                "error"
            );

            payButton.disabled = false;
            payButton.textContent = "Pay Now";
        }


    } catch (error) {

        showResult(
            "Unable to process payment. Please try again.",
            "error"
        );

        payButton.disabled = false;
        payButton.textContent = "Pay Now";
    }

});


function showResult(message, type) {

    paymentResult.innerHTML = message;

    paymentResult.classList.remove(
        "hidden",
        "success",
        "error"
    );

    paymentResult.classList.add(type);
}