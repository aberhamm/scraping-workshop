// Add a custom header to the page
// let header = document.createElement("h1");
// header.textContent = "Injected by Splash Spider!";
// header.style.color = "white";
// header.style.textAlign = "center";
// header.style.marginTop = "20px";
// document.body.prepend(header);

document.addEventListener("DOMContentLoaded", () => {
    [...document.querySelectorAll(".show, .collapse, .fade")].forEach(
        (element) => {
            element.classList.remove("show", "collapse", "fade");
        }
    );
});
