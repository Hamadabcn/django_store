let stripe, elements;
const stripeSubmit = document.getElementById('stripe-submit');

async function createStripeSession() {

  const form = document.getElementById('form-user-info');
  const formData = new FormData(form);

  switchPaymentMethod('stripe', '')

  stripeSubmit.disabled = true;
  try {
    const { data } = await axios.post("/checkout/stripe", formData)
    const { client_secret } = data;

    const appearance = { theme: 'flat' };
    elements = stripe.elements({ appearance, clientSecret: client_secret });
    const paymentElement = elements.create("payment")
    paymentElement.mount("#payment-element");

    document
    .querySelector("#payment-form")
    .addEventListener("submit", _stripeFormSubmit);

    document.getElementById('stripe-card').style.display = 'block'
    stripeSubmit.disabled = false;
  } catch (e) {
    console.log(e)
    notyf.error(e.response.data.message);
  }
}

async function _stripeFormSubmit(e) {
  e.preventDefault();
  stripeSubmit.disabled = true;
  const host = window.location.protocol + "//" + window.location.host;
  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: `${host}/checkout/complete`,
    },
  });

  if (error.type === "card_error" || error.type === "validation_error") {
    notyf.error(error.message);
  } else {
    notyf.error("Sorry, an error occurred during the payment process");
  }
  stripeSubmit.disabled = false;
}

async function _checkStripePaymentStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );
  if (!clientSecret) {
    return;
  }
  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
  switch (paymentIntent.status) {
    case "succeeded":
      notyf.success("Your payment has been completed successfully");
      break;
    case "processing":
      notyf.success("Payment is being processed");
      break;
    default:
      notyf.error("Sorry, an error occurred during the payment process");
      break;
  }
}

async function _stripeInit() {
    const { data } = await axios("/checkout/stripe/config");
    stripe = Stripe(data.public_key, { locale: 'ar' });
    _checkStripePaymentStatus();
}

_stripeInit();
