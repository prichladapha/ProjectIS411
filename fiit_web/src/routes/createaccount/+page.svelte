<script>
  import { enhance } from '$app/forms';

  let { form } = $props();
  let password = $state('');
  let confirmPassword = $state('');
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
          
          <form method="POST" use:enhance>
            
            <div class="field">
              <label class="label">Username</label>
              <div class="control">
                <input
                  class="input is-primary"
                  type="text"
                  name="name" 
                  placeholder="Enter your username"
                  value={form?.name ?? ''}
                  required
                />
              </div>
            </div>

            <div class="field">
              <label class="label">Display Name</label>
              <div class="control">
                <input
                  class="input is-primary"
                  type="text"
                  name="display_name" 
                  placeholder="ชื่อที่จะใช้แสดง (ไม่บังคับ)"
                  value={form?.display_name ?? ''}
                />
              </div>
            </div>

            <div class="field">
              <label class="label">Email</label>
              <div class="control">
                <input
                  class="input is-primary"
                  type="email"
                  name="email"
                  placeholder="Enter your email"
                  value={form?.email ?? ''}
                  required
                />
              </div>
            </div>

            <div class="field">
              <label class="label">Phone Number</label>
              <div class="control">
                <input
                  class="input is-primary"
                  type="tel"
                  name="phone"
                  placeholder="08X-XXX-XXXX"
                  value={form?.phone ?? ''}
                  required
                />
              </div>
            </div>

            <div class="field">
              <label class="label">Password</label>
              <div class="control">
                <input
                  class="input is-primary"
                  type="password"
                  name="password"
                  placeholder="Create a password"
                  bind:value={password}
                  required
                />
              </div>
            </div>

            <div class="field">
              <label class="label">Confirm Password</label>
              <div class="control">
                <input
                  class="input is-primary"
                  type="password"
                  name="confirmPassword"
                  placeholder="Confirm your password"
                  bind:value={confirmPassword}
                  required
                />
              </div>
            </div>

            {#if password !== '' && confirmPassword !== ''}
              {#if password === confirmPassword}
                <p class="help is-success mb-3">✓ รหัสผ่านตรงกัน</p>
              {:else}
                <p class="help is-danger mb-3">✗ รหัสผ่านยังไม่ตรงกัน</p>
              {/if}
            {/if}

            {#if form?.success}
              <div class="notification is-success is-light is-size-7 py-2 mb-3">
                {form.message}
              </div>
            {/if}

            {#if form?.error}
              <div class="notification is-danger is-light is-size-7 py-2 mb-3">
                {form.error}
              </div>
            {/if}

            <button class="button is-primary is-fullwidth mt-3 mb-4" type="submit">
              Sign Up
            </button>
          </form>

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