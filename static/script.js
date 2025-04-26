function jswalafuncttion(sent_title){
//    jo teen buttton hai english, hindi aur english waale uske click ka handle akrega
    fetch('/get_the_audios', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title: sent_title })
    })
    .then(response => response.json())
    .then(data => {
    // Verify that the data object contains the expected keys
        console.log(data);

    // Access the data using the correct keys
        var enValue = data.en;
        var frValue = data.fr;
        var geValue = data.ge;

    //Update button click handlers to trigger download
        document.querySelector('.english').onclick = function() {
            triggerDownload(enValue);
        };
        document.querySelector('.french').onclick = function() {
            triggerDownload(frValue);
        };
        document.querySelector('.german').onclick = function() {
            triggerDownload(geValue);
        };
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function triggerDownload(mp3FilePath) {
    fetch('/download_mp3', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mp3_file_path: mp3FilePath })
    })
    .then(response => {
        // Trigger download if needed
            return response.blob();
    })
    .then(blob => {
        download(blob)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


//// JavaScript function to handle audio download
//function offcanvas(title) {
//        var offcanvasTitle = document.getElementById('offcanvasExampleLabel');
//        offcanvasTitle.innerText = title;
//
////        call downloadMP3 function
//        jswalafuncttion(title);
//
//        var offcanvasElement = new bootstrap.Offcanvas(document.getElementById('offcanvasExample'));
//        offcanvasElement.show();
//    }

function modal(title) {
    var modalTitle = document.getElementById('exampleModalLabel');
    modalTitle.innerText = "Now, get an audio blog of "+title+"!";

    jswalafuncttion(title);

    var modalElement = new bootstrap.Modal(document.getElementById('exampleModal'))
    modalElement.show();

}

    // Add a click event listener to the logout button
document.getElementById('logoutButton').addEventListener('click', function() {
    // Redirect the user to the /login page
    window.location.href = '/login';
});



document.addEventListener("DOMContentLoaded", function() {
    var selectedButtons = [];
    var carousel = document.getElementById('related-blogs-carousel');
    var dropdownMenu = document.querySelector('.dropdown-menu');
    dropdownMenu.innerHTML = '';


    // Function to toggle selection and update selectedButtons array
    function toggleSelection(button) {
        var value = button.value;
        var index = selectedButtons.indexOf(value);

        if (index === -1) {
            // If button is not already selected, add it to selectedButtons array
            selectedButtons.push(value);
            button.classList.add("selected");
        } else {
            // If button is already selected, remove it from selectedButtons array
            selectedButtons.splice(index, 1);
            button.classList.remove("selected");
        }
    }

        // Function to handle starring content
    function starContent(button, dropdownMenu) {
                    // Clear previous dropdown menu items
        console.log("entered the loop");
        var h3Element = button.parentElement;
        var starIcon = button.querySelector('svg');
        h3Element.classList.toggle("starred"); // Toggle the class for styling
        starIcon.classList.toggle("starred"); // Toggle the class for changing color
        var starPath = starIcon.querySelector('path');
        var entry = button.parentElement.textContent.trim();
        console.log(entry);

        if (starIcon.classList.contains("starred")) {
            // If the star button is currently yellow (starred), add the dropdown item
              starPath.setAttribute("fill", "yellow");
            var dropdownItem = document.createElement('li');
            dropdownItem.innerHTML = `<button class="dropdown-item btn" onclick="modal('${entry}')">${entry}</button>`;
            dropdownMenu.appendChild(dropdownItem);

            console.log("Dropdown menu:", dropdownMenu);
            console.log("Dropdown menu parent element:", dropdownMenu.parentElement);

            if (dropdownMenu.parentElement){
                dropdownMenu.parentElement.classList.add('show');
            } else {
                console.error("Dropdown menu parent element is null.");
            }






        }
        else {
            console.log("else part")
            console.log("dropdownmenu", dropdownMenu)
            // If the star button is currently not yellow (starred), remove the dropdown item
            var dropdownItems = dropdownMenu.querySelectorAll('.dropdown-item');
            console.log(dropdownItems.firstChild)
            starPath.setAttribute("fill", "currentColor");
            dropdownItems.forEach(item => {
                if (item.textContent.trim() === entry) {

                    console.log(item)
                    item.remove();
                    console.log("new dropdown", dropdownMenu)
                    dropdownMenu.parentElement.classList.add('show');
                }
            });
        }
    }

    // Event listener for button clicks
    document.querySelectorAll('.item-button').forEach(button => {
        button.addEventListener('click', function() {
            toggleSelection(button);
        });
    });

    // Event listener for submit button
    document.getElementById('submit-button').addEventListener('click', function() {
        // Send selected button values to Flask route for matching
        fetch('/match_keywords', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selected_keywords: selectedButtons })
        })



        .then(response => response.json())
        .then(data => {

            console.log("Matched titles:", data.matched_entries);
            console.log("Description of blogs:", data.desc_title);
            console.log("image url is:", data.image_url);

            // Clear previous carousel items
            var carouselInner = carousel.querySelector('.carousel-inner');
            carouselInner.innerHTML = '';
            // Add new carousel items
            data.matched_entries.forEach((entry, index) => {
                console.log(entry)
                var isActive = index === 0 ? 'active' : ''; // Set first item as active
                var item = `
                    <div class="carousel-item ${isActive} transbox">
                        <h3>${entry} <button class="star-button btn btn-bg btn-secondary" style="vertical-align: baseline;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#D3D3D3" class="bi bi-star-fill" viewBox="0 0 16 16"   style="vertical-align: baseline;">
                        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                        </svg></button></h3>
                        <img src="static/${data.image_url[index]}" class="rounded mx-auto d-block" alt="Blog Image">
                        <p>${data.desc_title[index]}</p>
                    </div>
                `;
                carouselInner.innerHTML += item;
            });

            // Show the carousel after data is loaded
            carousel.classList.remove('d-none');

            // Event listener for star buttons
            document.querySelectorAll('.star-button').forEach(button => {
                console.log("hi");
                button.addEventListener('click', function() {
                    starContent(button,dropdownMenu);
                });
            });
        })


        .catch(error => console.error('Error:', error));
    });



});
