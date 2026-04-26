<script>
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';
	import { cartStore, loadCart } from '$lib/cart.svelte.js';
	import { currentUser } from '$lib/shared';
	import { browser } from '$app/environment';

	let { data, children } = $props();
	let menuOpen = $state(false);

	if (browser && data.user) {
    	localStorage.setItem('current_user_id', data.user.customer_id);
	}

	// ดึงข้อมูล user จาก Server (ผ่านไฟล์ +layout.server.js)
	let user = $derived(data.user);
	currentUser.set(data.user);

	onMount(async () => {
    if (user && user.customer_id) {
        // บรรทัดนี้สำคัญมาก! ถ้าไม่มี ปุ่ม Add to Cart จะไม่รู้ว่าเป็นของใคร
        localStorage.setItem("current_user_id", user.customer_id.toString());
        await loadCart(user.customer_id);
    }
});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
	/>
</svelte:head>

<nav class="navbar has-background-primary" role="navigation" aria-label="main navigation">
	<div class="container">
		<div class="navbar-brand">
			<a class="navbar-item" href="/">
				<div style="display:flex; flex-direction:column; align-items:center;">
					<strong class="is-size-4">FIIT</strong>
					<p class="is-size-7 has-text-black">Your Clothes</p>
				</div>
			</a>

			<a
				role="button"
				class="navbar-burger"
				class:is-active={menuOpen}
				aria-label="menu"
				aria-expanded={menuOpen}
				onclick={() => (menuOpen = !menuOpen)}
			>
				<span aria-hidden="true"></span>
				<span aria-hidden="true"></span>
				<span aria-hidden="true"></span>
			</a>
		</div>

		<div id="navbarMenu" class="navbar-menu" class:is-active={menuOpen} style="text-align: center;">
			<div class="navbar-start" style="flex-grow: 1">
				<a class="navbar-item" href="/">Home</a>
				<a class="navbar-item" href="/community">
					Commu<span class="is-hidden-desktop">nity</span>
				</a>
			</div>

			<div class="navbar-end">
				<a class="navbar-item" href="/notify">
					<span class="icon"><i class="fas fa-bell"></i></span>
					<span class="is-hidden-desktop ml-1">Notification</span>
				</a>

				<a class="navbar-item" href="/cart" style="position: relative;">
					<div style="position: relative; display: inline-block;">
						<span class="icon">
							<i class="fas fa-shopping-cart"></i>
						</span>

						{#if cartStore.count > 0}
							<span
								class="tag is-danger is-rounded is-small"
								style="position: absolute; top: -8px; right: -12px; font-size: 0.65rem; height: 1.5em; min-width: 1.5em; padding: 0.2em; border: 2px solid #00d1b2;"
							>
								{cartStore.count}
							</span>
						{/if}
						<span class="is-hidden-desktop ml-2">Cart</span>
					</div>
				</a>

				<div class="navbar-item">
					<div class="buttons">
						{#if user}
							<a href="/profile" class="button is-white is-rounded has-text-weight-bold">
								<span class="icon"><i class="fas fa-user mr-2"></i></span>
								{user.display_name || user.username}
							</a>
						{:else}
							<a href="/signin" class="button is-white is-rounded has-text-weight-bold">
								Sign In
							</a>
						{/if}
					</div>
				</div>
			</div>
		</div>
	</div>
</nav>

{@render children()}

<style>
	@media (max-width: 1023px) {
		:global(.navbar-menu.is-active .navbar-item) {
			justify-content: center;
		}
		:global(.navbar-menu.is-active .navbar-start),
		:global(.navbar-menu.is-active .navbar-end) {
			display: flex;
			flex-direction: column;
			align-items: center;
		}

		:global(.navbar-item .button.is-white) {
			background-color: transparent !important;
			border: none !important;
			box-shadow: none !important;
		}

		:global(.navbar-item) {
			display: flex;
			justify-content: center;
		}
	}

	@media (min-width: 1024px) {
		:global(.navbar-item:hover) {
			background-color: transparent !important;
		}
	}

	.icon-wrapper {
		position: relative;
		display: inline-block;
	}
</style>