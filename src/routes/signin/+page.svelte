<script>
  import { goto } from '$app/navigation';
  import { currentUser } from '$lib/shared';

  let email = '';
  let password = '';
  let error = '';

  async function handleSignIn() {
    error = '';

    if (!email || !password) {
      error = 'Please enter email and password';
      return;
    }


    if (email === 'test@gmail.com' && password === '1234') {
      currentUser.set({ name: 'notyourkiko', avatar: 'https://i.pinimg.com/1200x/d0/a8/24/d0a824014719918bc812e52c29f6c7a6.jpg' }); // 
      goto('/profile');
    } else {
      error = 'Invalid email or password';
    }
  }
</script>

<section class="hero is-primary">
  <div class="hero-body py-3">
    <div class="container has-text-centered">
      <p class="title is-4 mb-0">SignIn</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-4-desktop is-5-tablet">
        <div class="box">
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
                placeholder="Enter your password"
                bind:value={password}
              />
            </div>
          </div>

          {#if error}
            <p class="has-text-danger is-size-7 mb-3">{error}</p>
          {/if}

          <div class="is-flex is-justify-content-flex-end mb-4">
            <a class="is-size-7 has-text-primary" href="/forgetpassword">Forgot password?</a>
          </div>

          <button class="button is-primary is-fullwidth mb-4" on:click={handleSignIn}>
            SignIn
          </button>

          <p class="has-text-centered is-size-7 has-text-grey mb-3">or continue with</p>

          <div class="buttons">
            <button class="button is-light is-fullwidth">Google</button>
            <button class="button is-light is-fullwidth">Facebook</button>
            <button class="button is-light is-fullwidth">Apple</button>
          </div>

          <div class="has-text-centered mt-4">
            <p class="is-size-7">
              Don’t have an account?
              <a class="has-text-primary" href="/createaccount">Create account</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>