<script>
window.foo = function(firstName, lastName, email, phone){
   var form_data = {access_code: "EXPERIENCE", email: email, first_name:firstName, last_name: lastName, phone_number: phone};
  namecoach.widget.initModalForm("#initiate-call", form_data,
    function(response) {
      console.log('The call has been successfully made');
      console.log(response);
    }, function(response, code) {
      console.log('Failed to make the call');
      console.log(response);
      console.log(code);
      
      // Create and show error modal
      showErrorModal(response, code);
    })
}

// Function to show error modal
function showErrorModal(response, errorCode) {
  // Create modal elements
  const modalBackdrop = document.createElement('div');
  modalBackdrop.className = 'modal-backdrop';
  modalBackdrop.style.position = 'fixed';
  modalBackdrop.style.top = '0';
  modalBackdrop.style.left = '0';
  modalBackdrop.style.width = '100%';
  modalBackdrop.style.height = '100%';
  modalBackdrop.style.backgroundColor = 'rgba(0,0,0,0.5)';
  modalBackdrop.style.zIndex = '1050';
  
  const modalDialog = document.createElement('div');
  modalDialog.className = 'modal-dialog';
  modalDialog.style.position = 'fixed';
  modalDialog.style.top = '50%';
  modalDialog.style.left = '50%';
  modalDialog.style.transform = 'translate(-50%, -50%)';
  modalDialog.style.maxWidth = '500px';
  modalDialog.style.width = '90%';
  modalDialog.style.backgroundColor = 'white';
  modalDialog.style.borderRadius = '10px';
  modalDialog.style.padding = '20px';
  modalDialog.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
  modalDialog.style.zIndex = '1051';
  
    // Check for specific error messages
  if (response && typeof response === 'object' && response.message === "The email already used") {
    errorMessage = "Voice recording already saved for this account. Thank you!.";
    hideRetrySuggestion = true;
  } else if (errorCode === 405) {
    errorMessage = "Voice recording already saved for this account. Thank you!";
    hideRetrySuggestion = true;
  } else if (errorCode) {
    errorMessage += ` (Error code: ${errorCode})`;
  }
  
  modalDialog.innerHTML = `
    <div class="modal-header" style="border-bottom: 1px solid #dee2e6; padding-bottom: 15px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
      <button type="button" class="close-modal" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; padding: 0; margin-right: 15px;">&times;</button>
      <h3 style="margin: 0; color: #0d6efd; flex-grow: 1;">Notification</h3>
    </div>
    <div class="modal-body" style="margin-bottom: 20px;">
      <p>${errorMessage}</p>
      ${!hideRetrySuggestion ? '<p>Please try again later or contact support for assistance.</p>' : ''}
    </div>
    <div class="modal-footer" style="text-align: right;">
      <button type="button" class="btn-record close-modal" style="background-color: #0d6efd; color: white; padding: 8px 20px; border-radius: 30px; border: none; cursor: pointer;">Close</button>
    </div>
  `;
  
  // Add to DOM
  document.body.appendChild(modalBackdrop);
  document.body.appendChild(modalDialog);
  
  // Handle closing modal
  const closeButtons = document.querySelectorAll('.close-modal');
  closeButtons.forEach(button => {
    button.addEventListener('click', function() {
      document.body.removeChild(modalBackdrop);
      document.body.removeChild(modalDialog);
    });
  });
  
  // Close modal when clicking on backdrop
  modalBackdrop.addEventListener('click', function() {
    document.body.removeChild(modalBackdrop);
    document.body.removeChild(modalDialog);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  // Change the selector if your "Record My Name" button has a different ID/class.
  var recordButton = document.querySelector("#initiate-call");
  if (recordButton) {
    recordButton.addEventListener("click", function() {
      // Use a delay to allow the modal to be rendered.
      setTimeout(function() {
        // Locate the modal container (assuming it has the class used by tingle modals)
        var modal = document.querySelector(".tingle-modal");
        if (modal) {
          // Find and enable the call button (with class "tingle-btn--primary")
          var callButton = modal.querySelector('.tingle-btn--primary');
          if (callButton) {
            callButton.disabled = false;
          }
          
          // Hide any widget row whose text contains "pronoun" (case-insensitive)
          modal.querySelectorAll('.widget-row').forEach(function(row) {
            if (row.textContent.toLowerCase().includes("pronoun")) {
              row.style.display = "none";
            }
          });
        }
      }, 100); // Adjust delay (in milliseconds) as needed for your modal render timing.
    });
  }
});
</script>