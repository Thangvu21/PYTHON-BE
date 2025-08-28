const form = document.getElementById("time-form")
const image_block = document.querySelector('.container');

form.addEventListener("submit", function (e) {
    e.preventDefault()
    const start_time = this.start_time.value
    const end_time = this.end_time.value

    fetch(`${window.location.origin}/api/image/image_for_time/`, {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'

        },
        method: "POST",
        body: JSON.stringify({
            "start_time": start_time,
            "end_time": end_time
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json()
    }).then(data => {
        const images = data;
        if (!Array.isArray(images)) {
            throw new Error('Invalid data format');
        }
        return images;
    }).then(images => {
        if (images.length === 0) {
            const message = document.createElement('p');
            message.textContent = 'No images available';
            image_block.appendChild(message);
            return;
        }
        const image_blocks = images.map(src => {
            const img = document.createElement('img');
            img.src = src.url;
            img.alt = 'Image';
            img.className = 'image-item';
            return img;
        });
        image_block.append(...image_blocks);
    })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });

})