document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById("user_input");
    input.focus();

    input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            this.form.submit();
        }
    });
});


// console.log("✅1 script.js loaded!");

// document.addEventListener("DOMContentLoaded", function () {
//     console.log("✅ script.js loaded!");

//     const menuToggle = document.getElementById("menu-toggle");
//     const navigation = document.getElementById("navigation");

//     if (menuToggle && navigation) {
//         menuToggle.addEventListener("click", function () {
//             navigation.classList.toggle("show");
//         });

//         document.addEventListener("click", function (event) {
//             if (!navigation.contains(event.target) && event.target !== menuToggle) {
//                 navigation.classList.remove("show");
//             }
//         });
//     }
// });

document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.getElementById("menu-toggle");
  const navigation = document.getElementById("navigation");
  const dropdownBtn = document.querySelector(".dropbtn");
  const dropdown = document.querySelector(".dropdown");

  // เปิด/ปิดเมนูหลัก
  menuToggle.addEventListener("click", function () {
    navigation.classList.toggle("show");
  });

  // เปิด/ปิดเมนูย่อย Game
  dropdownBtn.addEventListener("click", function (e) {
    e.preventDefault();
    dropdown.classList.toggle("active");
  });

  // ปิดเมนูหลักเมื่อคลิกข้างนอก (มือถือ)
  document.addEventListener("click", function (e) {
    if (!navigation.contains(e.target) && e.target !== menuToggle) {
      navigation.classList.remove("show");
      dropdown.classList.remove("active");
    }
  });
});

window.onload = function () {
        const input = document.getElementById('user_input');
        if (input) {
            input.focus();
        }
    }







