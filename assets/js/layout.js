/**
 * PCC - Plate-Forme Citoyenne des Compétences
 * Shared Layout Components (Header & Footer)
 */

document.addEventListener('DOMContentLoaded', () => {
    renderHeader();
    renderFooter();
    setupMobileMenu();
});

const pages = [
    { name: 'Accueil', url: 'index.html' },
    { name: 'Talents', url: 'explore.html' },
    { name: 'Opportunités', url: 'opportunities.html' },
];

const userPages = [
    { name: 'Tableau de Bord', url: 'dashboard.html', icon: 'dashboard' },
    { name: 'Mon Profil', url: 'profile.html', icon: 'person' },
    { name: 'Mes Compétences', url: 'skills.html', icon: 'terminal' },
    { name: 'Admin', url: 'admin.html', icon: 'admin_panel_settings' },
];

function renderHeader() {
    const header = document.getElementById('main-header');
    if (!header) return;

    const currentPath = window.location.pathname.split('/').pop() || 'index.html';

    const navLinks = pages.map(page => `
        <a class="${currentPath === page.url ? 'text-primary font-bold' : 'text-slate-600 dark:text-slate-400 hover:text-primary'} transition-colors" href="${page.url}">${page.name}</a>
    `).join('');

    header.className = "sticky top-0 z-50 bg-background-light/90 dark:bg-background-dark/90 backdrop-blur-md border-b border-primary/10 px-4 py-3";
    header.innerHTML = `
        <div class="max-w-7xl mx-auto flex items-center justify-between">
            <div class="flex items-center gap-2">
                <a href="index.html" class="flex items-center gap-2 group">
                    <div class="bg-primary p-2 rounded-lg flex items-center justify-center text-white group-hover:scale-110 transition-transform">
                        <i class="fas fa-star text-lg"></i>
                    </div>
                    <h1 class="text-xl font-extrabold tracking-tight text-primary">PCC</h1>
                </a>
            </div>
            
            <!-- Desktop Nav -->
            <div class="hidden md:flex items-center gap-8 text-sm font-bold uppercase tracking-widest">
                ${navLinks}
            </div>

            <div class="flex items-center gap-3">
                <button class="p-2 text-slate-600 dark:text-slate-400 hover:bg-primary/10 rounded-full transition-colors">
                    <i class="fas fa-search"></i>
                </button>
                <div class="hidden sm:flex items-center gap-2">
                    <a href="login.html" class="px-5 py-2 text-sm font-bold text-primary hover:bg-primary/10 rounded-xl transition-all">Connexion</a>
                    <a href="register.html" class="px-5 py-2 text-sm font-bold bg-primary text-white rounded-xl shadow-lg shadow-primary/20 hover:bg-primary/90 transition-all">Rejoindre</a>
                </div>
                <button id="mobile-menu-toggle" class="md:hidden p-2 text-slate-600 dark:text-slate-400 hover:bg-primary/10 rounded-full">
                    <i class="fas fa-bars"></i>
                </button>
            </div>
        </div>

        <!-- Mobile Menu Overlay -->
        <div id="mobile-menu" class="hidden fixed inset-0 z-[60] bg-slate-900/60 backdrop-blur-sm transition-all duration-300">
            <div class="absolute right-0 top-0 bottom-0 w-80 bg-background-light dark:bg-background-dark p-8 shadow-2xl flex flex-col">
                <div class="flex justify-between items-center mb-10">
                    <div class="flex items-center gap-2">
                        <div class="bg-primary p-2 rounded-lg text-white">
                            <i class="fas fa-star"></i>
                        </div>
                        <h2 class="text-xl font-black text-primary">Menu</h2>
                    </div>
                    <button id="mobile-menu-close" class="p-2 hover:bg-primary/10 rounded-full transition-colors">
                        <i class="fas fa-times text-xl text-slate-400"></i>
                    </button>
                </div>
                
                <div class="flex flex-col gap-2 font-bold text-lg mb-8">
                    <p class="text-xs uppercase tracking-widest text-slate-400 mb-2">Navigation</p>
                    ${pages.map(page => `
                        <a class="flex items-center justify-between p-4 rounded-2xl ${currentPath === page.url ? 'bg-primary/10 text-primary' : 'hover:bg-primary/5 text-slate-600 dark:text-slate-400'}" href="${page.url}">
                            ${page.name}
                            <i class="fas fa-chevron-right text-xs opacity-50"></i>
                        </a>
                    `).join('')}
                </div>

                <div class="flex flex-col gap-2 font-bold text-lg mb-8">
                    <p class="text-xs uppercase tracking-widest text-slate-400 mb-2">Mon Espace</p>
                    ${userPages.map(page => `
                        <a class="flex items-center gap-4 p-4 rounded-2xl ${currentPath === page.url ? 'bg-primary/10 text-primary' : 'hover:bg-primary/5 text-slate-600 dark:text-slate-400'}" href="${page.url}">
                            <i class="fas fa-${page.icon}"></i>
                            ${page.name}
                        </a>
                    `).join('')}
                </div>
                
                <div class="mt-auto pt-8 border-t border-slate-200 dark:border-slate-800 grid grid-cols-2 gap-4">
                    <a href="login.html" class="flex items-center justify-center p-4 border-2 border-primary/20 text-primary rounded-2xl text-sm font-bold">Connexion</a>
                    <a href="register.html" class="flex items-center justify-center p-4 bg-primary text-white rounded-2xl text-sm font-bold shadow-lg shadow-primary/20">Rejoindre</a>
                </div>
            </div>
        </div>
    `;
}

function renderFooter() {
    const footer = document.getElementById('main-footer');
    if (!footer) return;

    footer.className = "bg-slate-900 text-white pt-20 pb-10 px-4 mt-auto";
    footer.innerHTML = `
        <div class="max-w-7xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-16 mb-16 border-b border-slate-800 pb-16">
                <div class="col-span-1">
                    <div class="flex items-center gap-2 mb-8">
                        <div class="bg-primary p-2 rounded-xl flex items-center justify-center text-white scale-110">
                            <i class="fas fa-star text-lg"></i>
                        </div>
                        <h1 class="text-2xl font-black tracking-tight">PCC</h1>
                    </div>
                    <p class="text-slate-400 text-sm leading-relaxed mb-8">
                        La Plate-Forme Citoyenne des Compétences est une initiative citoyenne un Think Tank Citoyen pour valoriser les talents béninois.
                    </p>
                    <div class="flex gap-4">
                        <a class="size-11 rounded-xl bg-slate-800 flex items-center justify-center hover:bg-primary hover:-translate-y-1 transition-all" href="#">
                            <i class="fab fa-facebook-f text-lg"></i>
                        </a>
                        <a class="size-11 rounded-xl bg-slate-800 flex items-center justify-center hover:bg-primary hover:-translate-y-1 transition-all" href="#">
                            <i class="fab fa-twitter text-lg"></i>
                        </a>
                    </div>
                </div>
                <div>
                    <h6 class="font-black mb-8 text-primary uppercase text-xs tracking-[0.2em]">Plateforme</h6>
                    <ul class="space-y-5 text-sm font-bold text-slate-400">
                        <li><a class="hover:text-white transition-colors" href="#">Comment ça marche</a></li>
                        <li><a class="hover:text-white transition-colors" href="explore.html">Talents à la une</a></li>
                        <li><a class="hover:text-white transition-colors" href="opportunities.html">Offres d'emploi</a></li>
                        <li><a class="hover:text-white transition-colors" href="#">Actualités</a></li>
                    </ul>
                </div>
                <div>
                    <h6 class="font-black mb-8 text-primary uppercase text-xs tracking-[0.2em]">Support</h6>
                    <ul class="space-y-5 text-sm font-bold text-slate-400">
                        <li><a class="hover:text-white transition-colors" href="#">Aide & FAQ</a></li>
                        <li><a class="hover:text-white transition-colors" href="#">Contact</a></li>
                        <li><a class="hover:text-white transition-colors" href="#">Confidentialité</a></li>
                        <li><a class="hover:text-white transition-colors" href="#">Mentions Légales</a></li>
                    </ul>
                </div>
                <div class="bg-slate-800/50 p-8 rounded-3xl border border-slate-700">
                    <h6 class="font-black mb-4 text-white uppercase text-xs tracking-[0.2em]">Newsletter</h6>
                    <p class="text-xs text-slate-400 mb-6 font-medium">Restez informé des dernières opportunités nationales.</p>
                    <div class="flex gap-2">
                        <input class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 text-xs font-medium focus:ring-1 focus:ring-primary outline-none" placeholder="Email"/>
                        <button class="bg-primary p-3 rounded-xl text-white hover:bg-primary/90 transition-colors">
                            <i class="fas fa-paper-plane text-xs"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="flex flex-col md:flex-row justify-between items-center text-[10px] font-bold uppercase tracking-widest text-slate-500 gap-8">
                <p>© 2024 PCC. Tous droits réservés.</p>
                <div class="flex gap-8 items-center">
                    <a href="#" class="hover:text-white transition-colors">Confidentialité</a>
                    <a href="#" class="hover:text-white transition-colors">Cookies</a>
                    <div class="flex items-center gap-3 bg-slate-800 px-4 py-2 rounded-full border border-slate-700">
                        <img alt="Drapeau du Bénin" class="rounded-sm shadow-sm" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBEwnTrapCO6lQo9FMQP6i2RlQMe6q1f2rUpN0KHg5D6g9CnDUy_ZaHsu_Tjv6Q515lDeM7LCUZv0xoh_12Cy5NH9zZZUm_GpWToYDfULHdJWPeAFH6fXfOtqT2lv7cd17Ja-aa-ZZi_7SLgY56oi_GRZ8gnqjh_q8oM00SejcIW01aP05nPAUIsU1_jT2mwLwMf5LmpR0NbTI2beS6jq8c43urLSQsgo9h9Jt9sAT2t10wAm2z9ZpTIOGodoDh9a6MnBAbMl_J5c0" width="22"/>
                        <span class="text-xs">République du Bénin</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function setupMobileMenu() {
    const toggle = document.getElementById('mobile-menu-toggle');
    const close = document.getElementById('mobile-menu-close');
    const menu = document.getElementById('mobile-menu');

    if (toggle && menu) {
        toggle.addEventListener('click', () => {
            menu.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        });
    }

    if (close && menu) {
        close.addEventListener('click', () => {
            menu.classList.add('hidden');
            document.body.style.overflow = '';
        });
    }

    // Close on backdrop click
    if (menu) {
        menu.addEventListener('click', (e) => {
            if (e.target === menu) {
                menu.classList.add('hidden');
                document.body.style.overflow = '';
            }
        });
    }
}
