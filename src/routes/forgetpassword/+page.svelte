<script>
  
  let email = $state('');
  let error = $state(''); 
  let successMessage = $state(''); 

  function handleReset() {
    console.log('ปุ่ม Send Reset Link ถูกกด!');
    
  }
</script>

<section class="hero is-primary">
  <div class="hero-body py-3">
    <div class="container has-text-centered">
      <p class="title is-4 mb-0">Reset Password</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-4-desktop is-5-tablet">
        <div class="box">
          
          <p class="has-text-centered is-size-7 mb-5 has-text-grey-dark">
            Enter your email address and we'll send you a link to reset your password.
          </p>

          <div class="field">
            <label class="label">Email</label>
            <div class="control has-icons-left">
              <input
                class="input is-primary"
                type="email"
                placeholder="Enter your email"
                bind:value={email}
              />
              <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
              </span>
            </div>
          </div>

          {#if error}
            <div class="notification is-danger is-light is-size-7 py-2 px-3 mb-4">
              {error}
            </div>
          {/if}

          {#if successMessage}
            <div class="notification is-success is-light is-size-7 py-2 px-3 mb-4">
              {successMessage}
            </div>
          {/if}

          <button class="button is-primary is-fullwidth mt-2 mb-5" onclick={handleReset}>
            Send Reset Link
          </button>

          <div class="has-text-centered">
            <a class="is-size-7 has-text-grey" href="/signin">
              <span class="icon is-small"><i class="fas fa-arrow-left"></i></span>
              Back to Sign In
            </a>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  
  .notification {
    border-radius: 8px;
  }
</style>