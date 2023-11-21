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
                const contentContainer = document.querySelector('.content');
                contentContainer.innerHTML = newDocument.querySelector('.content').innerHTML;
            })
            .catch(error => console.error('Error fetching content:', error));
    }


});
// ... (previous script content) ...
function showForm(formName) {
        const formsContainer = document.getElementById('forms-container');
        fetch(`/${formName}`)
            .then(response => response.text())
            .then(html => {
                formsContainer.innerHTML = html;
                // Add event listener to the form submit button
                const form = formsContainer.querySelector('form');
                if (form) {
                    form.addEventListener('submit', function (event) {
                        event.preventDefault();
                        handleFormSubmit(form);
                    });
                }
            })
            .catch(error => console.error('Error fetching form:', error));
    }

    function handleFormSubmit(form) {
        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            // Update the forms-container with the updated HTML
            const formsContainer = document.getElementById('forms-container');
            formsContainer.innerHTML = html;
        })
        .catch(error => console.error('Error submitting form:', error));
    }
// ... (previous script content) ...

function showView(viewName) {
    const viewContainer = document.getElementById('view-container');
    fetch(`/${viewName}`)
        .then(response => response.text())
        .then(html => {
            viewContainer.innerHTML = html;
        })
        .catch(error => console.error('Error fetching view:', error));
}
// ... (previous script content) ...


function showEditForm(supplierId) {
    const editContainer = document.getElementById('edit-container');
    fetch(`/edit_supplier/${supplierId}`)
        .then(response => response.text())
        .then(html => {
            editContainer.innerHTML = html;
        })
        .catch(error => console.error('Error fetching edit form:', error));
}

function hideEditForm() {
    const editContainer = document.getElementById('edit-container');
    editContainer.innerHTML = ''; // Clear the content
}