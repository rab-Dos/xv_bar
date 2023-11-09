// splash
const splash = document.querySelector('.splash')
const splash_2 = document.querySelector('.splash_2')

document.addEventListener('DOMContentLoaded', (e)=>{
  setTimeout(()=>{
    splash.classList.add('fade-out');
    // splash.classList.remove('flex');
    // splash.classList.add('hidden');
  }, 6000);  
})

document.addEventListener('DOMContentLoaded', (e)=>{
  setTimeout(()=>{
    splash.classList.remove('flex');
    splash.classList.add('hidden');
  }, 7000);  
})

document.addEventListener('DOMContentLoaded', (e)=>{
  setTimeout(()=>{
    splash_2.classList.remove('hidden');
    splash_2.classList.add('flex');
  }, 8000);  
})

//Phone Mask
function maskPhone(event) {
  let tecla = event.key;
  let phone = event.target.value.replace(/\D+/g, "");

  if (/^[0-9]$/i.test(tecla)) {
      phone = phone + tecla;
      let numero = phone.length;

      if (numero >= 11) {
          return false;
      }
      
      if (numero > 10) {
          phone = phone.replace(/^(\d\d)(\d{5})(\d{4}).*/, "($1) $2-$3");
      } else if (numero > 5) {
          phone = phone.replace(/^(\d\d)(\d{4})(\d{0,4}).*/, "($1) $2-$3");
      } else if (numero > 2) {
          phone = phone.replace(/^(\d\d)(\d{0,5})/, "($1) $2");
      } else {
          phone = phone.replace(/^(\d*)/, "($1");
      }

      event.target.value = phone;
  }

  if (!["Backspace", "Delete"].includes(tecla)) {
      return false;
  }
}

// reloj
const DATE_TARGET = new Date('12/09/2023 07:00 PM');
const SPAN_DAYS = document.querySelector('span#days');
const SPAN_HOURS = document.querySelector('span#hours');
const SPAN_MINUTES = document.querySelector('span#minutes');
const SPAN_SECONDS = document.querySelector('span#seconds');
const MILLISECONDS_OF_A_SECOND = 1000;
const MILLISECONDS_OF_A_MINUTE = MILLISECONDS_OF_A_SECOND * 60;
const MILLISECONDS_OF_A_HOUR = MILLISECONDS_OF_A_MINUTE * 60;
const MILLISECONDS_OF_A_DAY = MILLISECONDS_OF_A_HOUR * 24

let REMAINING_DAYS = 0;
let REMAINING_HOURS = 0;
let REMAINING_MINUTES = 0;
let REMAINING_SECONDS = 0;

function updateCountdown() {
  let NOW = new Date()
  let DURATION = DATE_TARGET - NOW; 

  if (DATE_TARGET < NOW) {
    REMAINING_DAYS = 0;
    REMAINING_HOURS = 0;
    REMAINING_MINUTES = 0;
    REMAINING_SECONDS = 0;
  }
  else{
    REMAINING_DAYS = Math.floor(DURATION / MILLISECONDS_OF_A_DAY);
    REMAINING_HOURS = Math.floor((DURATION % MILLISECONDS_OF_A_DAY) / MILLISECONDS_OF_A_HOUR);
    REMAINING_MINUTES = Math.floor((DURATION % MILLISECONDS_OF_A_HOUR) / MILLISECONDS_OF_A_MINUTE);
    REMAINING_SECONDS = Math.floor((DURATION % MILLISECONDS_OF_A_MINUTE) / MILLISECONDS_OF_A_SECOND);    
  }
  
  SPAN_DAYS.textContent = REMAINING_DAYS;
  SPAN_HOURS.textContent = REMAINING_HOURS;
  SPAN_MINUTES.textContent = REMAINING_MINUTES;
  SPAN_SECONDS.textContent = REMAINING_SECONDS;
}

updateCountdown();
setInterval(updateCountdown, MILLISECONDS_OF_A_SECOND);

// dialog
const dialog = document.querySelector("dialog");
const showButton = document.querySelector("dialog + button");
const closeButton = document.querySelector("dialog button");

showButton.addEventListener("click", ()=>{
  dialog.classList.remove("hidden");
  dialog.classList.add("flex");
  dialog.showModal();
});

closeButton.addEventListener("click", ()=>{
  dialog.classList.remove("flex");
  dialog.classList.add("hidden");
  dialog.close();
});

document.addEventListener("keydown", function(event) {
  if (event.key === "Escape") {
    dialog.classList.remove("flex");
    dialog.classList.add("hidden");
    dialog.close();
  }
});

// Galería
let control = 1;
let timeC;
let carItem;
let nCarItem;

function fadeIn() {
  
  if (control > 8) {
    control = 1;
  }
  
  carItem = document.querySelector('.carItem'+control);
  carItem.classList.remove("flex");
  carItem.classList.add("hidden");
  control += 1;

  if (control > 8){
    nCarItem = document.querySelector('.carItem1');
  }
  else {
    nCarItem = document.querySelector('.carItem'+control);
  }

  nCarItem.classList.remove("hidden");
  nCarItem.classList.add("flex");

  console.log("IMG en pantalla:",control)

}

window.onload = function() {
  timeC = setInterval('fadeIn()',4000);
};

// Limpiar luego de generar Boleto
function limpiar() {

  setTimeout(() => {
    // Se obtiene la zona para agregar la plantilla
    const cuerpo = document.getElementById("sendData")    
    
    fetch("/boleto_ok", { method: "GET"})
    .then(response => {
      return response.text();
    })
    .then(html => {
      cuerpo.innerHTML = html
    })
    
  }, 3000)

}