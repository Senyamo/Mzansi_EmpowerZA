// jobs.js

document.addEventListener('DOMContentLoaded', function () {
    let currentPage = 1;
    const jobsContainer = document.getElementById('jobs-container');
    const loadMoreButton = document.getElementById('load-more');

    // Function to fetch jobs from API and display them
    function fetchJobs(page = 1) {
        fetch(`/api/jobs?page=${page}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    jobsContainer.innerHTML = `<p>${data.error}</p>`;
                } else {
                    displayJobs(data);
                    currentPage = page;
                    toggleLoadMoreButton(data.length);
                }
            })
            .catch(error => {
                jobsContainer.innerHTML = `<p>Error loading jobs. Please try again later.</p>`;
                console.error('Error fetching jobs:', error);
            });
    }

    // Function to display jobs on the page
    function displayJobs(jobs) {
        jobs.forEach(job => {
            const jobElement = document.createElement('div');
            jobElement.classList.add('job-item');
            jobElement.innerHTML = `
                <h3>${job.title}</h3>
                <p><strong>Company:</strong> ${job.company}</p>
                <p><strong>Location:</strong> ${job.location}</p>
                <p>${job.description}</p>
                <a href="${job.url}" target="_blank">View Job</a>
            `;
            jobsContainer.appendChild(jobElement);
        });
    }

    // Function to toggle the "Load More" button visibility
    function toggleLoadMoreButton(jobCount) {
        if (jobCount < 10) {
            loadMoreButton.style.display = 'none'; // Hide button if fewer than 10 jobs were loaded
        } else {
            loadMoreButton.style.display = 'block'; // Show button for more jobs
        }
    }

    // Event listener for "Load More" button
    loadMoreButton.addEventListener('click', function () {
        fetchJobs(currentPage + 1);
    });

    // Initial fetch on page load
    fetchJobs();
});
