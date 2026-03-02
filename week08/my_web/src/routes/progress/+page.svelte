<script>
let quantity = 0
function increment() {
quantity += 1
}
function decrement() {
if (quantity === 0) {
return
}
quantity -= 1
}
</script>

<progress class="progress is-success" value={quantity} max="100">
  {quantity}%
</progress>

<div class="buttons">
<button class="button is-success is-light" onclick = {increment}>Success</button>
<button class="button is-danger is-light" onclick={decrement}>Danger</button>
</div>