/**
 * Thai Text Cleaner - Frontend JavaScript
 * Handles form interaction, API status check, and dynamic UI updates
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('cleanseForm');
    const input = document.getElementById('thaiTextInput');
    const charCount = document.getElementById('charCount');
    const submitBtn = document.getElementById('submitBtn');
    const clearBtn = document.getElementById('clearBtn');
    
    // Status & Alert elements
    const apiKeyBadge = document.getElementById('apiKeyBadge');
    const apiKeyAlert = document.getElementById('apiKeyAlert');
    const loadingSection = document.getElementById('loadingSection');
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    const errorDetails = document.getElementById('errorDetails');
    
    // Results elements
    const resultSection = document.getElementById('resultSection');
    const originalText = document.getElementById('originalText');
    const cleansedText = document.getElementById('cleansedText');
    const originalCharCount = document.getElementById('originalCharCount');
    const cleansedCharCount = document.getElementById('cleansedCharCount');
    
    // Toast
    const toast = document.getElementById('toastNotification');
    const toastMessage = document.getElementById('toastMessage');

    // 1. Initial Status Check
    checkServerStatus();

    // 2. Character Counter
    input.addEventListener('input', () => {
        updateCharCount();
    });

    function updateCharCount() {
        const length = input.value.length;
        charCount.textContent = length.toLocaleString('th-TH');
    }

    // 3. Sample Text Pills
    document.querySelectorAll('.btn-pill').forEach(btn => {
        btn.addEventListener('click', () => {
            const sampleText = btn.getAttribute('data-sample');
            if (sampleText) {
                input.value = sampleText;
                updateCharCount();
                input.focus();
            }
        });
    });

    // 4. Clear Button
    clearBtn.addEventListener('click', () => {
        input.value = '';
        updateCharCount();
        hideError();
        resultSection.classList.add('d-none');
        input.focus();
    });

    // 5. Form Submission (Cleanse Text)
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const rawText = input.value.trim();
        if (!rawText) {
            showError('กรุณากรอกข้อความภาษาไทยก่อนกดปุ่มแก้ไข');
            input.focus();
            return;
        }

        // Set Loading State
        setLoading(true);
        hideError();
        resultSection.classList.add('d-none');

        try {
            const response = await fetch('/api/clean', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: rawText })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                const message = data.error || `เกิดข้อผิดพลาดในการเรียก API (รหัส ${response.status})`;
                let detailsText = '';
                if (data.details) {
                    if (typeof data.details === 'object') {
                        detailsText = JSON.stringify(data.details, null, 2);
                    } else {
                        detailsText = String(data.details);
                    }
                }
                showError(message, detailsText);
                return;
            }

            // Display Results
            displayResults(data.original_text, data.cleansing_text);

        } catch (err) {
            showError(
                'ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ Backend ได้',
                err.message || 'โปรดตรวจสอบว่าเซิร์ฟเวอร์ Flask กำลังทำงานอยู่'
            );
        } finally {
            setLoading(false);
        }
    });

    // 6. Copy Buttons
    document.querySelectorAll('.btn-copy').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            if (!targetElement) return;

            const textToCopy = targetElement.textContent || '';
            if (!textToCopy) return;

            navigator.clipboard.writeText(textToCopy).then(() => {
                showToast('คัดลอกข้อความสำเร็จแล้ว');
                const origIcon = btn.innerHTML;
                btn.innerHTML = '<i class="fa-solid fa-check"></i> <span>คัดลอกแล้ว</span>';
                btn.style.color = '#059669';
                btn.style.borderColor = '#10b981';
                setTimeout(() => {
                    btn.innerHTML = origIcon;
                    btn.style.color = '';
                    btn.style.borderColor = '';
                }, 2000);
            }).catch(() => {
                // Fallback for older browsers
                const textarea = document.createElement('textarea');
                textarea.value = textToCopy;
                document.body.appendChild(textarea);
                textarea.select();
                try {
                    document.execCommand('copy');
                    showToast('คัดลอกข้อความสำเร็จแล้ว');
                } catch {
                    showToast('ไม่สามารถคัดลอกได้โดยอัตโนมัติ');
                }
                document.body.removeChild(textarea);
            });
        });
    });

    // Helpers
    async function checkServerStatus() {
        try {
            const res = await fetch('/api/status');
            if (res.ok) {
                const data = await res.json();
                if (data.api_key_configured) {
                    apiKeyBadge.className = 'badge badge-success';
                    apiKeyBadge.innerHTML = '<i class="fa-solid fa-circle-check"></i> API Key พร้อมใช้งาน';
                    apiKeyAlert.classList.add('d-none');
                } else {
                    apiKeyBadge.className = 'badge badge-warning';
                    apiKeyBadge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> ยังไม่ตั้งค่า API Key';
                    apiKeyAlert.classList.remove('d-none');
                }
            } else {
                apiKeyBadge.className = 'badge badge-warning';
                apiKeyBadge.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> ไม่สามารถตรวจสถานะได้';
            }
        } catch {
            apiKeyBadge.className = 'badge badge-warning';
            apiKeyBadge.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> ออฟไลน์';
        }
    }

    function setLoading(isLoading) {
        if (isLoading) {
            loadingSection.classList.remove('d-none');
            submitBtn.disabled = true;
            clearBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> กำลังประมวลผล...';
        } else {
            loadingSection.classList.add('d-none');
            submitBtn.disabled = false;
            clearBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> แก้ไขข้อความ';
        }
    }

    function displayResults(orig, cleansed) {
        originalText.textContent = orig || '';
        cleansedText.textContent = cleansed || '';
        
        originalCharCount.textContent = `${(orig || '').length.toLocaleString('th-TH')} ตัวอักษร`;
        cleansedCharCount.textContent = `${(cleansed || '').length.toLocaleString('th-TH')} ตัวอักษร`;

        resultSection.classList.remove('d-none');
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function showError(msg, details = '') {
        errorMessage.textContent = msg;
        if (details) {
            errorDetails.textContent = details;
            errorDetails.classList.remove('d-none');
        } else {
            errorDetails.classList.add('d-none');
            errorDetails.textContent = '';
        }
        errorSection.classList.remove('d-none');
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    function hideError() {
        errorSection.classList.add('d-none');
        errorMessage.textContent = '';
        errorDetails.textContent = '';
    }

    let toastTimeout;
    function showToast(msg) {
        if (toastTimeout) clearTimeout(toastTimeout);
        toastMessage.textContent = msg;
        toast.classList.remove('d-none');
        toastTimeout = setTimeout(() => {
            toast.classList.add('d-none');
        }, 2500);
    }
});
