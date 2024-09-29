const $cupcakesUL = $('#cupcakes-list');
const $form = $('.add-cupcake-form');
const baseUrl = '/api/cupcakes';

// Event handler for form submission
$form.on('submit', async function (evt) {
    await addNewCupcake(evt);
});

// When the document is ready, load the list of cupcakes
$(document).ready(async function () {
    await showCupcakesList();
});

/**
 * Fetches the list of cupcakes from the server and displays them
 */
async function showCupcakesList() {
    try {
        const response = await axios.get(baseUrl);
        const cupcakes = response.data.cupcakes;

        // Prepend each cupcake to the list
        cupcakes.forEach(cupcake => {
            const $cupcakeLI = createCupcakeListItem(cupcake);
            $cupcakesUL.prepend($cupcakeLI);
        });
    } catch (error) {
        console.error("Error fetching cupcakes:", error);
        alert("Failed to load cupcakes.");
    }
}

/**
 * Handles the form submission to add a new cupcake
 */
async function addNewCupcake(evt) {
    evt.preventDefault();

    try {
        // Send a POST request to the API to add a new cupcake
        const postResp = await axios.post(baseUrl, {
            flavor: $('#flavor').val(),
            size: $('#size').val(),
            rating: $('#rating').val(),
            image: $('#image').val()
        });

        // Get the new cupcake data from API
        const newCupcakeID = postResp.data.cupcake.id;
        const getResp = await axios.get(`${baseUrl}/${newCupcakeID}`);
        const newCupcake = getResp.data.cupcake;

        // Prepend the new cupcake to the list
        const $newCupcakeLI = createCupcakeListItem(newCupcake);
        $cupcakesUL.prepend($newCupcakeLI);

        // Clear the form after submission
        $form[0].reset();
    } catch (error) {
        console.error("Error adding cupcake:", error);
        alert("Failed to add cupcake. Please try again.");
    }
}

async function updateCupcake(evt) {
    evt.preventDefault();
    // Get the cupcake ID from the cupcake list element's 'data-id' attribute
    const cupcake_id = $(this).parent().data('id');

    // Select the update cupcake form within the list element
    const $form = $(this).parent().find('form')

    try {
        // Send a PATCH request to the API to update a cupcake
        const patchResp = await axios.patch(`${baseUrl}/${cupcake_id}`, {
            flavor: $form.find("[name='flavor']").val(),
            size: $form.find("[name='size']").val(),
            rating: $form.find("[name='rating']").val(),
            image: $form.find("[name='image']").val()
        });

        // Extract the updated cupcake data 
        const updatedCupcake = patchResp.data.cupcake;

        // Update and display the new cupcake data
        $(this).parent().find('img').attr('src', updatedCupcake.image);
        $(this).parent().find('.flavor').text(updatedCupcake.flavor);
        $(this).parent().find('.size').text(updatedCupcake.size);
        $(this).parent().find('.rating').text(updatedCupcake.rating);

    } catch (error) {
        console.error("Error updating cupcake cupcake:", error);

    }
}

async function deleteCupcake() {
    // Get the cupcake ID from the cupcake list element's 'data-id' attribute
    const cupcake_id = $(this).parent().data('id');

    try {
        // Send a DELETE request to remove the cupcake from the server
        const deleteResp = await axios.delete(`${baseUrl}/${cupcake_id}`);
        // Remove the cupcake from the DOM
        $(this).parent().remove();
    } catch (error) {
        console.error("Error deleting cupcake:", error);
    }
}

function createCupcakeListItem(cupcake) {
    // Select the cupcake template from the HTML, clone it so we can manipulate it
    const $template = $('#cupcake-template').contents().clone();

    // Set the 'data-id' attribute on the root <li> element to store the current cupcake's ID
    $template.filter('li').attr('data-id', cupcake.id);

    // Populate the template with cupcake details
    $template.find('img').attr('src', cupcake.image);
    $template.find('.flavor').text(cupcake.flavor);
    $template.find('.size').text(cupcake.size);
    $template.find('.rating').text(cupcake.rating);

    // Set the form input values for updating the cupcake with current data
    const $form = $template.find('form');
    $form.find("[name='image']").val(cupcake.image);
    $form.find("[name='flavor']").val(cupcake.flavor);
    $form.find("[name='size']").val(cupcake.size);
    $form.find("[name='rating']").val(cupcake.rating);

    // Attach event handler for updating the cupcake
    $form.on('submit', updateCupcake);

    // Attach event handler for deleting the cupcake
    $template.find('button').on('click', deleteCupcake);
    
    return $template;
}


