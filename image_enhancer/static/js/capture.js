document.getElementById('capture_btn').addEventListener('click', function() {
    var video = document.getElementById('video_feed');
    var canvas = document.createElement('canvas');
    canvas.width = video.width;
    canvas.height = video.height;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    var dataURL = canvas.toDataURL('image/jpeg');

    // AJAX 요청으로 서버에 이미지 데이터 전송
    fetch('/capture', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({image: dataURL}),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
});
