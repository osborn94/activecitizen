// Script for Mobile toggle button

// Selecting all necessary classes
const menuToggle = document.getElementsByClassName('menuToggle')[0];
const navLink = document.getElementsByClassName('m-nav-link')[0];

// adding event listener to the toggle bar
menuToggle.addEventListener('click', toggle);

// function to toggle mobile Nav-Bar
function toggle() {
  const x = document.getElementsByClassName('m-nav-link')[0];
  if (x.style.display === 'none') {
    x.style.display = 'block';
  } else {
    x.style.display = 'none';
  }
}

// End of mobile toggle button

// Carousel
class Carousel {
  constructor(container, items, controls, autoplayInterval) {
    this.carouselContainer = container;
    this.carouselControls = controls;
    this.carouselArray = [...items];
    this.autoplayInterval = autoplayInterval;
    this.autoplayTimer = null;
  }

  updateGallery() {
    this.carouselArray.forEach((el) => {
      el.classList.remove('gallery-item-1');
      el.classList.remove('gallery-item-2');
      el.classList.remove('gallery-item-3');
      el.classList.remove('gallery-item-4');
      el.classList.remove('gallery-item-5');
    });
    this.carouselArray.slice(0, 5).forEach((el, i) => {
      el.classList.add(`gallery-item-${i + 1}`);
    });
  }

  setCurrentState(direction) {
    if (direction.classList.contains('gallery-controls-previous')) {
      this.carouselArray.unshift(this.carouselArray.pop());
    } else {
      this.carouselArray.push(this.carouselArray.shift());
    }
    this.updateGallery();
  }

  setControls() {
    this.carouselControls.forEach((control) => {
      this.carouselControlsContainer.appendChild(
        document.createElement('button')
      ).className = `gallery-controls-${control}`;
      document.querySelector(`.gallery-controls-${control}`).innerText =
        control;
    });
  }

  useControls() {
    const triggers = [...this.carouselControlsContainer.childNodes];
    triggers.forEach((control) => {
      control.addEventListener('click', (e) => {
        e.preventDefault();
        this.setCurrentState(control);
      });
    });
  }

  startAutoplay() {
    this.autoplayTimer = setInterval(() => {
      this.setCurrentState(document.querySelector('.gallery-controls-next'));
    }, this.autoplayInterval);
  }

  stopAutoplay() {
    clearInterval(this.autoplayTimer);
  }

  init() {
    this.carouselControlsContainer =
      document.querySelector('.gallery-controls');
    this.setControls();
    this.useControls();
    this.startAutoplay();
  }
}

const galleryContainer = document.querySelector('.gallery-container');
const galleryControls = ['previous', 'next'];
const galleryItems = document.querySelectorAll('.gallery-item');
const exampleCarousel = new Carousel(
  galleryContainer,
  galleryItems,
  galleryControls,
  3000 // Set autoplay interval to 3 seconds (adjust as needed)
);
exampleCarousel.init();

// End of carousel
