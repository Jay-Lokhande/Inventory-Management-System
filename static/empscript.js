document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('.sidebar a');

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            // Prevent the default behavior of the link
            event.preventDefault();

            // Remove the 'active' class from all links
            links.forEach(l => l.classList.remove('active'));

            // Add the 'active' class to the clicked link
            link.classList.add('active');

            // Fetch and display the content for the clicked link
            const url = link.getAttribute('href');
            fetchContent(url);
        });
    });

    // Function to fetch and display content
    function fetchContent(url) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const newDocument = parser.parseFromString(html, 'text/html');

                // Update the content area with the new content
                const contentContainer = document.querySelector('.container');
                contentContainer.innerHTML = newDocument.querySelector('.container').innerHTML;
            })
            .catch(error => console.error('Error fetching content:', error));
    }


});