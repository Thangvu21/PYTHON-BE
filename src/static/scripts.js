
const image_block = document.querySelector('.container');

let page_hientai = 0; // hoặc lấy từ input, query string, v.v.
const page_size = 20;
const url = `http://localhost:8000/api/l_images?page=${page_hientai}&page_size=${page_size}`;

fetch(url, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'

    },

}).then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
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

/**
 * Vì khi tải file js thì phần tử html chưa có xuất hiện các link vì chưa load dữ liệu xong, 
 * nếu gán sự cho rỗng thì không có sự kiện nào được gán
 *  */    

document.addEventListener('DOMContentLoaded', function () {
    // Lắng nghe click trên các link phân trang
    document.querySelectorAll('.pagination-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const params = new URLSearchParams(this.search || this.href.split('?')[1]);
            const page = params.get('page') || 0;
            const page_size = 20; // hoặc lấy từ input nếu muốn động

            document.getElementById("current-page").innerHTML = `Trang hiện tại: ${page}<br>`;

            // Gọi lại API với page mới
            fetch(`http://localhost:8000/api/l_images?page=${page}&page_size=${page_size}`)
                .then(response => response.json())
                .then(images => {
                    image_block.innerHTML = '';
                    if (!Array.isArray(images) || images.length === 0) {
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
                    console.error('Fetch error:', error);
                });
        });
    });
});
