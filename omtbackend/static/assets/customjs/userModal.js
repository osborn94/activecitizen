// document.addEventListener("DOMContentLoaded", function () {
//     const viewButtons = document.querySelectorAll(".view-user-btn");

//     viewButtons.forEach(button => {
//       button.addEventListener("click", function () {
//         const userId = this.dataset.userId;

//         fetch(`/get-user/${userId}/`)
//           .then(response => response.json())
//           .then(data => {
//             document.getElementById("modal-user-image").src = data.profile_image;
//             document.getElementById("modal-user-name").textContent = data.full_name;
//             document.getElementById("modal-user-status").textContent = data.status;
//             document.getElementById("modal-user-id").textContent = "PU-" + data.id;
//             document.getElementById("modal-user-email").textContent = data.email;
//             document.getElementById("modal-user-phone").textContent = data.phone;
//             document.getElementById("modal-user-gender").textContent = data.gender;
//             document.getElementById("modal-user-dob").textContent = data.dob;
//             document.getElementById("modal-user-role").textContent = data.role;
//             document.getElementById("modal-user-state").textContent = data.state;
//             document.getElementById("modal-user-lga").textContent = data.lga;
//             document.getElementById("modal-user-ward").textContent = data.ward;
//             document.getElementById("modal-user-punit").textContent = data.polling_unit;
//           })
//           .catch(error => {
//             console.error("Error fetching user data:", error);
//           });
//       });
//     });
//   });
