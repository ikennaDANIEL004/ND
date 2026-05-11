document.addEventListener('DOMContentLoaded', () => { // wait for the HTML document to finish loading before running the script
  const menuButton = document.getElementById('mobileMenuButton'); // get the mobile menu toggle button by its ID
  const menu = document.getElementById('mobileMenu'); // get the mobile menu panel element by its ID
  const backdrop = document.getElementById('mobileMenuBackdrop'); // get the backdrop element that appears behind the mobile menu
  const closeButtons = document.querySelectorAll('[data-menu-close]'); // select all buttons that should close the mobile menu
  const nav = document.querySelector('nav'); // select the page navigation element
  const whiteSections = Array.from(document.querySelectorAll('section.bg-white, section.bg-slate-50')); // get all sections with white or slate background styles

  const openMenu = () => { // define a function to open the mobile menu
    menu.classList.remove('translate-x-full'); // remove the class that hides the menu offscreen
    backdrop.classList.remove('opacity-0', 'pointer-events-none'); // make the backdrop visible and interactive
    menuButton.setAttribute('aria-expanded', 'true'); // update accessibility state to indicate the menu is open
    document.body.classList.add('overflow-hidden'); // prevent page scrolling while the menu is open
  };

  const closeMenu = () => { // define a function to close the mobile menu
    menu.classList.add('translate-x-full'); // add the class that hides the menu offscreen
    backdrop.classList.add('opacity-0', 'pointer-events-none'); // hide the backdrop and disable its pointer events
    menuButton.setAttribute('aria-expanded', 'false'); // update accessibility state to indicate the menu is closed
    document.body.classList.remove('overflow-hidden'); // restore page scrolling
  };

  if (menuButton) { // if the menu button exists on the page
    menuButton.addEventListener('click', openMenu); // attach a click listener to open the mobile menu
  }

  if (backdrop) { // if the backdrop element exists
    backdrop.addEventListener('click', closeMenu); // attach a click listener to close the menu when clicking the backdrop
  }

  closeButtons.forEach((button) => button.addEventListener('click', closeMenu)); // attach close handler to each close button in the menu

  document.addEventListener('keydown', (event) => { // listen for keyboard events on the document
    if (event.key === 'Escape') { // if the Escape key is pressed
      closeMenu(); // close the mobile menu
    }
  });

  if (nav && whiteSections.length > 0) { // if a nav exists and there are white background sections to observe
    const observer = new IntersectionObserver((entries) => { // create an observer to watch section visibility
      const shouldUseContrast = entries.some((entry) => entry.isIntersecting); // check if any observed section is intersecting the viewport
      nav.classList.toggle('nav--contrast', shouldUseContrast); // toggle contrast styling on the nav based on visibility
    }, {
      rootMargin: '-80px 0px 0px 0px', // adjust the observer's viewport bounds to trigger earlier or later
      threshold: 0 // trigger when any part of the observed element enters the viewport
    });

    whiteSections.forEach((section) => observer.observe(section)); // start observing each white background section
  }
});
