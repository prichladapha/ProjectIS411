<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>


<section class="icon-demo">
            <div class="icon-row">
                <div class="icon-card">
                    <i class="fas fa-home"></i>
                    <p>Home</p>
                </div>
                <div class="icon-card">
                    <i class="fas fa-user"></i>
                    <p>User</p>
                </div>
                <div class="icon-card">
                    <i class="fas fa-envelope"></i>
                    <p>Email</p>
                </div>
                <div class="icon-card">
                    <i class="fas fa-cog"></i>
                    <p>Settings</p>
                </div>
                <div class="icon-card">
                    <i class="fab fa-twitter"></i>
                    <p>Twitter</p>
                </div>
            </div>
        </section>
<div class="buttons">
<button class="button is-primary">Primary</button>
<button class="button is-link">Link</button>
</div>
 
<div class="buttons">
<button class="button is-info is-light">Info</button>
<button class="button is-success is-light">Success</button>
<button class="button is-warning is-light">Warning</button>
<button class="button is-danger is-light">Danger</button>
</div>

<style>
.icon-demo {
    background-color: #ffc9c9;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    margin: 0 auto;
    text-align: center;
}

.icon-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 25px;
    justify-items: center;
    margin-top: 30px;
}

.icon-card {
    background-color: #f0f2f5;
    padding: 30px;
    border-radius: 10px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-align: center;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    width: 150px;
}

.icon-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.icon-card i {
    font-size: 3.5rem;
    transition: color 0.3s ease;
}

.icon-card i.fa-home {
    color: #fa4e30;
}

.icon-card i.fa-user {
    color: #74f79fee;
}

.icon-card i.fa-envelope {
    color: #5cabff;
}

.icon-card i.fa-cog {
    color: #ffb84d;
}

.icon-card i.fa-twitter {
    color: #4cbaff;
}

.icon-card p {
    margin-top: 15px;
    font-size: 1.1rem;
    color: #000000;
    font-weight: 500;
}
</style>