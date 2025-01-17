document.addEventListener('DOMContentLoaded', function() {

    var sections = document.querySelectorAll('.content section');
    
    sections.forEach(function(section, index) {
        if (index !== 0) {
            section.style.display = 'none';
        }
    });
    
    var sidebarLinks = document.querySelectorAll('.sidebar ul a');
    sidebarLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {

            var targetId = this.getAttribute('href').substring(1);

            sections.forEach(function(section) {
                section.style.display = 'none';
            });
        
            document.getElementById(targetId).style.display = 'flex';
            
            var sidebar = document.querySelector('.sidebar');
            var checkbox = document.querySelector('#check');
            sidebar.classList.remove('show');
            checkbox.checked = false;
            event.preventDefault();
        });
    });
});


