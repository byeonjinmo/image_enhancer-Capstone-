document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector("form");
    var loader = document.getElementById("loading");

    function previewImage() {
        var preview = document.getElementById('image_preview');
        var file = document.getElementById('original_image').files[0];
        var reader = new FileReader();

        reader.onloadend = function () {
            preview.src = reader.result;
            preview.style.display = 'block';
        };

        if (file) {
            reader.readAsDataURL(file);
        } else {
            preview.src = "";
            preview.style.display = 'none';
        }
    }

    form.onsubmit = function (event) {
        event.preventDefault(); // 폼 기본 제출 방지
        loader.style.display = "flex"; // 로딩 애니메이션 표시

        var formData = new FormData(form); // 폼 데이터 수집
        fetch('/enhancer/upload/', { // 서버 엔드포인트로 POST 요청
            method: 'POST',
            body: formData,
        })
            .then(function (response) {
                return response.json(); // 응답을 JSON으로 변환
            })
            .then(function (data) {
                console.log(data); // 서버로부터 받은 데이터 처리
                // 예: 처리된 이미지 페이지로 리디렉션
                window.location.href = `/enhancer/results/${data.image_id}/`;
            })
            .catch(function (error) {
                console.error('Error:', error); // 에러 처리
            })
            .finally(function () {
                loader.style.display = "none"; // 로딩 애니메이션 숨김
            });
    };
});
