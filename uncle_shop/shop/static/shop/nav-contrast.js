(() => {
  const bindOnce = (element, eventName, handler, key) => {
    if (!element || element.dataset[key]) {
      return;
    }
    element.dataset[key] = 'true';
    element.addEventListener(eventName, handler);
  };

  const initSiteChrome = () => {
    const menuButton = document.getElementById('mobileMenuButton');
    const menu = document.getElementById('mobileMenu');
    const backdrop = document.getElementById('mobileMenuBackdrop');
    const closeButtons = document.querySelectorAll('[data-menu-close]');
    const nav = document.querySelector('nav');
    const whiteSections = Array.from(document.querySelectorAll('section.bg-white, section.bg-slate-50'));
    const modal = document.getElementById('siteModal');
    const modalMessage = document.getElementById('siteModalMessage');
    const modalOk = document.getElementById('siteModalOk');
    const mobileSearchForm = document.getElementById('mobileSearchForm');
    const mobileSearchInput = document.getElementById('mobileSearchInput');

    const showModal = (message) => {
      if (!modal || !modalMessage) {
        return;
      }
      modalMessage.textContent = message;
      modal.classList.remove('hidden');
      modal.classList.add('flex');
      document.body.classList.add('modal-open');
    };

    const hideModal = () => {
      if (!modal) {
        return;
      }
      modal.classList.add('hidden');
      modal.classList.remove('flex');
      document.body.classList.remove('modal-open');
    };

    const openMenu = () => {
      if (!menu || !backdrop || !menuButton) {
        return;
      }
      menu.classList.remove('translate-x-full');
      backdrop.classList.remove('opacity-0', 'pointer-events-none');
      menuButton.setAttribute('aria-expanded', 'true');
      document.body.classList.add('overflow-hidden');
    };

    const closeMenu = () => {
      if (!menu || !backdrop || !menuButton) {
        return;
      }
      menu.classList.add('translate-x-full');
      backdrop.classList.add('opacity-0', 'pointer-events-none');
      menuButton.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('overflow-hidden');
    };

    bindOnce(menuButton, 'click', openMenu, 'menuOpenBound');
    bindOnce(backdrop, 'click', closeMenu, 'menuBackdropBound');
    closeButtons.forEach((button) => bindOnce(button, 'click', closeMenu, 'menuCloseBound'));

    bindOnce(mobileSearchForm, 'submit', (event) => {
      event.preventDefault();
      if (mobileSearchInput && mobileSearchInput.value.trim()) {
        showModal('No goods displayed for now. Contact us if you want any. Thank you.');
      }
    }, 'searchBound');

    bindOnce(modalOk, 'click', hideModal, 'modalOkBound');
    bindOnce(modal, 'click', (event) => {
      if (event.target === modal) {
        hideModal();
      }
    }, 'modalBackdropBound');

    if (!document.documentElement.dataset.escapeBound) {
      document.documentElement.dataset.escapeBound = 'true';
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
          closeMenu();
          hideModal();
        }
      });
    }

    const successMessage = document.querySelector('[data-contact-success]');
    if (successMessage && !successMessage.dataset.shown) {
      successMessage.dataset.shown = 'true';
      showModal(successMessage.textContent.trim());
    }

    if (nav && whiteSections.length > 0 && !nav.dataset.contrastBound) {
      nav.dataset.contrastBound = 'true';
      const observer = new IntersectionObserver((entries) => {
        const shouldUseContrast = entries.some((entry) => entry.isIntersecting);
        nav.classList.toggle('nav--contrast', shouldUseContrast);
      }, {
        rootMargin: '-80px 0px 0px 0px',
        threshold: 0
      });

      whiteSections.forEach((section) => observer.observe(section));
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSiteChrome);
  } else {
    initSiteChrome();
  }

  document.addEventListener('htmx:load', initSiteChrome);
  document.addEventListener('htmx:afterSwap', initSiteChrome);
})();
