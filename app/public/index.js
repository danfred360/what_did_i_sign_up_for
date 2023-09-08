const form = document.querySelector('form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const id = document.querySelector('#id').value;
    const title = document.querySelector('#title').value;
    const description = document.querySelector('#description').value;
    const token = document.querySelector('#token').value;
    const responseContainer = document.querySelector('#response-container');

    const data = {
        id,
        title,
        description,
    };

    try {
        const response = await fetch('/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Token': token,
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        console.log(result);
        responseContainer.innerHTML = `<div class="form_area">
        <div class="form_group">
            <p>Result: ${JSON.stringify(result)}<p> 
        </div>
        </div>`;
    } catch (error) {
        console.error('Error:', error);
    }
});