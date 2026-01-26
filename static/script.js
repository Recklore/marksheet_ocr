document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resetBtn = document.getElementById('resetBtn');
    const loader = document.getElementById('loader');
    
    // Result elements
    const emptyState = document.getElementById('emptyState');
    const resultContent = document.getElementById('resultContent');
    const candidateGrid = document.getElementById('candidateGrid');
    const marksTableBody = document.getElementById('marksTableBody');
    const toggleJsonBtn = document.getElementById('toggleJsonBtn');
    const rawJson = document.getElementById('rawJson');

    // --- Event Listeners ---

    // 1. File Upload Logic
    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) handleFile(e.target.files[0]);
    });

    // Drag & Drop
    dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
    });

    function handleFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            dropZone.classList.add('hidden');
            previewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }

    // 2. Reset Logic
    resetBtn.addEventListener('click', () => {
        fileInput.value = '';
        dropZone.classList.remove('hidden');
        previewContainer.classList.add('hidden');
        resultContent.classList.add('hidden');
        emptyState.classList.remove('hidden');
    });

    // 3. Analyze Logic (Call Backend)
    analyzeBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) return;

        // UI: Loading State
        analyzeBtn.disabled = true;
        loader.classList.remove('hidden');
        emptyState.classList.add('hidden');
        resultContent.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Failed to analyze');

            const data = await response.json();
            renderResults(data);

        } catch (error) {
            alert("Error: " + error.message);
            emptyState.classList.remove('hidden');
        } finally {
            analyzeBtn.disabled = false;
            loader.classList.add('hidden');
        }
    });

    // 4. Render Logic
    function renderResults(data) {
        resultContent.classList.remove('hidden');

        // A. Candidate Info
        candidateGrid.innerHTML = '';
        // Helper to safely get value or default
        const getVal = (field) => field?.value || '-';
        
        const details = [
            { label: 'Name', value: getVal(data.candidate.name) },
            { label: 'Roll No', value: getVal(data.candidate.roll_no) },
            { label: 'Board', value: getVal(data.candidate.board_university) },
            { label: 'Result', value: getVal(data.result_summary.overall_result) }
        ];

        details.forEach(d => {
            const div = document.createElement('div');
            div.className = 'detail-item';
            div.innerHTML = `<span class="detail-label">${d.label}</span><span class="detail-value">${d.value}</span>`;
            candidateGrid.appendChild(div);
        });

        // B. Marks Table
        marksTableBody.innerHTML = '';
        data.subjects.forEach(sub => {
            const tr = document.createElement('tr');
            const conf = (sub.obtained_marks.confidence * 100).toFixed(0);
            
            // Color code low confidence
            const confColor = conf < 70 ? 'red' : 'green';

            tr.innerHTML = `
                <td>${getVal(sub.subject_name)}</td>
                <td>${getVal(sub.obtained_marks)}</td>
                <td>${getVal(sub.max_marks)}</td>
                <td style="color:${confColor}; font-weight:bold;">${conf}%</td>
            `;
            marksTableBody.appendChild(tr);
        });

        // C. Raw JSON
        rawJson.textContent = JSON.stringify(data, null, 2);
    }

    // 5. Toggle JSON
    toggleJsonBtn.addEventListener('click', () => {
        rawJson.classList.toggle('hidden');
    });
});