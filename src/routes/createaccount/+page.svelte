<script>

  let name = $state('');
  let email = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let error = $state('');
  let successMessage = $state('');

  function handleSignUp() {
    if (!name || !email || !password || !confirmPassword) {
      error = 'กรุณากรอกข้อมูลให้ครบทุกช่อง' ;
      successMessage= '' ;
      return ;
    }

    if (password !== confirmPassword) {
      error = 'รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน';
      successMessage= '' ;
      return ;
    }

    error ='';
    successMessage ='สมัครสมาชิกสำเร็จ กำลังพากลับไปหน้าเข้าสู่ระบบ...';

    name ='';
    email='';
    password='';
    confirmPassword='';
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

          {#if password !== '' && confirmPassword !== ''}
            {#if password === confirmPassword}
              <p class="help is-success mb-3">✓ รหัสผ่านตรงกัน</p>
            {:else}
              <p class="help is-danger mb-3">✗ รหัสผ่านยังไม่ตรงกัน</p>
            {/if}
          {/if}

          {#if error}
            <div class="notification is-danger is-light is-size-7 py-2 mb-3">
              {error}
            </div>
          {/if}

          {#if successMessage}
            <div class="notification is-success is-light is-size-7 py-2 mb-3">
              {successMessage}
            </div>
          {/if}

          <button class="button is-primary is-fullwidth mt-3 mb-4" onclick={handleSignUp}>
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