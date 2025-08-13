document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll("li a");
    links.forEach(link => {
        link.addEventListener("click", () => {
            link.style.transition = "transform 0.15s ease";
            link.style.transform = "scale(0.95)";
            setTimeout(() => {
                link.style.transform = "scale(1)";
            }, 150);
        });
    });
});
