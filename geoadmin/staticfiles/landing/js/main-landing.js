const STORAGE_KEY = "geoAdminLoggedIn";

function getLoginState() {
	return localStorage.getItem(STORAGE_KEY) === "true";
}

function setLoginState(isLoggedIn) {
	localStorage.setItem(STORAGE_KEY, String(isLoggedIn));
}

function renderAuthUI(isLoggedIn) {
	const sidebar = document.getElementById("sidebar");
	const loginBtn = document.getElementById("loginBtn");
	const logoutBtn = document.getElementById("logoutBtn");

	if (!sidebar || !loginBtn || !logoutBtn) {
		return;
	}

	sidebar.classList.toggle("is-hidden", !isLoggedIn);
	sidebar.setAttribute("aria-hidden", String(!isLoggedIn));
	loginBtn.classList.toggle("is-hidden", isLoggedIn);
	logoutBtn.classList.toggle("is-hidden", !isLoggedIn);
	document.body.classList.toggle("sidebar-open", isLoggedIn);
}

function initAuthControls() {
	const loginBtn = document.getElementById("loginBtn");
	const logoutBtn = document.getElementById("logoutBtn");

	if (!loginBtn || !logoutBtn) {
		return;
	}

	renderAuthUI(getLoginState());

	loginBtn.addEventListener("click", () => {
		window.location.href = "/user";
	});

	logoutBtn.addEventListener("click", () => {
		setLoginState(false);
		renderAuthUI(false);
	});
}

function initMobileTopbarMenu() {
	const menuToggle = document.getElementById("menuToggle");
	const topbarNav = document.querySelector(".topbar-nav");
	const topbarMenu = document.getElementById("topbarMenu");

	if (!menuToggle || !topbarNav || !topbarMenu) {
		return;
	}

	const closeMenu = () => {
		topbarNav.classList.remove("menu-open");
		menuToggle.setAttribute("aria-expanded", "false");
	};

	menuToggle.addEventListener("click", () => {
		const isOpen = topbarNav.classList.toggle("menu-open");
		menuToggle.setAttribute("aria-expanded", String(isOpen));
	});

	document.addEventListener("click", (event) => {
		if (!topbarNav.contains(event.target)) {
			closeMenu();
		}
	});

	topbarMenu.addEventListener("click", (event) => {
		const target = event.target;
		if (target instanceof HTMLElement && target.classList.contains("nav-link")) {
			closeMenu();
		}
	});
}

function initNavbarEffect() {
	const navbar = document.querySelector(".topbar");
	const hero = document.querySelector(".hero-full");

	if (!navbar || !hero) return;

	function updateNavbar() {
		const rect = hero.getBoundingClientRect();
		if (rect.bottom <= 80) {
			navbar.classList.add("scrolled");
		} else {
			navbar.classList.remove("scrolled");
		}
	}

	window.addEventListener("scroll", updateNavbar);
}

function initNosotrosSlider() {
	const slider = document.getElementById("nosotrosSlider");
	if (!slider) return;

	let index = 0;
	const total = slider.children.length;

	setInterval(() => {
		index = (index + 1) % total;
		slider.style.transform = `translateX(-${index * 100}%)`;
	}, 5000);
}

function initHeroSlider() {
	const slider = document.getElementById("heroSlider");
	const dots = document.querySelectorAll("#heroDots .dot");

	if (!slider) return;

	let index = 0;
	const total = slider.children.length;

	function updateSlider(i) {
		index = i;
		slider.style.transform = `translateX(-${index * 100}%)`;
		dots.forEach(dot => dot.classList.remove("active"));
		dots[index].classList.add("active");
		const slides = slider.querySelectorAll(".slide");
		slides.forEach(slide => {
			slide.classList.remove("active");
			const img = slide.querySelector("img");
			img.style.animation = "none";
			img.offsetHeight;
			img.style.animation = null;
		});
		slides[index].classList.add("active");
	}

	dots.forEach(dot => {
		dot.addEventListener("click", () => {
			updateSlider(Number(dot.dataset.index));
		});
	});

	setInterval(() => {
		updateSlider((index + 1) % total);
	}, 5000);
}

function initCtaSlider() {
	const slides = document.querySelectorAll(".cta-slide");
	let index = 0;

	if (!slides.length) return;

	setInterval(() => {
		slides[index].classList.remove("active");
		index = (index + 1) % slides.length;
		slides[index].classList.add("active");
	}, 5000);
}

document.addEventListener("DOMContentLoaded", () => {
	initAuthControls();
	initMobileTopbarMenu();
	initHeroSlider();
	initNosotrosSlider();
	initNavbarEffect();
	initCtaSlider();
});