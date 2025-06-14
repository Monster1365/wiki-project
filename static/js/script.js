document.querySelectorAll('.section-header').forEach(header => {
        header.addEventListener('click', () => {
          const sectionBody = header.nextElementSibling;
          const toggleIcon = header.querySelector('.toggle-button');
          const isVisible = sectionBody.style.display !== 'none';
          sectionBody.style.display = isVisible ? 'none' : 'block';
          toggleIcon.textContent = isVisible ? '▶' : '▼';
        });
});