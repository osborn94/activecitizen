 // Here is the Function to fetch JSON data from file
 async function fetchJSON() {
    const response = await fetch('/qubes/light/assets/js/data.json');
    const data = await response.json();
    return data;
  }

  // Function to populate states dropdown
  async function populateStates() {
    const data = await fetchJSON();
    const stateSelect = document.getElementById('stateSelect');
    stateSelect.innerHTML = '<option value="">Select State</option>';

    data.forEach(stateObj => {
      const option = document.createElement('option');
      option.value = stateObj.state;
      option.textContent = stateObj.state.toUpperCase();
      stateSelect.appendChild(option);
    });
  }

  // Function to populate LGAs dropdown based on selected state
  async function populateLGAs() {
    const data = await fetchJSON();
    const stateSelect = document.getElementById('stateSelect');
    const lgaSelect = document.getElementById('lgaSelect');
    const wardSelect = document.getElementById('wardSelect');
    const pollingUnitSelect = document.getElementById('pollingUnitSelect');
    
    const selectedState = stateSelect.value;
    const stateObj = data.find(obj => obj.state === selectedState);
    
    lgaSelect.innerHTML = '<option value="">Select LGA</option>';
    wardSelect.innerHTML = '<option value="">Select Ward</option>';
    pollingUnitSelect.innerHTML = '<option value="">Select Polling Unit</option>';
    
    if (stateObj) {
      stateObj.lgas.forEach(lgaObj => {
        const option = document.createElement('option');
        option.value = lgaObj.lga;
        option.textContent = lgaObj.lga.toUpperCase();
        lgaSelect.appendChild(option);
      });
    }
  }

  // Function to populate wards dropdown based on selected LGA
  async function populateWards() {
    const data = await fetchJSON();
    const stateSelect = document.getElementById('stateSelect');
    const lgaSelect = document.getElementById('lgaSelect');
    const wardSelect = document.getElementById('wardSelect');
    const pollingUnitSelect = document.getElementById('pollingUnitSelect');

    const selectedState = stateSelect.value;
    const selectedLGA = lgaSelect.value;
    const stateObj = data.find(obj => obj.state === selectedState);
    
    wardSelect.innerHTML = '<option value="">Select Ward</option>';
    pollingUnitSelect.innerHTML = '<option value="">Select Polling Unit</option>';
    
    if (stateObj) {
      const lgaObj = stateObj.lgas.find(obj => obj.lga === selectedLGA);
      if (lgaObj) {
        lgaObj.wards.forEach(wardObj => {
          const option = document.createElement('option');
          option.value = wardObj.ward;
          option.textContent = wardObj.ward.toUpperCase();
          wardSelect.appendChild(option);
        });
      }
    }
  }

  // Function to populate polling units dropdown based on selected ward
  async function populatePollingUnits() {
    const data = await fetchJSON();
    const stateSelect = document.getElementById('stateSelect');
    const lgaSelect = document.getElementById('lgaSelect');
    const wardSelect = document.getElementById('wardSelect');
    const pollingUnitSelect = document.getElementById('pollingUnitSelect');

    const selectedState = stateSelect.value;
    const selectedLGA = lgaSelect.value;
    const selectedWard = wardSelect.value;
    const stateObj = data.find(obj => obj.state === selectedState);
    
    pollingUnitSelect.innerHTML = '<option value="">Select Polling Unit</option>';
    
    if (stateObj) {
      const lgaObj = stateObj.lgas.find(obj => obj.lga === selectedLGA);
      if (lgaObj) {
        const wardObj = lgaObj.wards.find(obj => obj.ward === selectedWard);
        if (wardObj) {
          wardObj.polling_units.forEach(unit => {
            const option = document.createElement('option');
            option.value = unit;
            option.textContent = unit.toUpperCase();
            pollingUnitSelect.appendChild(option);
          });
        }
      }
    }
  }

  // Populate states dropdown on page load
  populateStates();