document.addEventListener('DOMContentLoaded', async function() {
    const stateSelect = document.getElementById("stateSelect");
    const lgaSelect = document.getElementById("lgaSelect");
    const wardSelect = document.getElementById("wardSelect");
    const pollingUnitSelect = document.getElementById("pollingUnitSelect");

    // 1. Fetch the JSON file
    const response = await fetch(DATA_JSON_URL);
    const statesData = await response.json();

    // Populate the state dropdown
    statesData.forEach((state) => {
        const option = document.createElement("option");
        option.value = state.state; // Value is the state name
        option.textContent = state.state; // Text content is also the state name
        stateSelect.appendChild(option);
    });

    stateSelect.disabled = false;

    // 2. When a state is selected, populate the LGA dropdown
    stateSelect.addEventListener("change", function () {
        const selectedState = statesData.find(s => s.state === this.value);
        lgaSelect.innerHTML = '<option value="">Select LGA</option>';
        wardSelect.innerHTML = '<option value="">Select Ward</option>';
        pollingUnitSelect.innerHTML = '<option value="">Select Polling Unit</option>';
        wardSelect.disabled = true;
        pollingUnitSelect.disabled = true;

        if (selectedState) {
            selectedState.lgas.forEach(lga => {
                const option = document.createElement("option");
                option.value = lga.lga; // LGA name
                option.textContent = lga.lga; // LGA text content
                lgaSelect.appendChild(option);
            });
            lgaSelect.disabled = false;
        }
    });

    // 3. When an LGA is selected, populate the ward dropdown
    lgaSelect.addEventListener("change", function () {
        const selectedLga = statesData
            .find(state => state.state === stateSelect.value)
            .lgas
            .find(lga => lga.lga === this.value);

        wardSelect.innerHTML = '<option value="">Select Ward</option>';
        pollingUnitSelect.innerHTML = '<option value="">Select Polling Unit</option>';
        pollingUnitSelect.disabled = true;

        if (selectedLga) {
            selectedLga.wards.forEach(ward => {
                const option = document.createElement("option");
                option.value = ward.ward; // Ward name
                option.textContent = ward.ward; // Ward text content
                wardSelect.appendChild(option);
            });
            wardSelect.disabled = false;
        }
    });

    // 4. When a ward is selected, populate the polling unit dropdown
    wardSelect.addEventListener("change", function () {
        const selectedWard = statesData
            .find(state => state.state === stateSelect.value)
            .lgas
            .find(lga => lga.lga === lgaSelect.value)
            .wards
            .find(ward => ward.ward === this.value);

        pollingUnitSelect.innerHTML = '<option value="">Select Polling Unit</option>';

        if (selectedWard) {
            selectedWard.polling_units.forEach(pollingUnit => {
                const option = document.createElement("option");
                option.value = pollingUnit; // Polling unit name
                option.textContent = pollingUnit; // Polling unit text content
                pollingUnitSelect.appendChild(option);
            });
            pollingUnitSelect.disabled = false;
        }
    });
});




document.addEventListener('DOMContentLoaded', function() {
    let currentStep = 1;
    const totalSteps = 3;
    
    // Initialize form
    updateProgress();
    
    // Next step handler
    document.querySelectorAll('.next-step').forEach(button => {
        button.addEventListener('click', function() {
            const nextStep = parseInt(this.dataset.next);
            if (nextStep > currentStep && validateStep(currentStep)) {
                document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.remove('active');
                currentStep = nextStep;
                document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.add('active');
                updateProgress();
            }
        });
    });
    
    // Previous step handler
    document.querySelectorAll('.prev-step').forEach(button => {
        button.addEventListener('click', function() {
            const prevStep = parseInt(this.dataset.prev);
            document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.remove('active');
            currentStep = prevStep;
            document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.add('active');
            updateProgress();
        });
    });
    
    // Update progress bar
    function updateProgress() {
        document.querySelectorAll('.progress-step').forEach(step => {
            const stepNum = parseInt(step.dataset.step);
            step.classList.remove('active', 'completed');
            
            if (stepNum === currentStep) {
                step.classList.add('active');
            } else if (stepNum < currentStep) {
                step.classList.add('completed');
            }
        });
    }
    
    // Basic step validation
    function validateStep(step) {
        let isValid = true;
        const currentStepEl = document.querySelector(`.form-step[data-step="${step}"]`);
        
        // Check required fields in current step
        currentStepEl.querySelectorAll('[required]').forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
       
        
        return isValid;
    }
    
    // Image preview functionality
    const passportInput = document.getElementById('passport');
    const imagePreview = document.getElementById('imagePreview');
    const uploadLoader = document.getElementById('uploadLoader');
    const uploadProgress = document.getElementById('uploadProgress');
    
    passportInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            // Show loader
            uploadLoader.style.display = 'block';
            uploadProgress.style.width = '0%';
            
            // Simulate upload progress
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += 10;
                uploadProgress.style.width = `${progress}%`;
                
                if (progress >= 100) {
                    clearInterval(progressInterval);
                    uploadLoader.style.display = 'none';
                }
            }, 100);
            
            // Create image preview
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
            }
            reader.readAsDataURL(file);
        }
    });
    
    // You can keep your existing state/LGA/polling unit JavaScript logic here
});



console.log('hello')