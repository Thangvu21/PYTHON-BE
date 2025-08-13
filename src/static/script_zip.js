const form = document.getElementById("time-form")
const container = document.querySelector('.container')

form.addEventListener('submit', (e) => {
    e.preventDefault()

    const start_time = this.start_time.value
    const end_time = this.end_time.value

    fetch('http://127.0.0.1:8000/api/down/down_load_zip', {
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
        const task_id = data.task_id;
        const zip_block = document.createElement('p');
        zip_block.textContent = "Đang tạo file zip, vui lòng chờ...";
        container.appendChild(zip_block);

        // Long polling function
        function pollStatus() {
            fetch(`http://127.0.0.1:8000/api/down/task_status?task_id=${task_id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(response => response.json())
                .then(statusData => {
                    if (statusData.status === "pending") {
                        zip_block.textContent = "Đang tạo file zip, vui lòng chờ...";
                        setTimeout(pollStatus, 1000); // Gọi lại sau 2s
                    } else if (statusData.status === "success") {
                        zip_block.textContent = "Tạo file zip thành công!";
                        const download_btn = document.createElement('a');
                        download_btn.href = statusData.download_url;
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
                        container.appendChild(download_btn);
                    } else if (statusData.status == "failure") {
                        zip_block.textContent = "Có lỗi xảy ra: " + statusData.error;
                    } else {
                        zip_block.textContent = "Trạng thái: " + statusData.status;
                        setTimeout(pollStatus, 2000);
                    }
                })
                .catch(err => {
                    zip_block.textContent = "Lỗi kết nối tới server!";
                });
        }
        pollStatus()
    })

})