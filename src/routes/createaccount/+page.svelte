<script>

  let name = $state('');
  let email = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let error = $state(''); 

  function handleSignUp() {
    console.log('ปุ่ม Sign Up ถูกกด!');
  }
  
</script>

<section class="hero is-primary">
  <div class="hero-body py-3">
    <div class="container has-text-centered">
      <p class="title is-4 mb-0">Create Account</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-4-desktop is-5-tablet">
        <div class="box">
          
          <div class="field">
            <label class="label">Name</label>
            <div class="control">
              <input
                class="input is-primary"
                type="text"
                placeholder="Enter your full name"
                bind:value={name}
              />
            </div>
          </div>

          <div class="field">
            <label class="label">Email</label>
            <div class="control">
              <input
                class="input is-primary"
                type="email"
                placeholder="Enter your email"
                bind:value={email}
              />
            </div>
          </div>

          <div class="field">
            <label class="label">Password</label>
            <div class="control">
              <input
                class="input is-primary"
                type="password"
                placeholder="Create a password"
                bind:value={password}
              />
            </div>
          </div>

          <div class="field">
            <label class="label">Confirm Password</label>
            <div class="control">
              <input
                class="input is-primary"
                type="password"
                placeholder="Confirm your password"
                bind:value={confirmPassword}
              />
            </div>
          </div>

          {#if error}
            <p class="has-text-danger is-size-7 mb-3">{error}</p>
          {/if}

          <button class="button is-primary is-fullwidth mt-5 mb-4" onclick={handleSignUp}>
            Sign Up
          </button>

          <p class="has-text-centered is-size-7 has-text-grey mb-3">or continue with</p>

          <div class="buttons">
            <button class="button is-light is-fullwidth">Google</button>
            <button class="button is-light is-fullwidth">Facebook</button>
            <button class="button is-light is-fullwidth">Apple</button>
          </div>

          <div class="has-text-centered mt-4">
            <p class="is-size-7">
              Already have an account?
              <a class="has-text-primary" href="/signin">Sign in</a>
            </p>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</section>