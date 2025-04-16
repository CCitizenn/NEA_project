const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');
const loginPopup = document.querySelector('.btnLogin-popup');
const closePopup = document.querySelector('.icon-close');
const middleSection = document.querySelector('.middle');


registerLink.addEventListener('click', ()=> {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', ()=> {
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', ()=> {
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', ()=> {
    wrapper.classList.remove('active-popup');
    wrapper.classList.remove('active');
});

/* hides the middle 2 buttons on clicking "login"*/

loginPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup');
    middleSection.classList.add('hidden'); 
});

/*shows the middle section on re-clicking "login"*/
closePopup.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
    middleSection.classList.remove('hidden'); 
})