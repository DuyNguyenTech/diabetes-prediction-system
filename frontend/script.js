let myChart = null;

//xu ly khi bam phan tich
document.getElementById('diagnosisForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const btn = document.getElementById('submitBtn');
    const originalBtnHtml = btn.innerHTML;
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Đang phân tích...';

    const data = {
        gender: document.getElementById('gender').value,
        age: parseInt(document.getElementById('age').value),
        hypertension: parseInt(document.getElementById('hypertension').value), 
        heart_disease: parseInt(document.getElementById('heart_disease').value), 
        smoking_history: document.getElementById('smoking_history').value,
        bmi: parseFloat(document.getElementById('bmi').value),
        HbA1c_level: parseFloat(document.getElementById('HbA1c_level').value),
        blood_glucose_level: parseInt(document.getElementById('blood_glucose_level').value)
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Lỗi Server (${response.status}): ${errorText}`);
        }

        const result = await response.json();
        
        await new Promise(resolve => setTimeout(resolve, 500));
        renderResult(result);

    } catch (error) {
        console.error("Lỗi chi tiết:", error);
        alert('⚠️ Đã có lỗi xảy ra!\n\nChi tiết: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalBtnHtml;
    }
});

//lam moi
document.getElementById('resetBtn').addEventListener('click', function() {
    //xoa ket qua va hien thi lai form
    document.getElementById('diagnosisForm').reset();
    
    //an ket qua va hien thi lai form
    document.getElementById('resultState').classList.add('d-none');
    document.getElementById('initialState').classList.remove('d-none');
    
    //huy bieu do neu co
    if (myChart) {
        myChart.destroy();
        myChart = null;
    }
});

//xu ly khi bam vao tieu de chinh de lam moi trang
document.getElementById('mainTitle').addEventListener('click', function() {
    //goi su kien click cua nut reset de lam moi trang
    document.getElementById('resetBtn').click();
    
    //hieu ung nhan nut
    this.style.opacity = '0.5';
    setTimeout(() => {
        this.style.opacity = '1';
    }, 150);
});

//hien thi ket qua va bieu do
function renderResult(result) {
    document.getElementById('initialState').classList.add('d-none');
    document.getElementById('resultState').classList.remove('d-none');

    const prob = (result.probability * 100).toFixed(1);
    const isDanger = result.prediction === 1;
    
    const textEl = document.getElementById('resultText');
    const descEl = document.getElementById('resultDesc');
    const percentEl = document.getElementById('percentText');

    percentEl.innerText = `${prob}%`;

    if (isDanger) {
        textEl.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>CẢNH BÁO NGUY CƠ CAO';
        textEl.className = "fw-bold mb-2 text-danger text-uppercase";
        descEl.innerText = "Chỉ số phân tích vượt ngưỡng an toàn. Khuyến nghị thực hiện xét nghiệm chuyên sâu.";
        percentEl.style.color = "#dc3545"; 
    } else {
        textEl.innerHTML = '<i class="fas fa-shield-alt me-2"></i>KẾT QUẢ AN TOÀN';
        textEl.className = "fw-bold mb-2 text-success text-uppercase";
        descEl.innerText = "Các chỉ số hiện tại nằm trong vùng an toàn. Tiếp tục duy trì lối sống lành mạnh.";
        percentEl.style.color = "#198754"; 
    }

    const ctx = document.getElementById('riskChart').getContext('2d');
    if (myChart) myChart.destroy();

    myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Nguy cơ', 'An toàn'],
            datasets: [{
                data: [prob, 100 - prob],
                backgroundColor: [
                    isDanger ? '#dc3545' : '#198754', 
                    '#e9ecef'
                ],
                borderWidth: 0,
                cutout: '85%',
                borderRadius: 30
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { tooltip: { enabled: false }, legend: { display: false } },
            animation: { animateScale: true, animateRotate: true, duration: 1000 }
        }
    });
}