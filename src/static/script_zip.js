const form = document.getElementById("time-form")
const container = document.querySelector('.container')

form.addEventListener('submit', (e) => {
    e.preventDefault()

    const start_time = this.start_time.value
    const end_time = this.end_time.value

    fetch('http://127.0.0.1:8000/api/down_load_zip/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            "start_time": start_time,
            "end_time": end_time
        })
    }).then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json()
    }).then((data) => {
        const path = data
        if (path == '') {
            throw new Error('Đường dẫn rỗng')
        }
        return path
    }).then((path) => {
        console.log(path)
        const download_btn = document.createElement('a');
        download_btn.href = path
        download_btn.textContent = 'Tải file zip';
        
        download_btn.className = 'btn btn-success mt-2';
        download_btn.download = '';
        download_btn.id = 'download-zip-btn';
        download_btn.style.display = 'inline-block';
        download_btn.style.fontWeight = 'bold';
        download_btn.style.fontSize = '1.1rem';
        download_btn.style.marginTop = '10px';
        download_btn.style.padding = '10px 24px';
        download_btn.style.borderRadius = '6px';
        download_btn.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
        download_btn.style.transition = 'background 0.2s';

        download_btn.onmouseover = () => {
            download_btn.style.background = '#218838';
            download_btn.style.color = '#fff'
        };
        download_btn.onmouseout = () => {
            download_btn.style.background = '';
            download_btn.style.color = '';
        };
        
        container.style.textAlign = 'center';

        container.appendChild(download_btn)
    })

})