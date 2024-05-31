// Define a function to fetch movies
function getMovies() {
    fetch('http://127.0.0.1:5000/movies') // Make a GET request to the /movies endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Parse the JSON response
        })
        .then(data => {
            console.log('Movies:', data); // Log the retrieved movie data
            const tableBody = document.getElementById('apiTableBody');

        // Clear existing table rows
        tableBody.innerHTML = '';

        // Iterate over the movies array in the response
        data.movies.forEach(movie => {
            // Create a new table row
            const row = tableBody.insertRow();

            // Populate the table row with movie data
            row.innerHTML = `<td>${movie.id}</td>
                             <td>${movie.name}</td>
                             <td>${movie.year}</td>
                             <td>${movie.genre}</td>
                             <td>${movie.director}</td>`;
        });
            // Handle the movie data as needed
        })
        .catch(error => {
            console.error('Error fetching movies:', error); // Log any errors
        });
}


// Get a reference to the form element
const form = document.getElementById('myForm');
const error_msg = document.getElementById('post-error')
// Add an event listener for the form submit event
form.addEventListener('submit', function(event) {
     // Prevent the default form submission behavior
    event.preventDefault();
    const formData = new FormData(form);
    
    const postData = {}
    formData.forEach((value, key) => {
        postData[key]=value;
    });
    console.log(postData);

    console.log(JSON.stringify(postData))
    fetch('http://127.0.0.1:5000/movies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
            error_msg.innerHTML="Network response was not ok";
        }
        return response.json();
    })
    .then(data => {
        console.log('Form data submitted successfully:', data);
        // Handle the response data as needed
        document.getElementById('myForm').reset();

        // Redirect to another page
        window.location.href = 'index.html';
    })
    .catch(error => {
        error_msg.innerHTML="Error submitting form data:"+error;
        console.error('Error submitting form data:', error);
    });
})

