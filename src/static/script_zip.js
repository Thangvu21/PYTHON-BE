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
        const download_btn = document.createElement('a');
        download_btn.href = path
        download_btn.textContent = 'Tải file zip'
        download_btn.className = 'button btn-success'
        download_btn.download = ''
        container.appendChild(download_btn)
    })

})