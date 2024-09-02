
/* 
 ========= main JS documentation ==========================

 * theme name: HealthEase Dashboard
 * version: 1.0
 * description: Workplace Html5 Template
 * author: softivus
 * author url: 
    ==================================================
    side menu bar with local storage 
    sorting table data
    action icon show/hide 
    toggle filter box
    input file and show file name
    small device chat list toggle
    pre loader
    Current Year
*/

"use strict";
$(document).ready(function () {

  // side menu bar with local storage 
  let toggleMenu = document.getElementsByClassName('toggle-menu')
  let sidebar = document.getElementsByClassName('sidebar')
  let contentWrapper = document.getElementsByClassName('content-wrapper')
  let sidebarWrapper = document.getElementsByClassName('sidebar-wrapper')
  let sidebarMenu = document.querySelectorAll('.show-item')
  let hideSmallDeviceMenu = document.getElementById('hide-menubar')
  let smallMenu = localStorage.getItem('small-menu')

  function activeSmallMenu() {
    sidebar[0].classList.add('hide-sidebar');
    contentWrapper[0].classList.add('full-wrapper')
    sidebarWrapper[0].classList.add('px-0')
    sidebarMenu.forEach(item => item.classList.add('hide-item'))
    localStorage.setItem("small-menu", "enabled")
  }

  function activeBigMenu() {
    sidebar[0].classList.remove('hide-sidebar')
    contentWrapper[0].classList.remove('full-wrapper')
    sidebarWrapper[0].classList.remove('px-0')
    sidebarMenu.forEach(item => item.classList.remove('hide-item'))
    localStorage.setItem("small-menu", "disabled")
  }

  if (smallMenu === "enabled") {
    activeSmallMenu() // set state of darkMode on page load
  }

  toggleMenu[0].addEventListener('click', function () {
    smallMenu = localStorage.getItem('small-menu')
    if (smallMenu === "disabled") {
      activeSmallMenu()
    } else {
      activeBigMenu()
    }
  })

  hideSmallDeviceMenu.addEventListener('click', function () {
    smallMenu = localStorage.getItem('small-menu')
    if (smallMenu === "disabled") {
      activeSmallMenu()
    } else {
      activeBigMenu()
    }
  })

  if(window.innerWidth < 991) {
    sidebarMenu.forEach( item => {
      item.addEventListener('click', activeBigMenu)
    })
  }

  // sorting table data
  let sortDevices = document.querySelectorAll('.sort-devices')
  for (let i = 0; i < sortDevices.length; i++) {
    sortDevices[i].addEventListener('click', function () {
      sortTable(i)
    })
  }

  function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchCount = 0;
    table = document.getElementById("itemTable");

    switching = true;
    dir = "asc";

    while (switching) {
      switching = false;
      rows = table.rows;
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];

        if (dir == "asc") {
          if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            shouldSwitch = true;
            break;
          }
        } else if (dir == "desc") {
          if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
            shouldSwitch = true;
            break;
          }
        }
      }
      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        switchCount++;
      } else {
        if (switchCount == 0 && dir == "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  }


  // action icon show/hide 
  let actionIcon = document.querySelectorAll('.act-icon')
  for (let i = 0; i < actionIcon.length; i++) {
    actionIcon[i].addEventListener('click', function () {

      if (actionIcon[i].classList.contains('fa-eye')) {
        actionIcon[i].classList.remove('fa-eye')
        actionIcon[i].classList.add('fa-eye-slash');
      } else {
        actionIcon[i].classList.add('fa-eye')
        actionIcon[i].classList.remove('fa-eye-slash');
      }
    })
  }


  // toggle filter box
  $("#showFilter").click(function () {
    $(".filter-list").slideToggle();
  });
    // toggle filter box
  $("#showFilter2").click(function () {
    $(".filter-list2").slideToggle();
  });



  // input file and show file name
  const inputFileBtn = document.getElementsByClassName('file-input')[0]
  const getFile = document.getElementById('getFile')
  let showSelectedFile = document.getElementById('showSelectedFile')

  if (inputFileBtn) {
    inputFileBtn.addEventListener('click', function (e) {
      getFile.click()
      getFile.addEventListener('change', function () {
        showSelectedFile.innerHTML = this.files[0].name
      })
    })
  }


  // small device chat list toggle
  const toggleChatList = document.getElementsByClassName('msg-list-btn')[0]
  const chatList = document.getElementsByClassName('msg-list')[0]

  if (toggleChatList) {
    toggleChatList.addEventListener('click', function () {
      chatList.style.left = chatList.style.left === '0%' ? '-100%' : '0%'
    })
  }


  //Preloader
  setTimeout(function () {
    $('#preloader').fadeToggle();
  }, 1000);

  // Current Year
  $(".currentYear").text(new Date().getFullYear());




});