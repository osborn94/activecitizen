const links = document.querySelectorAll('.pagination .page-link');

links.forEach(link => {
  link.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default action of the link
    
    // Example: Redirect to different pages based on link text
    switch (this.textContent) {
      case '1':
        window.location.href = '/qubes/light/app-contact.html';
        break;
      case '2':
        window.location.href = '/qubes/light/app-contact2.html';
        break;
      case '3':
        window.location.href = '/qubes/light/app-contact3.html';
        break;
      default:
        break;
    }
  });
});
