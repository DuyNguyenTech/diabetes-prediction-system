document.getElementById('healthForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const btn = document.getElementById('analyzeBtn');
    const btnText = btn.querySelector('.btn-text');
    const loader = document.getElementById('btnLoader');
    
    btn.disabled = true;
    btnText.style.display = 'none';
    loader.style.display = 'block';

    //thu thap du lieu tu form
    const data = {
        gender: document.getElementById('gender').value,
        age: parseInt(document.getElementById('age').value),
        hypertension: 0, 
        heart_disease: 0, 
        smoking_history: document.getElementById('smoking_history').value,
        bmi: parseFloat(document.getElementById('bmi').value),
        HbA1c_level: parseFloat(document.getElementById('hba1c').value),
        blood_glucose_level: parseInt(document.getElementById('blood_glucose').value)
    };

    try {
        //gui yeu cau den server
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Lỗi server: ${response.status}`);
        }

        const result = await response.json();
        
        //gia lap do tre
        setTimeout(() => {
            renderResult(result);
            resetButton();
        }, 800);

    } catch (error) {
        console.error("Lỗi:", error);
        alert("Không thể kết nối với hệ thống AI. Vui lòng kiểm tra Docker!");
        resetButton();
    }

    function resetButton() {
        btn.disabled = false;
        btnText.style.display = 'block';
        loader.style.display = 'none';
    }
});

let myChart = null;

function renderResult(result) {
    document.getElementById('initialState').classList.add('hidden');
    document.getElementById('resultState').classList.remove('hidden');

    const prob = (result.probability * 100).toFixed(1);
    const isDanger = result.prediction === 1;
    
    //cap nhat text
    document.getElementById('percentText').innerText = `${prob}%`;
    document.getElementById('percentText').style.color = isDanger ? '#ef4444' : '#10b981';
    
    const card = document.getElementById('diagnosisCard');
    const title = document.getElementById('riskLabel');
    const desc = document.getElementById('riskDescription');

    card.className = `diagnosis-card ${isDanger ? 'danger' : 'safe'}`;
    
    if (isDanger) {
        title.innerText = "CẢNH BÁO: NGUY CƠ CAO";
        title.style.color = "#ef4444";
        desc.innerText = "Chỉ số phân tích vượt ngưỡng an toàn (0.37). AI khuyến nghị thực hiện xét nghiệm chuyên sâu.";
    } else {
        title.innerText = "AN TOÀN: NGUY CƠ THẤP";
        title.style.color = "#10b981";
        desc.innerText = "Các chỉ số nằm trong vùng kiểm soát. Hãy duy trì lối sống lành mạnh và tập luyện.";
    }

    //ve bieu do
    const ctx = document.getElementById('riskChart').getContext('2d');
    if (myChart) myChart.destroy();

    myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Nguy cơ', 'An toàn'],
            datasets: [{
                data: [prob, 100 - prob],
                backgroundColor: [
                    isDanger ? '#ef4444' : '#10b981',
                    '#e2e8f0'
                ],
                borderWidth: 0,
                cutout: '85%',
                borderRadius: 20
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: { enabled: false } },
            animation: { animateScale: true, animateRotate: true }
        }
    });
}